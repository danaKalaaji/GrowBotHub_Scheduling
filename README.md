## 🛰️ Project Overview – GrowBotHub Scheduling
This repository contains the work done as part of a semester project within **GrowBotHub**, an EPFL student association designing autonomous vertical farms for space exploration, particularly for future missions on the Moon. Our system is part of **IGLUNA: A Habitat in Ice**, where we will deploy and test a working prototype during the 2021 Field Campaign.

### 🎯 Focus of This Work: Scheduling

Our team was responsible for developing and optimizing the **scheduling algorithm** that dictates the movement of plants across a vertical aeroponic farm to:
- Maximize plant production over a given period.
- Ensure plants receive the right nutrients at the right time.
- Respect physical constraints like module capacity and plant size.
- Adapt to delays via **real-time rescheduling**.

We built on the work of the previous semester team, which used a **multi-commodity flow model** with the PuLP solver. We improved their algorithm, implemented new features requested by GrowBotHub, and handled dynamic updates during execution.

### 🤝 Part of a Larger System

Our scheduling system integrates with other subsystems developed in parallel by interdisciplinary teams:
- **Structure** – Designing the physical layout and movement mechanisms.
- **Aeroponics** – Managing water and nutrient delivery.
- **Robotics** – Programming the robotic arm and vision system.
- **Networking** – Facilitating communication between components and Earth control.
- **Chemical Engineering** – Designing nutrient solutions and handling waste.

📄 **More details and full results are available in the report:** `GrowBotHub.pdf`


## Project Structure

<details>
<summary>Click to expand the project structure</summary>
1node1moduleType - 5strawb/

Projet_Semestre.pdf
README.md
Scheduling_1node1bac - Raccourci.lnk
pycache/
classes.py
data.txt
edges.py
graph_construction_and_draw.py
inputs.py
main.py
optimization.py
outputs.py
plant_datas.txt
plants_array.py
1nodemodule - 5strawb/

Projet_Semestre.pdf
README.md
pycache/
classes.py
data.txt
edges.py
graph_construction_and_draw.py
inputs.py
main.py
optimization.py
outputs.py
plant_datas.txt
plants_array.py
scheduling/
classes.py
data.txt
input.py
main.py
output.txt
output2.txt
smalldata.txt
OptimalNbTrays/

Projet_Semestre.pdf
README.md
pycache/
classes.py
data.txt
edges.py
graph_construction_and_draw.py
inputs.py
main.py
optimization.py
outputs.py
plant_datas.txt
plants_array.py
total_plants_given_trays.py

</details>

## Key Features

- **Automated Scheduling**: Modules for scheduling plant growth stages efficiently.
- **Graph Construction and Visualization**: Tools for creating and visualizing growth graphs.
- **Optimization**: Algorithms for optimizing resource allocation and plant placement.

## Installation

To run this project, you'll need Python installed on your system. Follow these steps to get started:

1. Clone this repository:
   ```bash
   git clone https://github.com/danaKalaaji/GrowBotHub_Scheduling.git
Navigate into the desired module directory.
Navigate into the desired module directory.

Run the main script:
python main.py
Usage Examples
You can find example usage patterns in the main.py of each module. Simply modify the input parameters to suit your needs.
