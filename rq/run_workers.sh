#!/usr/bin/env bash
set -e

NUM_QUEUES="${NUM_QUEUES:-10}"
NUM_WORKERS="${NUM_WORKERS:-10}"

QUEUES=""
for i in $(seq 0 $((NUM_QUEUES - 1))); do
    QUEUES="$QUEUES queue_$i"
done

START=$(date +%s.%N)
rq worker-pool -q -n "$NUM_WORKERS" -b $QUEUES
END=$(date +%s.%N)
echo "Total time: $(echo "$END - $START" | bc) seconds"

python -c "
from redis import Redis
r = Redis()
total = 0
for i in range($NUM_QUEUES):
    length = r.llen(f'rq:queue:queue_{i}')
    print(f'  queue_{i}: {length} messages')
    total += length
print(f'  Total remaining: {total} messages')
"
