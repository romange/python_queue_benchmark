# Sidekiq Benchmark

## Prerequisites

```bash
sudo apt update && sudo apt install -y ruby ruby-dev ruby-bundler
```

Then install gems:

```bash
cd sidekiq
bundle install
```

## Usage

1. Enqueue jobs:
   ```bash
   ruby enqueue_jobs.rb
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
| `NUM_WORKERS` | `10` | Sidekiq concurrency (threads) |
| `POLL_INTERVAL` | `2` | Drain poll interval in seconds |
