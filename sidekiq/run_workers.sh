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
bundle exec sidekiq -r ./worker.rb -c "$NUM_WORKERS" -q "$QUEUES" &
WORKER_PID=$!

ruby drain.rb "$WORKER_PID"
wait "$WORKER_PID" 2>/dev/null || true
END=$(date +%s.%N)
echo "Total time: $(echo "$END - $START" | bc) seconds"

ruby -e "
require 'redis'
r = Redis.new
total = 0
${NUM_QUEUES}.times do |i|
  length = r.llen(\"queue:queue_#{i}\")
  puts \"  queue_#{i}: #{length} messages\"
  total += length
end
puts \"  Total remaining: #{total} messages\"
"
