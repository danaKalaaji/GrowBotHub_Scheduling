# 1node1moduleType - 5strawb

##  Overview

**1node1moduleType - 5strawb** is a scheduling and optimization project focused on efficient cultivation using modular plant growth systems. It explores graph-based modeling and linear optimization to allocate resources (nodes and modules) over time to maximize plant yield within given constraints.

---

##  Directory Structure

```
1node1moduleType - 5strawb/
├── main.py                      # Entry point: runs the scheduling and optimization process
├── classes.py                   # Data structures and class definitions
├── edges.py                     # Graph edge management and constraint handling
├── graph_construction_and_draw.py  # Graph creation and visualization
├── inputs.py                    # Input data reading and preprocessing
├── optimization.py              # Core optimization logic using PuLP
├── outputs.py                   # Output formatting and writing
├── plants_array.py              # Manages internal plant data arrays
├── data.txt                     # Primary input configuration file
├── plant_datas.txt              # Detailed plant types and stage data
├── output.txt                   # Main output of the scheduling result
├── output2.txt                  # Additional output for comparisons
├── output_compare.txt           # Validation/comparison output
├── output_harvested.txt         # Records harvested plants and statistics
└── Projet_Semestre.pdf          # Report from previous contributors, describes the project state before current modifications

```

---

## Installation & Setup

### Prerequisites

- Python 3.x  
- [PuLP](https://coin-or.github.io/pulp/) (Python Linear Programming library)

Install PuLP with:

```bash
pip install pulp
```

---

### Clone the Repository

```bash
git clone https://github.com/danaKalaaji/scheduling_algo_flowNetworks_GrowBotHub.git
cd scheduling_algo_flowNetworks_GrowBotHub/1node1moduleType - 5strawb
```

### Ensure Required Files Are Present

The following files must be in the **same directory** as `main.py`:

- `data.txt`
- `plant_datas.txt`
- All relevant `.py` files listed above

---

##  Running the Program

Execute the program with:

```bash
python3 main.py
```

>  Make sure `data.txt` and `plant_datas.txt` are correctly formatted. Any deviation from the expected syntax will result in a crash.

---

## `data.txt` Format

This file defines the scheduling constraints and scenario parameters. Each line must follow the format:

```
KEYWORD|value1|value2|...
```

All indices are 0-based.

### Recognized Keywords

- **TRAYS**: Total number of trays  
  `TRAYS|5`

- **HOLES**: Number of holes per tray  
  `HOLES|10`

- **HORIZON**: Number of days to simulate  
  `HORIZON|20`

- **MAX_SIZE**: Distance constraints between hole pairs  
  `MAX_SIZE|distance:pair_indices;...`  
  Example:  
  `MAX_SIZE|15:0,1-3,4;14:0,2-1,2-3,2-4,2`

- **MAX_TIME**: Maximum runtime in minutes for optimization  
  `MAX_TIME|120`

- **PLANT**: Plant configuration  
  ```
  PLANT|name|total_days|color|sizes|tray_indexes|days_in_trays
  ```

  Example:
  ```
  PLANT|Strawberry|7|red|15,20,25|0,1|0,1;1,2
  ```

---

## Outputs

The program generates several output files:

- `output.txt`: Main results
- `output2.txt`: Alternative formatting or details
- `output_compare.txt`: Comparison metrics between runs
- `output_harvested.txt`: Breakdown of harvested plants

---
