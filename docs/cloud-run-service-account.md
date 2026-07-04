# Cloud Run least-privilege service account (prep)

**Status:** not yet applied. This is a runbook to fix audit Finding #3 — the
`skill-library-mcp` Cloud Run service currently runs as the project's **default
Compute Engine service account**, which holds broad `Editor`. The service is
`--allow-unauthenticated` (public) and holds a repo-write PAT, so a code-exec bug
or leaked token would inherit project-wide `Editor`. Pin a dedicated SA with only
the roles the service actually needs.

## What the service actually needs

Verified against `mcp-server/`:
- **Secret Manager read** for the three secrets the deploy injects:
  `github-bot-pat`, `anthropic-api-key`, `maint-trigger-token`.
- **Nothing else.** The server reads skills/registry from files baked into the
  image (`COPY . .`), and the maintenance bot writes back via GitHub PRs using
  `GITHUB_BOT_PAT` — neither path calls Firestore, GCS, or other GCP APIs. So
  `roles/secretmanager.secretAccessor` (scoped to the three secrets) is the whole
  role set.

## Steps

Set your values (from `.github/workflows/deploy.yml` repo vars):

```bash
PROJECT=skill-library-prod
REGION=us-central1
SA=skill-library-mcp-runtime
SA_EMAIL="${SA}@${PROJECT}.iam.gserviceaccount.com"
# The identity CI deploys as (Workload Identity Federation SA), = vars.GCP_SERVICE_ACCOUNT
DEPLOYER_SA="<paste vars.GCP_SERVICE_ACCOUNT from repo settings>"
```

**1. Create the runtime SA**
```bash
gcloud iam service-accounts create "$SA" \
  --project="$PROJECT" \
  --display-name="skill-library-mcp Cloud Run runtime (least privilege)"
```

**2. Grant read on exactly the three secrets** (per-secret, not project-wide)
```bash
for S in github-bot-pat anthropic-api-key maint-trigger-token; do
  gcloud secrets add-iam-policy-binding "$S" \
    --project="$PROJECT" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/secretmanager.secretAccessor"
done
```

**3. Let the CI deployer act as the new SA** (required to deploy a service that
runs *as* it)
```bash
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --project="$PROJECT" \
  --member="serviceAccount:${DEPLOYER_SA}" \
  --role="roles/iam.serviceAccountUser"
```

**4. Pin it in the deploy pipeline** — add ONE flag to the `gcloud run deploy`
step in `.github/workflows/deploy.yml` (do this only after steps 1–3, or the
deploy will fail with a missing-SA error):
```diff
           --allow-unauthenticated \
+          --service-account="skill-library-mcp-runtime@skill-library-prod.iam.gserviceaccount.com" \
           --max-instances=1 \
```
(If you also keep `cloudrun/service.yaml` in sync for documentation, set
`spec.template.spec.serviceAccountName` there too — but note CI deploys via flags,
not that file.)

**5. Deploy & verify**
```bash
# trigger the normal deploy (merge to main), then confirm the running SA:
gcloud run services describe skill-library-mcp \
  --region="$REGION" --project="$PROJECT" \
  --format="value(spec.template.spec.serviceAccountName)"
# → skill-library-mcp-runtime@skill-library-prod.iam.gserviceaccount.com
```
Then hit `/health` (should still be 200) and exercise a `/maint/*` endpoint with
the token (confirms secret access still works under the new SA).

## Rollback
Remove the `--service-account` flag from `deploy.yml` and redeploy; the service
reverts to the default Compute SA. The dedicated SA and its bindings can be left
in place or deleted (`gcloud iam service-accounts delete "$SA_EMAIL"`).
