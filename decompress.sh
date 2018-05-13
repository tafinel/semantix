#!/bin/bash
echo "[INFO] ------DECOMPRESS FILE"
echo "[INFO] Arquivo: "$1
echo "[INFO] ---------------------"

arquivo=$1
origem="files/"$1
destino="files/d/"$1

echo "[INFO] Inicio da descompactacao"
echo "[INFO] cat ${origem}*.gz | gzip -d > ${destino}"
cat ${origem}*.gz | gzip -d > ${destino}
echo "[INFO] Fim da descompactacao"