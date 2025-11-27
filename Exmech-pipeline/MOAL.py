import os
import torch
import pandas as pd
from botorch.models import SingleTaskGP, ModelListGP
from botorch.fit import fit_gpytorch_model
from botorch.acquisition.multi_objective import ExpectedHypervolumeImprovement
from botorch.utils.multi_objective.box_decompositions.non_dominated import NondominatedPartitioning
from botorch.optim import optimize_acqf
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from gpytorch.mlls import ExactMarginalLogLikelihood
from sklearn.preprocessing import MinMaxScaler

# Define global variables
train_x = None
train_obj = None
std_train_obj = None
model = None

def train_models(train_x, train_obj):
    models = []
    for i in range(train_obj.shape[1]):
        # Create separate GPR models for each objective function
        gp = SingleTaskGP(train_x, train_obj[:, i].unsqueeze(-1))
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        fit_gpytorch_model(mll)
        gp.likelihood.noise_covar.noise = torch.tensor(1e-3)
        models.append(gp)
    # Combine all models using ModelListGP
    model = ModelListGP(*models)

    return model

def multi_objective_active_learning(prev_observation=None,var1=None, var2=None, var3=None):
    global train_x, train_obj, model, std_train_obj

    # Read training data
    data_file = "train_process_data.xlsx"
    if os.path.exists(data_file):
        df = pd.read_excel(data_file)
        train_x = torch.tensor(df[['var1', 'var2', 'var3']].values, dtype=torch.double)
        train_obj = torch.tensor(df[['obj1', 'obj2', 'obj3']].values, dtype=torch.double)

    if prev_observation is not None:
        # Initialize training data
        if train_x is None or train_obj is None:
            train_x = torch.empty((0, 3), dtype=torch.double)
            train_obj = torch.empty((0, 3), dtype=torch.double)

        new_x = torch.tensor([[var1, var2, var3]], dtype=torch.double)
        if len(new_x.shape) == 1:
            new_x = new_x.unsqueeze(0)
        train_x = torch.cat([train_x, new_x])
        # Add the previous suggestion sampling point and observation
        print(f"Appended {new_x[0]} with observation {prev_observation} to dataset")
        new_obj = torch.tensor([prev_observation], dtype=torch.double)
        train_obj = torch.cat([train_obj, new_obj])


    scaler = MinMaxScaler()
    scaler.fit(train_obj)
    std_train_obj = scaler.transform(train_obj)

    print(std_train_obj)
    prediction = None
    if prev_observation is not None:
        sample_points = [var1, var2, var3]
        prediction = load_model_and_predict([sample_points], model)

    model = train_models(train_x, std_train_obj)
    ref_point = torch.tensor([0, 0, 0], dtype=torch.double)
    partitioning = NondominatedPartitioning( ref_point=ref_point, Y=std_train_obj)
    ehvi = ExpectedHypervolumeImprovement(
        model=model,
        ref_point=ref_point.tolist(),
        partitioning=partitioning,
    )
    bounds = torch.tensor([[0.2, 0.05, 0.1], [1.3, 0.7, 2]], dtype=torch.double)
    candidates, acq_values = optimize_acqf(
        acq_function=ehvi,
        bounds=bounds,
        q=30,
        num_restarts=5,
        raw_samples=10,
        sequential=True
    )
    acq_values_sorted, sorted_indices = torch.sort(acq_values, descending=True)  # Sort by acq_values

    epsilon = 0.1
    if torch.rand(1).item() <= epsilon:
        candidates_in_pre = candidates[sorted_indices[3:]]
        chosen_index = torch.randint(0, candidates_in_pre.size(0), (1,)).item()
        print(f'rand_choose BAD serial {chosen_index}')
        candidate_point = candidates_in_pre[chosen_index]
    else:
        candidates_in_pre = candidates[sorted_indices[:3]]
        chosen_index = torch.randint(0, candidates_in_pre.size(0), (1,)).item()
        print(f'rand_choose serial {chosen_index}')
        candidate_point = candidates_in_pre[chosen_index]

    # Compute current hypervolume
    pareto_mask = is_non_dominated(std_train_obj)
    pareto_front = std_train_obj[pareto_mask]
    Hv = Hypervolume(ref_point=ref_point)
    hypervolume = Hv.compute(pareto_front)

    # Return the suggested new sampling point
    return candidate_point, prediction, hypervolume

def load_model_and_predict(sample_points, model):
    """
    :param sample_points: list--[var1, var2, var3]
    :param model:
    :return:
    """
    model.eval()
    with torch.no_grad():
        sample_points_tensor = torch.tensor(sample_points, dtype=torch.double)
        # Predict for each model
        predictions = []
        for gp in model.models:
            pred = gp.posterior(sample_points_tensor).mean
            predictions.append(pred)
        return torch.cat(predictions, dim=-1)

if __name__ == '__main__':
    pass
