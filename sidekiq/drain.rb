require "redis"

poll_interval = Integer(ENV.fetch("POLL_INTERVAL", 2))
num_queues = Integer(ENV.fetch("NUM_QUEUES", 10))
worker_pid = Integer(ARGV[0])

redis = Redis.new

queue_keys = (0...num_queues).map { |i| "queue:queue_#{i}" }

loop do
  total = queue_keys.sum { |k| redis.llen(k) }
  if total == 0
    puts "All queues empty. Shutting down..."
    Process.kill("TERM", worker_pid)
    break
  end
  sleep poll_interval
end
