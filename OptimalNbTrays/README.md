# OptimalNbTrays

**OptimalNbTrays** optimally allocates trays for plant growth under various constraints. It uses graph modeling and optimization techniques (via the [PuLP](https://coin-or.github.io/pulp/) linear programming package) to determine the most efficient configuration for growing plants.

---

## Directory Structure

```
OptimalNbTrays/
├── classes.py                    # Core classes like Node and Plant
├── edges.py                     # Relationships and constraints between graph nodes
├── graph_construction_and_draw.py  # Graph construction and visualization
├── inputs.py                    # Input parsing and validation (from data.txt)
├── optimization.py              # Main optimization logic using PuLP
├── outputs.py                   # Output formatting and result display
├── plants_array.py              # Handles plant data structures
├── data.txt                     # Input configuration file (see format below)
└── main.py                      # Entry point for running the program
```

---

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/danaKalaaji/scheduling_algo_flowNetworks_GrowBotHub.git
cd scheduling_algo_flowNetworks_GrowBotHub/OptimalNbTrays
```

### 2. Install Dependencies
Ensure you have Python 3 installed. Then install the required package:

```bash
pip install pulp
```

---

##  Running the Program

Execute the main script:

```bash
python3 main.py
```

 **Note:** Ensure all the `.py` files and `data.txt` are in the same directory as `main.py`.

---

##  `data.txt` File Format

This file contains configuration data and must strictly follow the expected format. Any errors in this file will cause the program to crash.

###  General Format

Each line follows the structure:  
`KEYWORD|value1|value2|...`

All indices are **0-based**.

###  Keywords and Examples

- **TRAYS**: Total number of trays to allocate  
  `TRAYS|5`

- **HOLES**: Number of holes per tray  
  `HOLES|10`

- **HORIZON**: Planning time horizon (in days)  
  `HORIZON|30`

- **MAX_SIZE**: Maximum distances between hole pairs to be respected  
  `MAX_SIZE|max_distance:hole_index_pairs;...`  
  Example:  
  `MAX_SIZE|15:0,1-3,4;14:0,2-1,2-3,2-4,2`

- **MAX_TIME**: Max optimization time in minutes  
  `MAX_TIME|5`

- **PLANT**: Plant data and growth cycle constraints  
  `PLANT|name|total_days|color|sizes|tray_indexes|days_in_trays`

  Example:
  ```
  PLANT|Tomato|5|red|10,20,30,40,50|0,1,2|0,1;1,2;2,3
  ```

---

## Error Handling

- Make sure each line strictly follows the expected format.
- A single formatting error in `data.txt` can result in a crash.
- All keywords must be in uppercase and spelled exactly as shown.

---

## How It Works

- The program reads `data.txt` to understand the planting schedule and constraints.
- It builds a graph model with nodes representing plant states and edges representing transitions.
- An optimization algorithm determines the optimal use of trays to grow the maximum number of plants over the given horizon.

---

