import pandas as pd
import numpy as np
from typing import TypedDict, Any

class PipelineState(TypedDict):
    raw_data: Any
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class CleanAgent:
    def __init__(self, llm):
        self.llm = llm
        self.cleaning_report = {}
        
    def clean_data(self, state: PipelineState) -> PipelineState:
        print("\n🧹 CLEAN AGENT: Starting data cleaning...")
        
        df = state["raw_data"].copy()
        original_shape = df.shape
        
        report = {
            "original_rows": original_shape[0],
            "original_columns": original_shape[1],
        }
        
        print(f"   Original shape: {original_shape}")
        print(f"   Missing values: {df.isnull().sum().sum()}")
        
        # 1. Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"   ✓ Filled {col} with median: {median_val:.2f}")
        
        # 2. Fix data types - ensure numeric columns are numeric
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        
        # 3. Remove duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            df = df.drop_duplicates()
            print(f"   ✓ Removed {duplicates} duplicates")
        
        # 4. Remove rows with negative values in quantity/sales columns
        for col in df.columns:
            if 'quantity' in col.lower() or 'sales' in col.lower():
                try:
                    invalid_count = (df[col] < 0).sum()
                    if invalid_count > 0:
                        df = df[df[col] >= 0]
                        print(f"   ✓ Removed {invalid_count} rows with negative {col}")
                except:
                    pass
        
        final_shape = df.shape
        report["final_rows"] = final_shape[0]
        report["rows_removed"] = original_shape[0] - final_shape[0]
        
        print(f"   Final shape: {final_shape}")
        print(f"   Rows removed: {report['rows_removed']}")
        
        state["cleaned_data"] = df
        state["messages"].append({
            "role": "clean_agent",
            "content": f"Cleaned data: {original_shape[0]} → {final_shape[0]} rows"
        })
        
        return state
    
    def get_report(self) -> dict:
        return self.cleaning_report