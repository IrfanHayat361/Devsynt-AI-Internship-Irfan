import pandas as pd
import numpy as np
from typing import TypedDict, Any

class PipelineState(TypedDict):
    raw_data: Any
    domain: str
    domain_config: dict
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class DomainConfigAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.domain_config = {}
    
    def detect_domain(self, state: PipelineState) -> PipelineState:
        """Detect the domain/type of dataset"""
        
        print("\n🔍 DOMAIN CONFIGURATION: Analyzing dataset...")
        
        df = state["raw_data"]
        columns = df.columns.tolist()
        columns_lower = [col.lower() for col in columns]
        
        domain = "unknown"
        domain_config = {
            "name": "Unknown Domain",
            "key_metrics": [],
            "grouping_columns": [],
            "numeric_columns": [],
            "description": ""
        }
        
        # Check for Retail/Sales domain
        retail_keywords = ['sales', 'revenue', 'quantity', 'region', 'category', 'product', 'order', 'profit']
        retail_count = sum(1 for col in columns_lower if any(keyword in col for keyword in retail_keywords))
        
        if retail_count >= 4:
            domain = "retail"
            domain_config = {
                "name": "Retail Sales",
                "key_metrics": ["Total Sales", "Total Revenue", "Average Order Value"],
                "grouping_columns": ["Region", "Category", "Product"],
                "numeric_columns": ["Sales", "Revenue", "Quantity", "Profit"],
                "description": "Retail sales dataset"
            }
            print(f"   ✓ Detected: RETAIL SALES")
        
        # Check for E-commerce domain
        ecommerce_keywords = ['order', 'customer', 'price', 'quantity', 'product', 'category', 'status', 'date']
        ecommerce_count = sum(1 for col in columns_lower if any(keyword in col for keyword in ecommerce_keywords))
        
        if ecommerce_count >= 5 and domain == "unknown":
            domain = "ecommerce"
            domain_config = {
                "name": "E-Commerce Orders",
                "key_metrics": ["Total Orders", "Total Revenue", "Average Order Value"],
                "grouping_columns": ["Category", "Status", "Customer"],
                "numeric_columns": ["Price", "Quantity", "Revenue"],
                "description": "E-commerce order dataset"
            }
            print(f"   ✓ Detected: E-COMMERCE")
        
        # Check for Inventory domain
        inventory_keywords = ['stock', 'inventory', 'quantity', 'sku', 'warehouse', 'warehouse_id']
        inventory_count = sum(1 for col in columns_lower if any(keyword in col for keyword in inventory_keywords))
        
        if inventory_count >= 3 and domain == "unknown":
            domain = "inventory"
            domain_config = {
                "name": "Inventory Management",
                "key_metrics": ["Total Stock", "Stock Value", "Warehouse Count"],
                "grouping_columns": ["Warehouse", "SKU", "Category"],
                "numeric_columns": ["Quantity", "Stock Value"],
                "description": "Inventory management dataset"
            }
            print(f"   ✓ Detected: INVENTORY")
        
        # Check for Restaurant domain
        restaurant_keywords = ['restaurant', 'menu', 'dish', 'order', 'table', 'food', 'cuisine', 'item']
        restaurant_count = sum(1 for col in columns_lower if any(keyword in col for keyword in restaurant_keywords))
        
        if restaurant_count >= 3 and domain == "unknown":
            domain = "restaurant"
            domain_config = {
                "name": "Restaurant Sales",
                "key_metrics": ["Total Orders", "Total Revenue", "Popular Items"],
                "grouping_columns": ["Restaurant", "Category", "Item"],
                "numeric_columns": ["Price", "Quantity", "Revenue"],
                "description": "Restaurant sales dataset"
            }
            print(f"   ✓ Detected: RESTAURANT")
        
        # Check for SaaS domain
        saas_keywords = ['subscription', 'user', 'plan', 'churn', 'mrr', 'arr', 'account', 'tier']
        saas_count = sum(1 for col in columns_lower if any(keyword in col for keyword in saas_keywords))
        
        if saas_count >= 3 and domain == "unknown":
            domain = "saas"
            domain_config = {
                "name": "SaaS Subscriptions",
                "key_metrics": ["Total Users", "MRR", "Churn Rate"],
                "grouping_columns": ["Plan Type", "User Segment", "Account"],
                "numeric_columns": ["MRR", "Churn Rate", "Users"],
                "description": "SaaS subscription dataset"
            }
            print(f"   ✓ Detected: SAAS")
        
        # If no domain detected, use generic
        if domain == "unknown":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            domain = "generic"
            domain_config = {
                "name": "Generic Data",
                "key_metrics": ["Total Records", "Unique Values"],
                "grouping_columns": categorical_cols[:3],
                "numeric_columns": numeric_cols[:3],
                "description": "Generic dataset"
            }
            print(f"   ✓ Detected: GENERIC DOMAIN")
        
        state["domain"] = domain
        state["domain_config"] = domain_config
        
        print(f"   Domain: {domain_config['name']}")
        state["current_step"] = "clean"
        
        return state
    
    def get_config(self) -> dict:
        return self.domain_config