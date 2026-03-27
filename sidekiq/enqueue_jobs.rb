require "redis"
require "json"
require "securerandom"

TOTAL_JOBS = Integer(ENV.fetch("TOTAL_JOBS", 200_000))
NUM_QUEUES = Integer(ENV.fetch("NUM_QUEUES", 10))

redis = Redis.new(url: "redis://localhost:6379")

start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)

TOTAL_JOBS.times do |i|
  queue = "queue_#{i % NUM_QUEUES}"
  job = {
    "class" => "LoadTestJob",
    "args" => [i],
    "queue" => queue,
    "jid" => SecureRandom.hex(12),
    "created_at" => Time.now.to_f,
    "enqueued_at" => Time.now.to_f,
    "retry" => false,
  }.to_json

  redis.lpush("queue:#{queue}", job)
  redis.sadd("queues", queue)
end

end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
puts "All jobs enqueued within: #{end_time - start_time} seconds"

# Memory stats
info = redis.info("memory")
puts "=== MEMORY AT PEAK (before consuming) ==="
puts "  used_memory_human:      #{info['used_memory_human']}"
puts "  used_memory_peak_human: #{info['used_memory_peak_human']}"
puts "  used_memory_rss_human:  #{info['used_memory_rss_human']}"
puts "=========================================="
