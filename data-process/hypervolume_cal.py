# Read the training data and calculate the gradual increase of HV
import torch
import pandas as pd
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated


def hv_calculate():
    data_file = "samples.xlsx"
    df = pd.read_excel(data_file)
    train_obj = torch.tensor(df[['obj1', 'obj2', 'obj3']].values, dtype=torch.double)
    std_train_obj = torch.empty((0, train_obj.size(1)), dtype=torch.double)
    ref_point = torch.tensor([-1, -1, -1], dtype=torch.double)
    hypervolume_list = []
    for i in range(train_obj.size(0)):
        std_train_obj = torch.vstack((std_train_obj, train_obj[i].unsqueeze(0)))
        pareto_mask = is_non_dominated(std_train_obj)
        pareto_front = std_train_obj[pareto_mask]
        Hv = Hypervolume(ref_point=ref_point)
        hypervolume = Hv.compute(pareto_front)
        print(f"Step {i + 1}, Hypervolume: {hypervolume}")
        hypervolume_list.append(hypervolume)

    df['HV'] = hypervolume_list
    df.to_excel(data_file, index=False)


if __name__ == '__main__':
    # Step-by-step calculation of HV
    hv_calculate()



