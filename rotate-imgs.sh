#!/bin/bash

for f in "$@"
do
  CONV_PARAMS="-interpolative-resize 1024x1024"
  mimetype=$(file "$f" | sed -e 's,^[^:]*: \([^ ]*\) .*$,\1,')
  if [ "$mimetype" == "JPEG" ]; then
    jhead -autorot "$f" && jhead -norot "$f"
  elif [ "$mimetype" == "PNG" ]; then
    CONV_PARAMS="$CONV_PARAMS -auto-orient"
  else
    echo "Unhandled: $f ($mimetype)"
    break
  fi
  convert $CONV_PARAMS "$f" "tmp-$f" && mv "tmp-$f" "$f"
done
