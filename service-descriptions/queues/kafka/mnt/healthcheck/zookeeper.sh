ZK_PORT=${ZK_PORT:-2181}

res=$(echo ruok | nc localhost $ZK_PORT)
rc=$?
if [ "$res" != "imok" ]; then
  echo "Bad result: $res"
  echo "$rc"
  exit 1
fi
