# Profiler Tool

**Purpose:** Performance profiling

## Responsibility

- Profile system performance
- Measure computation time
- Analyze resource usage
- Identify bottlenecks

## Features

### Performance Profiling
- Measure formula computation time
- Measure module execution time
- Measure end-to-end latency
- CPU usage profiling

### Resource Profiling
- Memory usage
- CPU usage
- I/O operations
- Network usage (if applicable)

### Bottleneck Analysis
- Identify slow formulas
- Identify slow modules
- Identify resource constraints
- Performance recommendations

### Benchmarking
- Run performance benchmarks
- Compare performance across versions
- Track performance over time
- Generate performance reports

## Profiling Metrics

### Formula Performance
- CORE-1 to CORE-9 computation time
- Formula dependency time
- Formula cache hit rate

### Module Performance
- Runtime module execution time
- Memory module access time
- Interface module latency

### System Performance
- End-to-end latency
- Throughput
- Resource utilization
- Error rate

## Usage

### Profile Trace
```bash
profiler profile-trace <trace_id> --output profile.json
```

### Profile Formula
```bash
profiler profile-formula CORE-1 --iterations 1000
```

### Profile Module
```bash
profiler profile-module perception --duration 60s
```

### Benchmark
```bash
profiler benchmark --scenarios scenarios.json --output benchmark.json
```

### Performance Report
```bash
profiler report --trace-id <trace_id> --output report.html
```

## Output Formats

- **JSON** - Machine-readable performance data
- **HTML** - Human-readable performance reports
- **CSV** - Time series performance data
- **Text** - Console-friendly performance summary

## Reference

- BASE-5: Event & Trace System
- BASE-4: Layer Responsibility Lock

