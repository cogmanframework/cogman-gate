# Logs and Metrics Storage

**Purpose:** Documentation for logs and metrics storage

---

## Storage Locations

### Execution Logs
- **Path:** `storage/audit/execution_logs/`
- **Format:** JSON files (`{trace_id}.json`)
- **Content:** Execution logs with trajectory, action output, phase results

### Audit Trails
- **Path:** `storage/audit/trace_map/`
- **Format:** JSON files (`{trace_id}.json`)
- **Content:** Complete audit trail with lineage information

### Metrics
- **Path:** `storage/runtime/metrics/`
- **Format:** JSON files (`{trace_id}.json`)
- **Content:** Execution metrics (execution time, phase times, gate verdict, etc.)

---

## Usage

### View Logs

```bash
# List all logs
python3 tools/log_metrics_tool.py log list

# Get specific log
python3 tools/log_metrics_tool.py log get {trace_id}

# Query logs
python3 tools/log_metrics_tool.py log query --action-type text --success true
```

### View Metrics

```bash
# List all metrics
python3 tools/log_metrics_tool.py metrics list

# Get specific metrics
python3 tools/log_metrics_tool.py metrics get {trace_id}

# Show statistics
python3 tools/log_metrics_tool.py metrics stats

# Query metrics
python3 tools/log_metrics_tool.py metrics query --gate-verdict ALLOW --action-type text
```

### Python API

```python
from storage import LogViewer, MetricsViewer

# View logs
log_viewer = LogViewer()
logs = log_viewer.list_logs(limit=10)
log = log_viewer.get_log("trace_001")

# View metrics
metrics_viewer = MetricsViewer()
metrics = metrics_viewer.list_metrics(limit=10)
metric = metrics_viewer.get_metrics("trace_001")
stats = metrics_viewer.get_statistics()
```

---

## File Formats

### Execution Log Format

```json
{
  "trace_id": "abc123",
  "timestamp": 1234567890.0,
  "trajectory": {
    "trace_id": "abc123",
    "state_count": 3
  },
  "action_output": {
    "action_type": "text",
    "success": true,
    "trace_id": "abc123"
  },
  "phase_results": {
    "phase_times": {...},
    "gate_verdict": "ALLOW",
    "transformations": [...]
  }
}
```

### Metrics Format

```json
{
  "trace_id": "abc123",
  "execution_time": 0.123,
  "phase_times": {
    "perception": 0.01,
    "gate": 0.02,
    "wm_controller": 0.03,
    "reasoning": 0.02,
    "decision": 0.01,
    "action": 0.01
  },
  "gate_verdict": "ALLOW",
  "action_type": "text",
  "success": true,
  "timestamp": 1234567890.0
}
```

---

## Status

**Current Status:** Logs and metrics are created automatically by PostProcessor (PHASE 9)

**Storage:** Files are created when Runtime Loop executes PHASE 9

**Viewing:** Use `tools/log_metrics_tool.py` to view logs and metrics

