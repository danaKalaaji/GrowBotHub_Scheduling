# GrowBotHub Scheduling Algorithm

A comprehensive scheduling system for automated vertical farming in space environments, developed as part of the IGLUNA habitat project at EPFL.

## Project Overview

GrowBotHub is developing a fully automated vertical farming system for space exploration, particularly lunar habitats. This repository contains the scheduling algorithms that optimize plant movements across different growth modules to maximize harvest yield while respecting various constraints.

### Key Features

- **Multi-commodity flow optimization** for plant scheduling
- **Aeroponic system integration** with specialized nutrient modules
- **Diversity constraints** ensuring varied daily harvests
- **Plant size constraints** preventing overcrowding
- **Robotic arm instruction generation** for automated operations
- **Optimal module configuration** determination

## Repository Structure

### `1node1moduleType - 5strawb/`
**Optimized Version - Recommended for most use cases**

- Each graph node represents a **module type** (seedling, vegetative growth, flowering, development)
- Significantly reduced graph size: ~35x fewer edges compared to hole-based representation
- Fast execution time: ~2 minutes for 180-day scheduling
- Implements strawberry multiplication (5x) to account for multiple fruits per plant
- **Trade-off**: Less granular control over individual plant positions within modules

**Use when:**
- You need fast execution times
- Plant size constraints are not critical
- You're determining optimal module configurations

### `1nodemodule - 5strawb/`
**Detailed Version - For precise plant management**

- Each graph node represents an **individual module**
- Enables precise plant size constraint implementation
- Longer execution time: ~5.5 hours for 180-day scheduling
- Full control over plant placement and size management
- Implements strawberry multiplication (5x)

**Use when:**
- Plant size constraints are critical (lettuce, cabbage, fennel)
- You need precise control over plant placement
- Execution time is not a primary concern

### `OptimalNbTrays/`
Contains algorithms for determining the optimal number of modules of each type (seedling, vegetative growth, flowering, development) to maximize total harvest yield.

## Quick Start

### Prerequisites
- Python 3.x
- PuLP optimization library
- Input data files (module specifications, plant properties, growth times)

### Basic Usage

1. **Choose your implementation:**
  ```bash
  # For fast execution (recommended)
  cd "1node1moduleType - 5strawb"
  
  # For detailed plant management
  cd "1nodemodule - 5strawb"
