#!/bin/bash

set -euxo pipefail

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$SCRIPT_DIR/../"

if [[ ! -d "node_modules" ]]; then
    yarn install
    yarn run gitbook install
fi

yarn run gitbook build . docs
