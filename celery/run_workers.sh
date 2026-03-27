#!/usr/bin/env bash
set -e

NUM_QUEUES="${NUM_QUEUES:-10}"
NUM_WORKERS="${NUM_WORKERS:-10}"

QUEUES=""
for i in $(seq 0 $((NUM_QUEUES - 1))); do
    if [ -z "$QUEUES" ]; then
        QUEUES="queue_$i"
    else
        QUEUES="$QUEUES,queue_$i"
    fi
done

START=$(date +%s.%N)
celery -q --skip-checks -A tasks worker --loglevel=error -c "$NUM_WORKERS" -P threads -Q "$QUEUES" &
WORKER_PID=$!

python drain.py
wait "$WORKER_PID" 2>/dev/null || true
END=$(date +%s.%N)
echo "Total time: $(echo "$END - $START" | bc) seconds"

python -c "
from redis import Redis
r = Redis()
total = 0
for i in range($NUM_QUEUES):
    length = r.llen(f'queue_{i}')
    print(f'  queue_{i}: {length} messages')
    total += length
print(f'  Total remaining: {total} messages')
"
