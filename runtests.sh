#!/bin/bash

pushd . >/dev/null
cd "$(dirname ${BASH_SOURCE[0]})"
coverage run -m unittest discover && echo '====' && coverage report -im
popd >/dev/null
