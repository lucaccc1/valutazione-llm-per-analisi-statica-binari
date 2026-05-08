#!/bin/bash

ida_path="/home/luca/ida-pro-9.1/idat"
gt_script="scripts/ida/extract_gt.py"
strip_script="scripts/ida/extract_decomp.py"

echo "extracting ground truth..."

while IFS= read -r -d '' file; do
    echo "processing $file"
    $ida_path -c -A -pmetapc -S"$gt_script" "$file"
done < <(find dataset/bin_debug -type f -name "*.out" -print0)

echo "extracting llm inputs..."

while IFS= read -r -d '' file; do
    echo "processing $file"
    $ida_path -c -A -pmetapc -S"$strip_script" "$file"
done < <(find dataset/bin_stripped -type f -name "*.out" -print0)

echo "completed."