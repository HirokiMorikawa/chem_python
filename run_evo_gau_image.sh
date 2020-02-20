#!/bin/bash

docker run --rm -it -v $(pwd):/workdir -v /usr/local/gaussian16:/usr/local/gaussian16 -v /work:/work -w /workdir muscle/chem:muscle /bin/bash
