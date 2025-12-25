# Cogman CLI

Control & Operations CLI for Cogman Energetic Engine.

## Structure

```
cog_cli/
├── main.py               # Entry point
├── commands/             # Subcommands (NO LOGIC)
│   ├── energy.py         # Inspect EPS-8 / CORE formulas
│   ├── gate.py           # Test Decision Gate
│   ├── trace.py          # View execution traces
│   ├── replay.py         # Replay trajectory from logs
│   ├── memory.py         # Inspect memory fields (read-only)
│   └── config.py         # Validate config / policy
├── adapters/             # CLI ↔ system bridge
│   ├── kernel_adapter.py
│   ├── gate_adapter.py
│   └── memory_adapter.py
├── output/               # Formatting only
│   ├── table.py
│   ├── json.py
│   └── pretty.py
└── safety.py             # Hard CLI-level safety checks
```

## Usage

```bash
# Run CLI
python -m cog_cli.main <command> [options]

# Examples
python -m cog_cli.main energy compute --formula CORE-1 --I 0.8 --P 0.6 --S_a 0.7 --H 0.3
python -m cog_cli.main gate test --context robot_control --E_mu 50.0 --H 0.2
python -m cog_cli.main trace view --trace-id abc123
python -m cog_cli.main memory inspect --field episodic
python -m cog_cli.main config validate --file gate_profiles.yaml
```

## Commands

### Energy

Inspect EPS-8 / CORE formulas.

```bash
cogman energy compute --formula CORE-1 --I 0.8 --P 0.6 --S_a 0.7 --H 0.3
cogman energy project --I 0.8 --P 0.6 --S 0.7 --H 0.3 --A 0.5
cogman energy validate --I 0.8 --P 0.6 --S 0.7 --H 0.3
```

### Gate

Test Decision Gate (ALLOW/REVIEW/BLOCK).

```bash
cogman gate test --context robot_control --E_mu 50.0 --H 0.2 --D 0.1
cogman gate validate --policy-file config/gate_profiles.yaml
```

### Trace

View execution traces.

```bash
cogman trace view --trace-id abc123
cogman trace list --limit 10
cogman trace search --filter "verdict=BLOCK"
```

### Replay

Replay trajectory from logs.

```bash
cogman replay --log-file storage/trajectory/raw/traj_001.log
```

### Memory

Inspect memory fields (read-only).

```bash
cogman memory inspect --field episodic
cogman memory list
cogman memory stats --field semantic
```

### Config

Validate config / policy.

```bash
cogman config validate --file config/gate_profiles.yaml
cogman config show --file config/gate_profiles.yaml
```

## Output Formats

- `pretty` (default): Human-readable format
- `table`: Table format (requires `tabulate`)
- `json`: JSON format

```bash
cogman energy compute --formula CORE-1 --I 0.8 --output-format json
```

## Safety Checks

The CLI runs safety checks before any operations:

- Python version check
- Required modules check
- Kernel availability check
- File permissions check

## Dependencies

- Python 3.7+
- `tabulate` (optional, for table output)
- `PyYAML` (optional, for YAML config support)

## Installation

```bash
# Install dependencies
pip install tabulate pyyaml

# Make CLI executable (optional)
chmod +x cog_cli/main.py
```

