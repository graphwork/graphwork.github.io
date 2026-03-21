#!/usr/bin/env bash
# Setup script for TUI screencast demo.
# Creates a realistic-looking workgraph project with tasks and dependencies.
set -euo pipefail

DEMO_DIR="${1:-/tmp/wg-demo}"

rm -rf "$DEMO_DIR"
mkdir -p "$DEMO_DIR"
cd "$DEMO_DIR"
git init -q

# Initialize workgraph
wg init -q 2>/dev/null || wg init

# Add tasks with a realistic dependency graph
# Phase 1: Design
wg add "Design API schema" --id design-api -d "Define REST endpoints, request/response types, and authentication flow"
wg add "Design database schema" --id design-db -d "Define tables, indexes, and migration strategy"

# Phase 2: Implementation (depends on design)
wg add "Implement auth service" --id impl-auth --after design-api -d "JWT-based authentication with refresh tokens"
wg add "Implement user endpoints" --id impl-users --after design-api,design-db -d "CRUD operations for user management"
wg add "Implement data pipeline" --id impl-pipeline --after design-db -d "ETL pipeline for analytics data ingestion"

# Phase 3: Testing (depends on implementation)
wg add "Integration tests" --id integration-tests --after impl-auth,impl-users -d "End-to-end API testing with test fixtures"
wg add "Load testing" --id load-tests --after impl-pipeline -d "Benchmark pipeline throughput under load"

# Phase 4: Deploy
wg add "Deploy to staging" --id deploy-staging --after integration-tests,load-tests -d "Deploy all services to staging environment"

# Simulate some progress — mark design tasks as done
wg claim design-api 2>/dev/null || true
wg done design-api 2>/dev/null || true
wg claim design-db 2>/dev/null || true
wg done design-db 2>/dev/null || true

# Mark one implementation task in-progress
wg claim impl-auth 2>/dev/null || true

echo "Demo project ready at $DEMO_DIR"
