# Phase 1: Project Structure and Configuration
# Creating project structure and configuration files

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Project configuration
PROJECT_CONFIG = {
    'project_name': 'Vaccination_Data_Analysis',
    'data_path': 'data/',
    'cleaned_data_path': 'data/cleaned/',
    'processed_data_path': 'data/processed/',
    'output_path': 'output/',
    'sql_scripts_path': 'sql_scripts/',
    'notebooks_path': 'notebooks/',
    'reports_path': 'reports/'
}

# Create directory structure
def create_project_structure():
    """Create comprehensive project directory structure"""
    directories = [
        'data/raw',
        'data/cleaned', 
        'data/processed',
        'data/external',
        'sql_scripts',
        'notebooks/exploration',
        'notebooks/analysis',
        'src/data_processing',
        'src/analysis',
        'src/visualization',
        'output/reports',
        'output/charts',
        'output/exports',
        'config',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

create_project_structure()

# Create configuration file
config_content = """
# Global Vaccination Data Analysis Project Configuration

## Data Sources
- WHO/UNICEF Estimates of National Immunization Coverage (WUENIC)
- WHO Immunization Data Portal
- Disease incidence and surveillance data

## Key Metrics
- Global vaccination coverage rates
- Disease incidence trends
- Vaccine effectiveness indicators
- Regional performance comparisons

## Target Deliverables
1. Clean SQL database with normalized schema
2. Interactive Power BI dashboards
3. Comprehensive analytical reports
4. Predictive models for coverage forecasting
"""

with open('config/project_config.md', 'w') as f:
    f.write(config_content)

print("Phase 1 Complete: Project structure and configuration established")