#!/bin/bash

# Variables
base_dir="/lustrefs/hdd_pool_dir/L1T/Filter/ThresholdScan_Zprime_DY"
out_dir="/lustrefs/hdd_pool_dir/L1T/Filter/ThresholdScan_Zprime_DY/results"  # Cambia esto a la ruta donde quieres guardar los resultados
index=1  # Contador inicial

# Bucle que recorre los nombres de las carpetas en base_dir
for folder in $(ls $base_dir); do
    folder_path="$base_dir/$folder/0000/"
    
    # Verificamos si la carpeta 0000 existe dentro del folder
    if [ -d "$folder_path" ]; then
        # Extraemos el THRESHOLD del nombre de la carpeta o de otro criterio
        threshold=$(ls "$folder_path" | grep -oP 'thr\d+' | head -n 1)  # Cambia THRESHOLD_PATTERN a tu patrón específico

        # Formar el nombre del archivo de salida y ejecutar sbatch
        outfilename="_${threshold}"
        
        echo "Submitting job for folder: $folder_path with threshold: $threshold"

        sbatch -c 8 -p batch -J destrada-$index --wrap "python3 concentrator.py -i $folder_path --outfilename=$outfilename --outfolder=$out_dir"

        # Incrementar el contador
        index=$((index + 1))
    else
        echo "Skipping folder: $folder (no 0000 directory found)"
    fi
done