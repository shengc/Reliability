#!/bin/bash

# Put your data file under directory "data"
# e.g. of usage
# ./run.sh comments.dat
# ./run.sh music.dat

DIR=`cd $(dirname $(cd $(dirname $0) && pwd)) && pwd`

PYTHONPATH=$PYTHONPATH:$DIR/src python -m main.Main $@
