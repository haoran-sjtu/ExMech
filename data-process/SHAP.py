import os
import time
import torch
import numpy
import pandas as pd
from botorch.models import SingleTaskGP, ModelListGP
from botorch.fit import fit_gpytorch_model
from botorch.acquisition.multi_objective import ExpectedHypervolumeImprovement
from botorch.utils.multi_objective.box_decompositions.non_dominated import NondominatedPartitioning
from botorch.optim import optimize_acqf
from gpytorch.mlls import ExactMarginalLogLikelihood
import shap
import numpy as np

# Define global variables
train_x = None
train_obj = None
std_train_obj = None
model = None

# Training data file path
data_file = 'shap_dataset.xlsx'

# Load saved training data and model if available
if os.path.exists(data_file):
    df = pd.read_excel(data_file)
    train_x = torch.tensor(df[['var1', 'var2', 'var3']].values, dtype=torch.double)
    train_obj = torch.tensor(df[['obj1', 'obj2', 'obj3']].values, dtype=torch.double)

def train_models(train_x, train_obj):
    models = []
    for i in range(train_obj.shape[1]):
        gp = SingleTaskGP(train_x, train_obj[:, i].unsqueeze(-1))
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        fit_gpytorch_model(mll)
        models.append(gp)
    model = ModelListGP(*models)
    return model

def multi_objective_bayesian_optimization_step(prev_observation=None, var1=None, var2=None, var3=None):
    global train_x, train_obj, model, std_train_obj

    if prev_observation is not None:
        if train_x is None or train_obj is None:
            train_x = torch.empty((0, 3), dtype=torch.double)
            train_obj = torch.empty((0, 3), dtype=torch.double)
        new_x = torch.tensor([[var1, var2, var3]], dtype=torch.double)
        print(f"Append new_x: {new_x}")
        if len(new_x.shape) == 1:
            new_x = new_x.unsqueeze(0)
        train_x = torch.cat([train_x, new_x])
        print(f"Appended {new_x[0]} with observation {prev_observation} to dataset")
        new_obj = torch.tensor([prev_observation], dtype=torch.double)
        train_obj = torch.cat([train_obj, new_obj])

    std_train_obj = train_obj

    model = train_models(train_x, std_train_obj)
    ref_point = torch.tensor([0, 0, 0], dtype=torch.double)
    partitioning = NondominatedPartitioning(ref_point=ref_point, Y=std_train_obj)
    ehvi = ExpectedHypervolumeImprovement(
        model=model,
        ref_point=ref_point.tolist(),
        partitioning=partitioning,
    )
    bounds = torch.tensor([[0.2, 0.05, 0.1], [1.3, 0.7, 2]], dtype=torch.double)
    candidate, acq_values = optimize_acqf(
        acq_function=ehvi,
        bounds=bounds,
        q=30,
        num_restarts=5,
        raw_samples=10,
        sequential=True
    )
    return candidate, model

def load_model_and_predict(sample_points, model):
    model.eval()
    with torch.no_grad():
        sample_points_tensor = torch.tensor(sample_points, dtype=torch.double)
        predictions = []
        for i, gp in enumerate(model.models):
            pred = gp.posterior(sample_points_tensor).mean
            predictions.append(pred)
        return torch.cat(predictions, dim=-1)

def shap_analysis(model, train_x):
    shap_3obj = []
    for i, gp_model in enumerate(model.models):
        print(f"Analyzing SHAP values for Objective {i + 1}")
        def model_predict(X):
            X_tensor = torch.tensor(X, dtype=torch.double)
            with torch.no_grad():
                return gp_model.posterior(X_tensor).mean.numpy()
        # Choose all data as background
        background_data = train_x.numpy()
        explainer = shap.KernelExplainer(model_predict, background_data)
        shap_values = explainer.shap_values(train_x.numpy())
        abs_values = np.abs(shap_values)
        feature_shap_values = np.mean(abs_values[0], axis=0)  # 1*3
        shap_3obj.append(feature_shap_values)
    shap_3obj = np.array(shap_3obj)
    return shap_3obj


# Calculate SHAP changes from iteration 1-58
def update_training_and_shap():
    all_shap_values_matrices = []
    for num_samples in range(1, 59):
        # Get the first num_samples samples
        current_train_x = train_x[:num_samples]
        current_train_obj = train_obj[:num_samples]
        model = train_models(current_train_x, current_train_obj)
        # Perform SHAP analysis and get the contribution of each feature for the current training set
        shap_values_matrix = shap_analysis(model, current_train_x)
        # Combine SHAP value matrix
        all_shap_values_matrices.append(shap_values_matrix)
        print(f"Feature SHAP values after adding {num_samples} sample(s): {shap_values_matrix[-1]}")
    all_shap_values_matrices = np.array(all_shap_values_matrices)
    return all_shap_values_matrices
