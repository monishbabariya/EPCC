# MinIO

Bootstrapped by `docker-compose.yml` `minio-init` service. Buckets created
idempotently on first run:

- `epcc-photos` — M04 ProgressEntry photo attachments (until M12 lands)
- `epcc-documents` — generic document storage (M12 will own)
- `epcc-exports` — generated CSVs / PDFs

Console: <http://localhost:9001> (default creds `minio` / `miniopassword` —
override via `.env.local`).
