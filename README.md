# ExMech 
The **Self-evolving Experimental Mechanician ExMech** project aims to discover lightweight, high-strength lattice materials, combining a robotic platform for “can do” (9 workstations for standardized experimental data generation) and a multi-objective active learning framework for “can think” (guiding directional exploration through evolving structure-property understanding).
## Repository Contents
In this repository, the code required for the autonomous operation of ExMech, as well as the code for analyzing the research results, is stored. 
- The code for the control and communication of the robotic platform (including 9 workstations), as well as the complete pipeline and the optimization algorithm (multi-objective active learning) for the ExMech.
- The code for data analysis, such as the calculation of the non-dominated solution set and SHAP analysis, has also been provided along with test data.
- The code for parametric modeling of plate lattices, including two kinds of specimens.
## Requirements
- Python 3.7 
#### Main libraries for ExMech operation 
- pyrealsense2
- cv2
- pyautogui
- libpyauboi5
- subprocess
- transforms3d
- logging
- requests
- json
- socket
- serial
- binascii
- numpy
#### Main libraries for Multi-objective active learning
- botorch
- gpytorch
- sklearn
- pandas
- os
- numpy
#### Main libraries for parametric modeling
- abaqus
- caeModules
- driverUtils
- abaqusConstants
## Instruction Notes
- Ensure the input files are correctly formatted for the script to function properly.
- Ensure all necessary directories and files are present before running the script.
- Necessary example input (.xlsx) files are included in their respective directories.

