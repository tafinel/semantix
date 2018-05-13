#!/bin/bash
echo "[INFO] -------TESTE SEMANTIX"
echo "[INFO] -------CARLOS TAFINEL"
echo "[INFO] ---------------------"
sh decompress.sh $1
python nasa.py $1
rm files/d/*