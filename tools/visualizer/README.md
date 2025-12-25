# Visualizer Tool

**Purpose:** Energy / trajectory plot

## Responsibility

- Visualize energy values
- Visualize trajectory evolution
- Plot energy over time
- Generate energy diagrams

## Features

### Energy Visualization
- Plot energy values (ΔEΨ, E_reflex, E_mind, etc.)
- Energy over time
- Energy distribution
- Energy heatmaps

### Trajectory Visualization
- Plot trajectory states
- Trajectory path in state space
- Trajectory evolution over time
- Trajectory comparison

### Energy Diagrams
- Energy flow diagrams
- Energy dependency graphs
- Energy component breakdown
- Energy phase diagrams

### Interactive Plots
- Zoom and pan
- Filter by time range
- Filter by energy type
- Export plots (PNG, SVG, PDF)

## Visualization Types

### Time Series
- Energy values over time
- State values over time
- Decision verdicts over time

### State Space
- Trajectory in state space
- Energy landscape
- Phase portraits

### Energy Flow
- Energy flow diagrams
- Energy dependency graphs
- Energy component breakdown

### Heatmaps
- Energy heatmaps
- State heatmaps
- Correlation heatmaps

## Usage

### Plot Energy
```bash
visualizer plot-energy --trace-id <trace_id> --output energy.png
```

### Plot Trajectory
```bash
visualizer plot-trajectory --trajectory-id <trajectory_id> --output trajectory.png
```

### Generate Energy Diagram
```bash
visualizer energy-diagram --trace-id <trace_id> --output diagram.svg
```

### Interactive Mode
```bash
visualizer interactive --trace-id <trace_id>
```

## Reference

- BASE-3: Formula Registry
- BASE-5: Event & Trace System
- COGMAN_CORE_KERNEL.md

