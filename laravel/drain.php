<?php

$numQueues = (int) (getenv("NUM_QUEUES") ?: 10);
$pollInterval = (int) (getenv("POLL_INTERVAL") ?: 2);

$redis = new Redis();
$redis->connect("127.0.0.1", 6379);

$queueKeys = [];
for ($i = 0; $i < $numQueues; $i++) {
    $queueKeys[] = "laravel-database-queues:queue_" . $i;
}

// Wait for queues to have jobs before starting to monitor
sleep(3);

$checks = 0;
while (true) {
    $total = 0;
    foreach ($queueKeys as $key) {
        $total += $redis->lLen($key);
    }
    echo "Remaining: $total\n";
    if ($total === 0 && $checks > 0) {
        echo "All queues empty. Shutting down...\n";
        break;
    }
    $checks++;
    sleep($pollInterval);
}
