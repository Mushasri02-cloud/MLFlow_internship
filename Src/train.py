import os
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import mlflow
import mlflow.sklearn

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def prepare_data(data_path, target_column):
    df = pd.read_csv(data_path)
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_log_model(X_train, X_test, y_train, y_test, model, model_name, tracking_uri, experiment_name):
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Calculate all required metrics
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1_score": f1_score(y_test, predictions, zero_division=0)
        }
        
        print(f"\n--- {model_name} Performance ---")
        for k, v in metrics.items():
            print(f"{k.capitalize()}: {v:.4f}")
            mlflow.log_metric(k, v)
            
        mlflow.log_params(model.get_params())
        
        # Log Feature Importance Chart
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            feature_names = X_train.columns
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(8, 5))
            sns.barplot(x=importances[indices], y=feature_names[indices], palette="viridis")
            plt.title(f"{model_name} Feature Importances")
            plt.xlabel("Importance Score")
            feat_img_path = f"{model_name}_feature_importance.png"
            plt.tight_layout()
            plt.savefig(feat_img_path)
            plt.close()
            mlflow.log_artifact(feat_img_path)
            if os.path.exists(feat_img_path):
                os.remove(feat_img_path)
        
        # Log Confusion Matrix
        cm = confusion_matrix(y_test, predictions)
        fig, ax = plt.subplots(figsize=(5, 5))
        ConfusionMatrixDisplay(confusion_matrix=cm).plot(ax=ax, cmap="Blues")
        plt.title(f"{model_name} Confusion Matrix")
        plot_path = f"{model_name}_confusion_matrix.png"
        plt.savefig(plot_path)
        plt.close()
        mlflow.log_artifact(plot_path)
        if os.path.exists(plot_path):
            os.remove(plot_path)
            
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=model_name)

def run_pipeline():
    config = load_config()
    ml_cfg = config["mlflow_config"]
    model_configs = config["model_params"]
    X_train, X_test, y_train, y_test = prepare_data(config["data"]["path"], config["data"]["target"])
    
    train_and_log_model(X_train, X_test, y_train, y_test, 
                        LogisticRegression(**model_configs["logistic_regression"]), 
                        "Logistic_Regression", ml_cfg["tracking_uri"], ml_cfg["experiment_name"])
    
    train_and_log_model(X_train, X_test, y_train, y_test, 
                        RandomForestClassifier(**model_configs["random_forest"]), 
                        "Random_Forest", ml_cfg["tracking_uri"], ml_cfg["experiment_name"])

if __name__ == "__main__":
    run_pipeline()