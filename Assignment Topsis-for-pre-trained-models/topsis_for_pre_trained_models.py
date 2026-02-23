from datasets import load_dataset
import time
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score

dataset = load_dataset("SetFit/sst2")
test_data = dataset["test"]

TEXT_COL = "text"
LABEL_COL = "label"

MAX_SAMPLES = 200

def evaluate_model(model_name, dataset):
    """
    Evaluates a pretrained Hugging Face text classification model
    and returns Accuracy, F1-score, Inference Time, and Model Size.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=False
    )
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    texts = dataset[TEXT_COL][:MAX_SAMPLES]
    labels = dataset[LABEL_COL][:MAX_SAMPLES]

    predictions = []
    start_time = time.time()

    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True
            )
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            predictions.append(pred)

    end_time = time.time()

    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions)
    inference_time = end_time - start_time
    model_size = sum(p.numel() for p in model.parameters()) / 1e6  # MB approx

    return accuracy, f1, inference_time, model_size

models = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "bert-base-uncased",
    "roberta-base",
    "albert-base-v2",
    "xlnet-base-cased"
]

results = []

for model in models:
    print(f"Evaluating: {model}")
    acc, f1, time_taken, size = evaluate_model(model, test_data)
    results.append([model, acc, f1, time_taken, size])

df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy", "F1 Score", "Inference Time", "Model Size (MB)"]
)

decision_matrix = df[["Accuracy", "F1 Score", "Inference Time", "Model Size (MB)"]].values

def topsis(matrix, weights, impacts):
    #
    norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    weighted_matrix = norm_matrix * weights

    ideal_best = np.zeros(matrix.shape[1])
    ideal_worst = np.zeros(matrix.shape[1])

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best[i] = weighted_matrix[:, i].max()
            ideal_worst[i] = weighted_matrix[:, i].min()
        else:
            ideal_best[i] = weighted_matrix[:, i].min()
            ideal_worst[i] = weighted_matrix[:, i].max()

    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    scores = dist_worst / (dist_best + dist_worst)
    return scores

weights = np.array([0.25, 0.25, 0.25, 0.25])
impacts = ["+", "+", "-", "-"]

df["TOPSIS Score"] = topsis(decision_matrix, weights, impacts)
df["Rank"] = df["TOPSIS Score"].rank(ascending=False)

df = df.sort_values("Rank")
print(df)

df.to_csv("topsis_model_ranking.csv", index=False)
