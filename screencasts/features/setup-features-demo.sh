#!/usr/bin/env bash
# Setup script for feature screenshot demos.
# Creates a rich workgraph project with tasks, dependencies, cycles, agents, and evaluations.
set -euo pipefail

# Unset agent identity so demo setup doesn't count against agent limits
unset WG_AGENT_ID

DEMO_DIR="${1:-/tmp/wg-features-demo}"

rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"
git init -q

# Initialize workgraph
wg init -q 2>/dev/null || wg init

# ── Phase 1: Design ──
wg add "Design API schema" --id design-api -d "Define REST endpoints, request/response types, and authentication flow"
wg add "Design database schema" --id design-db -d "Define tables, indexes, and migration strategy for PostgreSQL"
wg add "Design event system" --id design-events -d "Define event bus architecture and message formats"

# ── Phase 2: Implementation (depends on design) ──
wg add "Implement auth service" --id impl-auth --after design-api -d "JWT-based authentication with refresh tokens and OAuth2 support"
wg add "Implement user endpoints" --id impl-users --after design-api,design-db -d "CRUD operations for user management with pagination"
wg add "Implement data pipeline" --id impl-pipeline --after design-db,design-events -d "ETL pipeline for analytics data ingestion with backpressure"
wg add "Implement notification service" --id impl-notify --after design-events -d "Push notifications via WebSocket and email digest"
wg add "Implement search index" --id impl-search --after design-db -d "Full-text search with Elasticsearch integration"

# ── Phase 3: Testing ──
wg add "Integration tests" --id integration-tests --after impl-auth,impl-users -d "End-to-end API testing with test fixtures and mocks"
wg add "Load testing" --id load-tests --after impl-pipeline -d "Benchmark pipeline throughput under load with k6"
wg add "Security audit" --id security-audit --after impl-auth,impl-notify -d "OWASP top-10 vulnerability scan and penetration testing"

# ── Phase 4: Deploy ──
wg add "Deploy to staging" --id deploy-staging --after integration-tests,load-tests,security-audit -d "Deploy all services to staging environment with blue-green strategy"
wg add "Production release" --id prod-release --after deploy-staging -d "Canary deployment to production with rollback plan"

# ── Cycle: CI pipeline ──
wg add "Run CI checks" --id ci-checks --after impl-auth --max-iterations 3 -d "Lint, test, and build in CI pipeline"
wg add "Fix CI failures" --id ci-fix --after ci-checks -d "Address any CI failures found"
# Add back-edge for cycle
wg edge ci-fix ci-checks 2>/dev/null || true

# ── Documentation tasks ──
wg add "Write API docs" --id api-docs --after design-api -d "OpenAPI spec and developer guide"
wg add "Architecture decision record" --id adr --after design-api,design-db,design-events -d "Document key architecture decisions and tradeoffs"

# ── Simulate progress ──
wg claim design-api 2>/dev/null || true
wg done design-api 2>/dev/null || true
wg claim design-db 2>/dev/null || true
wg done design-db 2>/dev/null || true
wg claim design-events 2>/dev/null || true
wg done design-events 2>/dev/null || true

# Mark implementation tasks in various states
wg claim impl-auth 2>/dev/null || true
wg done impl-auth 2>/dev/null || true
wg claim impl-users 2>/dev/null || true
# impl-users stays in-progress
wg claim impl-pipeline 2>/dev/null || true
# impl-pipeline stays in-progress
wg claim api-docs 2>/dev/null || true
wg done api-docs 2>/dev/null || true

# CI cycle - first iteration done
wg claim ci-checks 2>/dev/null || true
wg done ci-checks 2>/dev/null || true

# Initialize agency
wg agency init 2>/dev/null || true

# Add a message for chat demo
wg msg send impl-users "The pagination should use cursor-based approach, not offset" 2>/dev/null || true
wg msg send impl-pipeline "Backpressure handled via bounded channel — see design doc" 2>/dev/null || true

echo "Features demo project ready at $DEMO_DIR"
