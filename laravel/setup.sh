#!/usr/bin/env bash
set -e

# Create a minimal Laravel app
composer create-project laravel/laravel app --prefer-dist --no-interaction
cd app

# Install phpredis (predis is slower)
# phpredis should already be available as a PHP extension

# Configure Redis as queue and cache driver
sed -i 's/QUEUE_CONNECTION=.*/QUEUE_CONNECTION=redis/' .env
sed -i 's/CACHE_STORE=.*/CACHE_STORE=redis/' .env
sed -i 's/REDIS_HOST=.*/REDIS_HOST=127.0.0.1/' .env

# Create the job class
php artisan make:job LoadTestJob

# Replace the job with a no-op
cat > app/Jobs/LoadTestJob.php << 'JOBEOF'
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class LoadTestJob implements ShouldQueue
{
    use Queueable;

    public int $num;
    public $tries = 0;

    public function __construct(int $num)
    {
        $this->num = $num;
    }

    public function handle(): void
    {
    }
}
JOBEOF

echo "Setup complete. Copy enqueue_jobs.php and other scripts into app/."
