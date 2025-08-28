
import pandas as pd
import numpy as np

def assess_data_quality(df, dataset_name):
    """Comprehensive data quality assessment for vaccination datasets"""
    print(f"\n{'='*60}")
    print(f"DATA QUALITY ASSESSMENT: {dataset_name.upper()}")
    print(f"{'='*60}")

    # Basic info
    print(f"Dataset Shape: {df.shape}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Missing values analysis
    missing_analysis = df.isnull().sum()
    missing_percentage = (missing_analysis / len(df)) * 100

    print(f"\nMISSING VALUES ANALYSIS:")
    print("-" * 30)
    for col in df.columns:
        if missing_analysis[col] > 0:
            print(f"{col}: {missing_analysis[col]:,} ({missing_percentage[col]:.2f}%)")

    # Data types and unique values
    print(f"\nDATA TYPES AND UNIQUE VALUES:")
    print("-" * 35)
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"{col}: {df[col].dtype} - {unique_count:,} unique values")

    # Duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate Records: {duplicates:,}")

    # Quality score calculation
    completeness_score = (1 - missing_percentage.mean() / 100) * 100
    uniqueness_score = 100 if duplicates == 0 else max(0, 100 - (duplicates / len(df)) * 100)
    overall_quality = (completeness_score + uniqueness_score) / 2

    print(f"\nQUALITY SCORES:")
    print(f"Completeness: {completeness_score:.2f}%")
    print(f"Uniqueness: {uniqueness_score:.2f}%")
    print(f"Overall Quality: {overall_quality:.2f}%")

    return {
        'missing_analysis': missing_analysis,
        'missing_percentage': missing_percentage,
        'duplicates': duplicates,
        'quality_scores': {
            'completeness': completeness_score,
            'uniqueness': uniqueness_score,
            'overall': overall_quality
        }
    }

def clean_coverage_data(df):
    """Comprehensive cleaning for vaccination coverage data"""
    print("Cleaning Coverage Data...")
    df_clean = df.copy()

    # Remove rows where essential columns are all null
    essential_cols = ['CODE', 'NAME', 'YEAR', 'ANTIGEN']
    df_clean = df_clean.dropna(subset=essential_cols, how='any')

    # Standardize country codes
    df_clean['CODE'] = df_clean['CODE'].str.upper().str.strip()

    # Clean year data
    df_clean['YEAR'] = pd.to_numeric(df_clean['YEAR'], errors='coerce')
    df_clean = df_clean[(df_clean['YEAR'] >= 1980) & (df_clean['YEAR'] <= 2024)]

    # Handle missing target numbers
    df_clean['TARGET_NUMBER'] = df_clean.groupby(['CODE', 'ANTIGEN'])['TARGET_NUMBER'].transform(
        lambda x: x.fillna(x.median())
    )

    # Calculate missing doses from coverage and target
    mask_calc_doses = (df_clean['DOSES'].isna() & 
                      df_clean['COVERAGE'].notna() & 
                      df_clean['TARGET_NUMBER'].notna())

    df_clean.loc[mask_calc_doses, 'DOSES'] = (
        df_clean.loc[mask_calc_doses, 'COVERAGE'] / 100 * 
        df_clean.loc[mask_calc_doses, 'TARGET_NUMBER']
    )

    # Calculate missing coverage from doses and target
    mask_calc_coverage = (df_clean['COVERAGE'].isna() & 
                         df_clean['DOSES'].notna() & 
                         df_clean['TARGET_NUMBER'].notna() &
                         (df_clean['TARGET_NUMBER'] > 0))

    df_clean.loc[mask_calc_coverage, 'COVERAGE'] = (
        df_clean.loc[mask_calc_coverage, 'DOSES'] / 
        df_clean.loc[mask_calc_coverage, 'TARGET_NUMBER'] * 100
    )

    # Cap coverage at 100%
    df_clean['COVERAGE'] = np.where(df_clean['COVERAGE'] > 100, 100, df_clean['COVERAGE'])

    # Remove negative values
    numeric_cols = ['TARGET_NUMBER', 'DOSES', 'COVERAGE']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean = df_clean[df_clean[col] >= 0]

    print(f"Coverage data cleaned: {len(df_clean):,} records remaining")
    return df_clean
