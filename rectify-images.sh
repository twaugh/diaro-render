#!/bin/bash

if [ "$#" -lt 2 ]; then
    printf "Syntax: $0 XML-PATH MEDIA-FILE[...]\n"
    exit 1
fi

XML=$1
shift

for img in "$@"; do
    ext=${img##*.}
    mimetype=$(file --brief --mime-type "$img")
    realext=${mimetype#image/}
    realext=${realext/jpeg/jpg}
    case "$realext" in
        jpg|png)
            ;;
        *)
            continue
            ;;
    esac
    if [ "$ext" == "$realext" ]; then
        continue
    fi
    basename=$(basename "$img")
    printf "s/\\(${basename%.*}[^.]*\.\\)$ext/\\\\1$realext/g\n"
done | sed -i.orig -f /dev/stdin "$XML"
