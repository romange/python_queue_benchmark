#!/usr/bin/env bash
set -e

NUM_WORKERS="${NUM_WORKERS:-10}"

START=$(date +%s.%N)
taskiq worker --workers "$NUM_WORKERS" --log-level ERROR tasks:broker &
WORKER_PID=$!

python drain.py "$WORKER_PID"
wait "$WORKER_PID" 2>/dev/null || true
END=$(date +%s.%N)
echo "Total time: $(echo "$END - $START" | bc) seconds"

python -c "
from redis import Redis
r = Redis()
groups = r.xinfo_groups('taskiq_bench')
if groups:
    g = groups[0]
    print(f'  lag: {g.get(\"lag\", 0)}, pending: {g.get(\"pending\", 0)}')
"
