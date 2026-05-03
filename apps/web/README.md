# EPCC Web (React + Vite)

Frontend for EPCC. Implements module wireframes M01, M02, M03, M04, M34.

## Layout

```
apps/web/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── biome.json
├── tailwind.config.ts
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── routes/
│   ├── modules/         # one folder per spec (m34_*, m01_*, ...)
│   ├── components/      # shadcn/ui copies + custom
│   ├── lib/             # api client, auth, utils
│   └── styles/
├── public/
└── tests/               # Vitest unit + Playwright e2e
```

## Local development

```bash
cd apps/web
pnpm install
pnpm dev          # http://localhost:5173
pnpm test         # vitest
pnpm e2e          # playwright (requires backend running)
pnpm lint         # biome
pnpm typecheck    # tsc
```

Or, from the repo root: `make dev`.
