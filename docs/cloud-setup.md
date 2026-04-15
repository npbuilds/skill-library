# Cloud Setup — one-time prerequisites for Layer 1 deploy

This document lists the one-time GCP + GitHub setup you must complete
before `.github/workflows/deploy.yml` can successfully deploy the MCP
server to Cloud Run.

**You do these steps once, by hand, on your machine.** Subsequent
deploys happen automatically when CI passes on `main`.

Follow sections top-to-bottom. Where a value appears in `<ANGLE_BRACKETS>`,
substitute your own.

---

## 0. Decide your values

| Variable | Example | What it is |
|---|---|---|
| `PROJECT_ID` | `skill-library-prod` | GCP project ID (globally unique) |
| `REGION` | `us-central1` | Cloud Run + Artifact Registry region |
| `AR_REPO` | `skill-library-images` | Artifact Registry repo name |
| `DEPLOY_SA` | `github-deployer` | Service account name for the GitHub deploy workflow |
| `GITHUB_REPO` | `npbuilds/skill-library` | This repo |

You'll use these repeatedly. Export them in your shell for the session:

```bash
export PROJECT_ID=skill-library-prod
export REGION=us-central1
export AR_REPO=skill-library-images
export DEPLOY_SA=github-deployer
export GITHUB_REPO=npbuilds/skill-library
```

---

## 1. Create the GCP project + enable billing

```bash
gcloud projects create "$PROJECT_ID" --name="Skill Library"
gcloud config set project "$PROJECT_ID"
```

Then **enable billing** for the project in the Cloud Console
(https://console.cloud.google.com/billing/linkedaccount). APIs won't
enable until billing is linked.

---

## 2. Enable required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com
```

---

## 3. Create the Artifact Registry repo

```bash
gcloud artifacts repositories create "$AR_REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Container images for the skill library MCP server"
```

---

## 4. Create the deploy service account

```bash
gcloud iam service-accounts create "$DEPLOY_SA" \
  --display-name="GitHub Actions — Cloud Run deployer"

export DEPLOY_SA_EMAIL="${DEPLOY_SA}@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant least-privilege roles it needs to build + deploy.
for role in \
  roles/run.admin \
  roles/artifactregistry.writer \
  roles/cloudbuild.builds.editor \
  roles/storage.admin \
  roles/iam.serviceAccountUser \
  roles/logging.logWriter
do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${DEPLOY_SA_EMAIL}" \
    --role="$role"
done
```

> `storage.admin` is needed because Cloud Build stages source in a bucket.
> `iam.serviceAccountUser` lets it act as the Cloud Run runtime SA.

---

## 5. Set up Workload Identity Federation (no JSON keys)

This lets GitHub Actions authenticate to GCP via OIDC tokens — no
long-lived JSON keys stored in GitHub.

```bash
# 5a. Pool
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --display-name="GitHub Actions pool"

# 5b. Provider (attributes map GitHub's OIDC claims to GCP principals)
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub OIDC" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '$(echo $GITHUB_REPO | cut -d/ -f1)'" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# 5c. Allow this repo's workflows to impersonate the deploy SA
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')

gcloud iam service-accounts add-iam-policy-binding "$DEPLOY_SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/${GITHUB_REPO}"

# 5d. Capture the provider resource name — you'll paste this into GitHub
export WIF_PROVIDER="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/providers/github-provider"
echo "WIF_PROVIDER = $WIF_PROVIDER"
echo "DEPLOY_SA_EMAIL = $DEPLOY_SA_EMAIL"
```

---

## 6. Configure GitHub repository variables

In your repo on github.com: **Settings → Secrets and variables → Actions → Variables tab**.

Add these **variables** (not secrets — they aren't sensitive; visibility is fine):

| Name | Value |
|---|---|
| `GCP_PROJECT_ID` | your `$PROJECT_ID` |
| `GCP_REGION` | your `$REGION` |
| `AR_REPO` | your `$AR_REPO` |
| `WIF_PROVIDER` | the `$WIF_PROVIDER` value from step 5d |
| `DEPLOY_SA_EMAIL` | the `$DEPLOY_SA_EMAIL` value from step 4 |

No secrets are needed at this stage. (Secret Manager values like the
bot PAT are injected into Cloud Run directly in Layer 2, not through
GitHub Actions.)

---

## 7. First deploy — smoke test

1. Commit & push `.github/workflows/deploy.yml`, `cloudrun/service.yaml`,
   and this doc to `main`.
2. CI runs on push to main. When CI succeeds, `deploy.yml` fires via
   `workflow_run`.
3. Watch the deploy job: `gh run watch` or the Actions tab.
4. When it completes, get the service URL:
   ```bash
   gcloud run services describe skill-library-mcp \
     --region="$REGION" --format='value(status.url)'
   ```
5. Smoke test (Cloud Run requires auth — use your gcloud identity token):
   ```bash
   SERVICE_URL=$(gcloud run services describe skill-library-mcp \
     --region="$REGION" --format='value(status.url)')
   curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     "$SERVICE_URL/"
   ```
   You should see an MCP server response (not a 401 / 403 / 500).

If the service is deployed with `--no-allow-unauthenticated`, only
callers with a valid IAM identity token can reach it. For claude.ai
access, see [Section 9](#9-grant-claudeai-access-optional).

---

## 8. Redeploying

Push any commit to `main` → CI runs → deploy.yml runs on success.
No manual step. To redeploy the same commit (e.g., after changing env
vars in `deploy.yml`), use **Actions → Deploy to Cloud Run → Run workflow**.

To roll back to a previous revision:

```bash
gcloud run revisions list --service=skill-library-mcp --region="$REGION"
gcloud run services update-traffic skill-library-mcp \
  --region="$REGION" \
  --to-revisions=<previous-revision-name>=100
```

---

## 9. Grant claude.ai access (optional, once remote MCP is ready)

When you want claude.ai (web/mobile) to reach the MCP server, you have
two options:

**Option A — Public access with bearer token auth in the app layer.**
Relax Cloud Run's IAM to `allUsers`, then require a bearer token at
the application level (verified in `mcp-server/server.py`). Simpler;
slightly less secure.

**Option B — Keep IAM private, mint identity tokens for claude.ai.**
claude.ai doesn't natively support GCP IAM, so this path requires a
small token-minting proxy or public wrapper. More secure; more work.

Decision on this is **deferred until Layer 2 lands** — by then the
maintenance endpoints also need auth and we'll pick one model for both.

---

## 10. Kill switch

To pause the service without deleting it:

```bash
gcloud run services update skill-library-mcp \
  --region="$REGION" \
  --max-instances=0
```

Set back to `1` to restore.

To fully tear down:

```bash
gcloud run services delete skill-library-mcp --region="$REGION"
gcloud artifacts repositories delete "$AR_REPO" --location="$REGION"
# (Leave the GCP project unless you're certain.)
```

---

## Appendix — verification checklist

After completing steps 1–7:

- [ ] `gcloud config get-value project` returns your `PROJECT_ID`
- [ ] `gcloud artifacts repositories list` shows `$AR_REPO`
- [ ] `gcloud iam service-accounts list` shows `$DEPLOY_SA_EMAIL`
- [ ] `gcloud iam workload-identity-pools list --location=global` shows `github-pool`
- [ ] In GitHub, all 5 variables above are set under repo settings
- [ ] `.github/workflows/deploy.yml` exists on `main`
- [ ] A deploy run has succeeded in the Actions tab
- [ ] `curl` against the service URL returns an MCP response (with identity token)

If any of these fail, the deploy workflow won't succeed — each is a
precondition, not optional.
