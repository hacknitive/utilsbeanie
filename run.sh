#!/bin/bash

# Exit immediately if a command exits with a non-zero status,
# Treat unset variables as an error and exit immediately,
# Prevent errors in a pipeline from being masked
set -euo pipefail

# # Load environment variables from configs/.env
# if [ -f "configs/.env" ]; then
#     export $(grep -v '^#' configs/.env | xargs)
# else
#     echo "Config file configs/.env not found!"
#     exit 1
# fi

# Define functions for each command
up-infra() {
    docker compose -f tests/docker-compose.yml up mongo -d --remove-orphans
}

stop-infra() {
    docker compose -f tests/docker-compose.yml stop mongo
}

down-infra() {
    docker compose -f tests/docker-compose.yml down mongo -v
}

infra-test() {
    docker compose -f tests/docker-compose.yml up mongo -d --remove-orphans
    pytest tests/ --cache-clear
    docker compose -f tests/docker-compose.yml down mongo -v
}

test() {
    pytest tests/ --cache-clear
}

cov-test() {
    coverage run -m pytest tests/ --cache-clear
    coverage report
}

cov-show() {
    coverage report
}

# Function to display usage
usage() {
    echo "Usage: $0 {up|log|up-build|up-web|test|shell|stop|lint-code|down|deep-clean|help}"
    echo
    echo "Commands:"
    echo "  up-infra        Bring Mongodb container up."
    echo "  stop-infra      stop Mongodb container."
    echo "  down-infra      Delete Mongodb container and its volume and network."
    echo "  infra-test      Bring Mongodb up then run tests by this command 'pytest /tests --clear-cache'."
    echo "  test            Run tests by this command 'pytest /tests --clear-cache'."
    echo "  cov-test        Run tests by coverage then show the report."
    echo "  cov-show        Show coverage report."
    echo "  help            Display this help message."
    exit 1
}

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Error: No command provided."
    usage
fi

# Parse the first argument
case "$1" in
    up-infra)
        up-infra
        ;;
    stop-infra)
        stop-infra
        ;;
    down-infra)
        down-infra
        ;;
    infra-test)
        infra-test
        ;;
    test)
        test
        ;;
    cov-test)
        cov-test
        ;;
    cov-show)
        cov-show
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo "Error: Unknown command '$1'"
        usage
        ;;
esac
