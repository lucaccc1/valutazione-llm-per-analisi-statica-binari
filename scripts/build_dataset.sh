#!/bin/bash

SOURCE_DIR="dataset/src"
DEBUG_DIR="dataset/bin_debug"
STRIPPED_DIR="dataset/bin_stripped"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "source directory '$SOURCE_DIR' not found."
    exit 1
fi

echo "starting recursive compilation in $SOURCE_DIR"

INCLUDE_FLAGS=$(find "$SOURCE_DIR" -type d -printf "-I %p ")

while IFS= read -r -d '' file; do
    rel_path="${file#$SOURCE_DIR/}"
    sub_dir=$(dirname "$rel_path")
    basename=$(basename "$file" .c)
    
    current_debug_dir="$DEBUG_DIR/$sub_dir"
    current_stripped_dir="$STRIPPED_DIR/$sub_dir"
    
    mkdir -p "$current_debug_dir"
    mkdir -p "$current_stripped_dir"
    
    debug_bin="$current_debug_dir/${basename}_debug.out"
    stripped_bin="$current_stripped_dir/${basename}_stripped.out"

    echo "processing $rel_path"

    if gcc -g "$INCLUDE_FLAGS" "$file" -o "$debug_bin" -lm; then
        cp "$debug_bin" "$stripped_bin"
        strip "$stripped_bin"
    else
        echo "warning: failed to compile $rel_path."
    fi
done < <(find "$SOURCE_DIR" -type f -name "*.c" -print0)

echo "processing completed."