require "sidekiq"

Sidekiq.configure_server do |config|
  config.redis = { url: "redis://localhost:6379" }
end

class LoadTestJob
  include Sidekiq::Job
  sidekiq_options retry: false

  def perform(num)
  end
end
