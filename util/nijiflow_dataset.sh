#!/bin/bash
#
# pixivpy_wrapper to nijiflow data file format
#  https://github.com/fallthrough/nijiflow
#
set -u
set -eu
set -o pipefail

trap 'echo "error:$0($LINENO) \"$BASH_COMMAND\" \"$@\""' ERR

python3 util/nijiflow_dataset_from_path.py 0 ${HOME}/pixiv_data/image__艦これ         アズールレーン,アズレン
python3 util/nijiflow_dataset_from_path.py 1 ${HOME}/pixiv_data/image__アズールレーン 艦これ,艦隊これくしょん

