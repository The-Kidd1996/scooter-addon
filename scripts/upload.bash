#!/bin/bash

for file in *.py; do
    echo [Upload]: Processing file $file
    ampy put $file /$file
done

echo [Upload]: Reset
ampy reset
