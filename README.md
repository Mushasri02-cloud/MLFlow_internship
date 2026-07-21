# Decoupled Clinical Decision Support System: Diabetes Prediction MLOps Pipeline

An enterprise-grade, fully decoupled Machine Learning Operations (MLOps) system architecture that separates parameter configuration, experiment model tracking, binary version registries, and customer-facing inference web applications.

## 🏗️ System Architecture Flowchart
Dataset ──> Script Pipeline ──> MLflow Tracking (SQLite backend) ──> Versioned Model Registry ──> Streamlit UI Serve Client

## 📋 Project Overview
This repository implements a clinical support solution designed to assess patient diabetic probabilities based on key diagnostic attributes. Rather than compiling standard localized scripts, this layout structures production design patterns by integrating automated validation engines, model registration databases, and an interactive frontend dashboard.

## 🛠️ Technology Stack
* **Frontend Dashboard UI:** Streamlit Engine
* **Experiment Management Infrastructure:** MLflow Tracking Server Backend
* **Storage Component Matrix:** SQLite Embedded Database Engines
* **Machine Learning Toolkits:** Scikit-Learn Ecosystem
* **Core Languages:** Python 3.x

## 📊 Dataset Specifications
The pipeline utilizes the **PIMA Indians Diabetes Dataset**, consisting of medical metrics collected from female patients:
* Clinical Predictors: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age.
* Target Matrix: Diagnostic Outcome Classification binary flag (0 or 1).

## 🚀 Step-by-Step Execution Guide

### 1. Initialize the Central MLflow Experiment Server
Run this terminal string to wake up your database connection engine on port 5000:
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 127.0.0.1 --port 5000