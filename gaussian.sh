#!/bin/bash

docker run \
--user=morikawa \
--rm -it \
-v $(pwd):/workdir \
-w /workdir \
muscle/chem:3.6 \
"$@"
