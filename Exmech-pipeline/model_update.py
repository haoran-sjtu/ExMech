import random
from datetime import datetime
import numpy as np
import pandas as pd
from MOAL import multi_objective_active_learning


def update_design():
    specimen = pd.read_excel('specimen.xlsx')
    specimen_mat = specimen.to_numpy()
    is_new_design = False
    for i in range(len(specimen_mat[:, 0])):
        if np.isnan(specimen_mat[i, 20]):  # Check if this row's parameters have been used
            print(f'Batch {i+1} data has not been iterated')
            mech_feature = specimen_mat[i, 10:20]
            if any(pd.isna(mech_feature)):  # Check if the mechanical features are complete
                print(f'Mechanical parameters for batch {specimen_mat[i, 0]} are incomplete')
            else:
                print(f'Mechanical parameters for batch {specimen_mat[i, 0]} are complete, proceeding with model update...')
                # Multi-objective active learning
                v1 = specimen_mat[i, 2]
                v2 = specimen_mat[i, 3]
                v3 = specimen_mat[i, 4]
                obj1 = specimen_mat[i, 16]
                obj2 = specimen_mat[i, 18]
                candidate = multi_objective_active_learning(v1, v2, v3, [obj1, obj2])
                print('Model updated')
                # Generate next batch parameters
                d1 = candidate(0)
                d2 = candidate(1)
                d3 = candidate(2)
                design = pd.read_excel('design.xlsx')
                design_mat = design.to_numpy()
                design_serial = int(design_mat[-1, 0]) + 1
                design_time = str(datetime.now())
                # Write and save
                design.loc[len(design)] = [design_serial, design_time, d1, d2, d3]  # Add new row
                design.to_excel('design.xlsx', index=False)
                print('Design parameters updated to design.xlsx')
                is_new_design = True
                # Set epoch to 1 in specimen.xlsx for this row
                specimen.iat[i, 20] = 1
                specimen.to_excel('specimen.xlsx', index=False)
        else:
            print(f'Batch {i+1} data has already been iterated')
            pass

    return is_new_design

if __name__ == '__main__':
    pass
