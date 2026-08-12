#!/usr/bin/env bash

set -euo pipefail

IMAGE="zenwing/human-tracking-dev:latest"

usage() {
    echo "Usage: ./dev.sh {build|pull|run}"
    exit 1
}

build() {
    echo "==> Building $IMAGE..."
    docker build -t "$IMAGE" .
}

pull() {
    echo "==> Pulling $IMAGE..."
    docker pull "$IMAGE"
}

run() {
    echo "==> Starting development container..."

    docker run --rm -it \
        -v "$(pwd):/workspace" \
        "$IMAGE"
}

if [[ $# -ne 1 ]]; then
    usage
fi

case "$1" in
    build)
        build
        ;;
    pull)
        pull
        ;;
    run)
        run
        ;;
    *)
        usage
        ;;
esac
