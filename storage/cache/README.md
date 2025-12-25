# Cache Storage

**Purpose:** Optional cache (redis / in-mem)

## Responsibility

- Cache frequently accessed data
- Improve performance
- Reduce storage I/O
- Optional caching layer

## Cache Types

### In-Memory Cache
- **Purpose:** Fast in-process cache
- **Format:** In-memory data structures
- **Access:** Fast read/write

### Redis Cache
- **Purpose:** Distributed cache
- **Format:** Redis key-value store
- **Access:** Network-based cache

### File Cache
- **Purpose:** Local file cache
- **Format:** Cached files
- **Access:** File-based cache

## Cacheable Data

### Trajectories
- Frequently accessed trajectories
- Recent trajectories
- Active trajectories

### Memory
- Frequently accessed memories
- Recent memories
- Strong memories

### Gate Decisions
- Recent decisions
- Decision patterns
- Decision statistics

### Runtime State
- Current system state
- Recent snapshots
- State checkpoints

## Operations

### Cache Get
- Get data from cache
- Check cache hit/miss
- Return cached data

### Cache Set
- Store data in cache
- Set cache expiration
- Update cache index

### Cache Invalidate
- Invalidate cache entry
- Clear cache
- Update cache index

## Configuration

### Cache Size
- Maximum cache size
- Cache eviction policy
- Cache replacement strategy

### Cache TTL
- Time-to-live for cache entries
- Cache expiration
- Cache refresh

## Reference

- BASE-5: Event & Trace System
- Performance optimization

