def _print_stats(info):
    print("=== MEMORY AT PEAK (before consuming) ===")
    print(f"  used_memory_human:      {info['used_memory_human']}")
    print(f"  used_memory_peak_human: {info['used_memory_peak_human']}")
    print(f"  used_memory_rss_human:  {info['used_memory_rss_human']}")
    print("==========================================")


def print_memory_stats(redis_conn=None):
    """Print Redis memory stats using a synchronous connection."""
    import redis as redis_sync
    if redis_conn is None:
        redis_conn = redis_sync.Redis()
    info = redis_conn.info("memory")
    _print_stats(info)


async def print_memory_stats_async(redis_conn=None):
    """Print Redis memory stats using an async connection."""
    if redis_conn is None:
        import redis.asyncio as aioredis
        redis_conn = aioredis.Redis()
        info = await redis_conn.info("memory")
        await redis_conn.aclose()
    else:
        info = await redis_conn.info("memory")
    _print_stats(info)
