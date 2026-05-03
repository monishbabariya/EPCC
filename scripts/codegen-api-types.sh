#!/usr/bin/env bash
# OpenAPI -> TypeScript codegen.
#
# Round 25 scaffold: prints plan, exits 0. Round 26 replaces with a real
# pipeline:
#   1. Boot the API (or use a pre-dumped openapi.json)
#   2. Run `openapi-typescript apps/api/openapi.json -o packages/api-types/src/_generated.ts`

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_FILE="$REPO_ROOT/packages/api-types/src/_generated.ts"
OPENAPI_JSON="$REPO_ROOT/apps/api/openapi.json"

echo "OpenAPI spec : $(echo "$OPENAPI_JSON" | sed "s|$REPO_ROOT/||")"
echo "TS output    : $(echo "$OUT_FILE" | sed "s|$REPO_ROOT/||")"
echo
echo "Round 25 scaffold — api-types codegen not yet implemented. Round 26 replaces this stub."
