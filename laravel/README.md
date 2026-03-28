# Laravel Queue Benchmark

## Prerequisites

Install PHP, Composer, and the Redis extension:

```bash
sudo apt update && sudo apt install -y php php-cli php-redis php-mbstring php-xml composer
```

## Setup

Run the setup script to create a minimal Laravel app:

```bash
cd laravel
./setup.sh
```

Then copy the benchmark scripts into the Laravel app:

```bash
cp enqueue_jobs.php drain.php run_workers.sh app/
cd app
```

## Usage

1. Enqueue jobs:
   ```bash
   php enqueue_jobs.php
   ```

2. Process jobs:
   ```bash
   NUM_QUEUES=10 NUM_WORKERS=10 ./run_workers.sh
   ```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TOTAL_JOBS` | `200000` | Total number of jobs to enqueue |
| `NUM_QUEUES` | `10` | Number of queues |
| `NUM_WORKERS` | `10` | Number of worker processes |
| `POLL_INTERVAL` | `2` | Drain poll interval in seconds |

## Notes

- Laravel has no built-in worker concurrency flag. The script launches multiple `queue:work` processes.
- Each `queue:work` process is single-threaded (PHP limitation).
- The `--sleep=0` flag disables polling delay for maximum throughput.
