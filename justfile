set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

install:
    npm ci

dev:
    npm run dev -- --host 127.0.0.1

build:
    npm run build

lint:
    npm run lint

typecheck:
    npm run typecheck

# Python host: lint + import smoke test against the published auroraview wheel.
py-check:
    uvx ruff check --target-version py311 main.py backend/ scripts/
    uvx ruff format --check --target-version py311 main.py backend/ scripts/
    python -c "import sys; sys.path.insert(0, '.'); import backend; print('backend imports OK;', len(backend.get_samples_list()), 'samples discovered')"

# Refresh the vendored examples/ copy from a local try-auroraview/auroraview checkout.
sync-examples checkout:
    python scripts/sync_examples.py {{checkout}}

check: build lint py-check
