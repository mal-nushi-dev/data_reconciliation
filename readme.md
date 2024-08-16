# Data Reconciliation
Welcome to my data reconciliation project. This repository contains scripts and resources designed for reconciling data between a source and target dataset. The goal is to ensure data integrity by identifying discrepancies, automating recon processes, and generating a report of the results.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Directory Structure](#directory-structure)

## Overview
My Data Reconciliation project provides a framework to validate and reconcile data from a source and target dataset. It is especially useful in environments where data consistency between various systems is critical. This project supports customizable reconciliation rules, detailed reporting, and automation of the reconciliation process.

## Features
- **Customizable Reconciliation Rules**: Define custom rules to compare data between source and target datasets.
- **Detailed Reporting**: Generate a detailed report of the reconciliation process, including discrepancies.
- **Automated Reconciliation Process**: Run the reconciliation process automatically using the provided scripts.

## Setup
### Prerequesites
Before you begin, ensure you meet the following requirements:
- You have installed Python 3.8 or higher.
- pip (Python package installer)
- Virtualenv (optional but recommended)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/mal-nushi-dev/data_reconciliation.git
    cd data_reconciliation
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To start using the Data Reconciliation project, follow these steps:
1. Configure the reconciliation rules in the `config.ini` file.
2. Run the main reconciliation script:
    ```bash
    python main.py
    ```
