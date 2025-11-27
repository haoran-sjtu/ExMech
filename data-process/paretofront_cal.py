# Calculate the non-dominated solution as the Pareto front
import torch
import pandas as pd
from botorch.utils.multi_objective.pareto import is_non_dominated

def pareto_calculate():
    data_file = "samples.xlsx"
    # Saved training data and models, load them
    df = pd.read_excel(data_file)
    train_obj = torch.tensor(df[['obj1', 'obj2', 'obj3']].values, dtype=torch.double)
    serial = df[['Serial']].values
    std_train_obj = train_obj
    pareto_mask = is_non_dominated(std_train_obj)
    # Obtain the index of the non-dominated solution in the original training set
    pareto_indices = torch.where(pareto_mask)[0]
    pareto_serial = serial[pareto_indices]
    pareto_serial = pareto_serial.flatten().tolist()
    print(f'non_dominated serials are {pareto_indices.numpy()}')
    print(f'non_dominated serials are {pareto_serial}')
    df = pd.DataFrame(pareto_serial)
    df.to_clipboard(index=False, header=False)

if __name__ == '__main__':
    pareto_calculate()


