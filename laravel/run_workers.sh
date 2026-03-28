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

# Launch multiple worker processes (Laravel has no built-in concurrency flag)
for j in $(seq 1 "$NUM_WORKERS"); do
    php artisan queue:work redis --queue="$QUEUES" --sleep=0 --tries=0 --quiet &
done

php drain.php

# Kill all background workers
kill $(jobs -p) 2>/dev/null
wait 2>/dev/null || true

END=$(date +%s.%N)
echo "Total time: $(echo "$END - $START" | bc) seconds"

php -r "
\$r = new Redis();
\$r->connect('127.0.0.1', 6379);
\$total = 0;
for (\$i = 0; \$i < $NUM_QUEUES; \$i++) {
    \$len = \$r->lLen(\"laravel-database-queues:queue_\$i\");
    echo \"  queue_\$i: \$len messages\n\";
    \$total += \$len;
}
echo \"  Total remaining: \$total messages\n\";
"
