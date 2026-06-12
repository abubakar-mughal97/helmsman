#!/usr/bin/env bash
# Helmsman dev environment bring-up.
set -e

# X11 access for local containers — resets on logout/reboot, so grant it every time.
xhost +local: > /dev/null

# Guard against Docker Desktop hijacking the CLI context.
if [ "$(docker context show)" != "default" ]; then
    echo "Docker context is '$(docker context show)' — switching to native engine."
    docker context use default
fi

# Start (or recreate, if config changed) the dev container.
docker compose -f "$(dirname "$0")/../docker/compose.yaml" up -d

echo "Ready. Enter with:  docker exec -it helmsman bash"