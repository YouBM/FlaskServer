#!/bin/bash
# run bash script of prod2pic

productName="${1:-Nike Reax 8 TR}"
dbFile="${2:-./pics-of-shoes.csv}"

grep "${productName}" ${dbFile} | tail -n 1 | cut -f 2 -d';' | cut -f 1 -d','
