<?php

require __DIR__ . "/vendor/autoload.php";

$app = require_once __DIR__ . "/bootstrap/app.php";
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$totalJobs = (int) (getenv("TOTAL_JOBS") ?: 200000);
$numQueues = (int) (getenv("NUM_QUEUES") ?: 10);

$startTime = microtime(true);

for ($i = 0; $i < $totalJobs; $i++) {
    $queue = "queue_" . ($i % $numQueues);
    App\Jobs\LoadTestJob::dispatch($i)->onQueue($queue);
}

$endTime = microtime(true);
printf("All jobs enqueued within: %.2f seconds\n", $endTime - $startTime);

$redis = app("redis")->connection()->client();
$info = $redis->info("memory");
echo "=== MEMORY AT PEAK (before consuming) ===\n";
echo "  used_memory_human:      " . $info["used_memory_human"] . "\n";
echo "  used_memory_peak_human: " . $info["used_memory_peak_human"] . "\n";
echo "  used_memory_rss_human:  " . $info["used_memory_rss_human"] . "\n";
echo "==========================================\n";
