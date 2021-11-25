#!/bin/bash

set -euxo pipefail

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

docker run --rm -it -v"$SCRIPT_DIR/../":/src -u 1000 node:8.17.0-slim bash /src/docker/_build.sh
