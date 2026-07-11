# Cloud Run least-privilege service account

**Status:** applied 2026-07-11 as part of the split-brain fix Phase 2. The
`skill-library-mcp` Cloud Run service is pinned to a dedicated runtime SA via
`--service-account` in `.github/workflows/deploy.yml` (repo var
`RUNTIME_SA_EMAIL`), with a post-deploy verification step that fails the deploy
if the running SA differs. Previously the service ran as the project's default
Compute Engine service account with broad `Editor` — unacceptable for a public
`--allow-unauthenticated` service holding a repo-write PAT.

## What the service actually needs

Verified against `mcp-server/`:
- **Secret Manager read** for the three secrets the deploy injects:
  `github-bot-pat`, `anthropic-api-key`, `maint-trigger-token`.
- **Firestore writes** (`roles/datastore.user`) for telemetry mirroring:
  `firestore_telemetry.py` mirrors usage/gap/feedback events to the `usage`,
  `gaps`, and `feedback` collections (gated on `MCP_REMOTE=true` +
  `TELEMETRY_FIRESTORE=1`). The local jsonl these events also append to is
  ephemeral on Cloud Run; the Firestore mirror is what the telemetry pull loop
  exports back into git. **Removing this role silently kills telemetry** — the
  mirror is best-effort by design and will not fail tool calls.
- **Nothing else.** The server reads skills/registry from files baked into the
  image (`COPY . .`), and the maintenance bot writes back via GitHub PRs using
  `GITHUB_BOT_PAT`.

## Setup (one-time, already applied)

Set your values (from `.github/workflows/deploy.yml` repo vars):

```bash
PROJECT=skill-library-prod
REGION=us-central1
SA=skill-library-mcp-runtime
SA_EMAIL="${SA}@${PROJECT}.iam.gserviceaccount.com"
# The identity CI deploys as (Workload Identity Federation SA), = vars.DEPLOY_SA_EMAIL
DEPLOYER_SA="<paste vars.DEPLOY_SA_EMAIL from repo settings>"
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

**3. Grant Firestore write for telemetry mirroring**
```bash
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/datastore.user"
```

**4. Let the CI deployer act as the new SA** (required to deploy a service that
runs *as* it)
```bash
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --project="$PROJECT" \
  --member="serviceAccount:${DEPLOYER_SA}" \
  --role="roles/iam.serviceAccountUser"
```

**5. Set the repo variable** consumed by `deploy.yml`:
```bash
gh variable set RUNTIME_SA_EMAIL --body "$SA_EMAIL"
```

**6. Deploy & verify** — the deploy workflow now does this automatically: it
passes `--service-account="${{ vars.RUNTIME_SA_EMAIL }}"` and then fails the
run if `gcloud run services describe` reports a different SA. Manual check:
```bash
gcloud run services describe skill-library-mcp \
  --region="$REGION" --project="$PROJECT" \
  --format="value(spec.template.spec.serviceAccountName)"
# → skill-library-mcp-runtime@skill-library-prod.iam.gserviceaccount.com
```
Then hit `/health` (should still be 200), exercise a `/maint/*` endpoint with
the token (confirms secret access), and call `search_skills` then check the
Firestore `usage`/`gaps` collections for the mirrored event (confirms
`datastore.user`).

## Rollback

Remove the `--service-account` flag and the "Verify runtime service account"
step from `deploy.yml` and redeploy; the service reverts to the default
Compute SA. The dedicated SA and its bindings can be left in place or deleted
(`gcloud iam service-accounts delete "$SA_EMAIL"`).
