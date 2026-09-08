import sys
import os
import pandas as pd
import glob
from datetime import datetime

sys.path.insert(0, 'agents')

from orchestrator import OrchestratorAgent, PipelineState
from domain_config import DomainConfigAgent
from clean_agent import CleanAgent
from analysis_agent import AnalysisAgent
from dynamic_dashboard import DynamicDashboardAgent
from langgraph.graph import StateGraph, START, END

def run_pipeline_for_dataset(csv_file, dataset_number):
    """Run the entire pipeline for a single dataset"""
    
    dataset_name = os.path.basename(csv_file)
    dataset_folder = f"assets/dataset{dataset_number}"
    os.makedirs(dataset_folder, exist_ok=True)
    
    print("\n" + "="*70)
    print(f"  DATASET {dataset_number}: {dataset_name}")
    print("="*70)
    
    # Step 1: Load data
    print("\n📁 LOADING DATA...")
    
    try:
        raw_data = pd.read_csv(csv_file, encoding='utf-8')
        print(f"✓ Loaded: {raw_data.shape[0]} rows × {raw_data.shape[1]} columns")
        print(f"  Columns: {', '.join(raw_data.columns[:5])}...")
    except Exception as e:
        print(f"❌ Error loading {csv_file}: {e}")
        return False
    
    # Step 2: Initialize agents
    print("\n🤖 INITIALIZING AGENTS...")
    
    llm = None
    try:
        from langchain_community.llms import Ollama
        llm = Ollama(model="gemma:2b", base_url="http://localhost:11434")
        print("✓ Connected to Ollama")
    except:
        print("⚠ Ollama not available (optional)")
    
    orchestrator = OrchestratorAgent()
    domain_agent = DomainConfigAgent(llm)
    clean_agent = CleanAgent(llm)
    analysis_agent = AnalysisAgent(llm)
    dashboard_agent = DynamicDashboardAgent()
    print("✓ All agents initialized")
    
    # Step 3: Build graph
    print("\n⚙️ BUILDING PIPELINE...")
    
    graph = StateGraph(PipelineState)
    
    def start_node(state):
        state["current_step"] = "domain_config"
        return state
    
    # Add all nodes
    graph.add_node("start", start_node)
    graph.add_node("orchestrator", orchestrator.orchestrator_node)
    graph.add_node("domain_config", domain_agent.detect_domain)
    graph.add_node("clean", clean_agent.clean_data)
    graph.add_node("analyze", analysis_agent.analyze_data)
    graph.add_node("dashboard", dashboard_agent.create_dashboard)
    
    # Connect edges properly
    graph.add_edge(START, "start")
    graph.add_edge("start", "orchestrator")
    
    # Conditional routing from orchestrator
    def route_from_orchestrator(state):
        step = state.get("current_step", "start")
        if step == "domain_config":
            return "domain_config"
        elif step == "clean":
            return "clean"
        elif step == "analyze":
            return "analyze"
        elif step == "dashboard":
            return "dashboard"
        else:
            return END
    
    graph.add_conditional_edges("orchestrator", route_from_orchestrator)
    graph.add_edge("domain_config", "orchestrator")
    graph.add_edge("clean", "orchestrator")
    graph.add_edge("analyze", "orchestrator")
    graph.add_edge("dashboard", "orchestrator")
    
    print("✓ Pipeline graph built")
    
    # Step 4: Run
    print("\n🔄 EXECUTING PIPELINE...")
    
    compiled_graph = graph.compile()
    
    initial_state = PipelineState(
        raw_data=raw_data,
        domain="",
        domain_config={},
        cleaned_data=None,
        analysis_results=None,
        dashboard_data=None,
        current_step="start",
        messages=[]
    )
    
    try:
        final_state = compiled_graph.invoke(initial_state)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False
    
    # Step 5: Move files to dataset-specific folder
    print("\n" + "="*70)
    print("  ORGANIZING OUTPUT FILES")
    print("="*70)
    
    files_to_move = [
        'dashboard.html',
        'top_items.png',
        'distribution.png',
        'category_performance.png'
    ]
    
    for file in files_to_move:
        src = f"assets/{file}"
        dst = f"{dataset_folder}/{file}"
        if os.path.exists(src):
            os.rename(src, dst)
            print(f"✓ Saved {file} for dataset {dataset_number}")
    
    # Step 6: Results
    print("\n" + "="*70)
    print("  RESULTS")
    print("="*70)
    
    domain_detected = final_state.get("domain", "unknown")
    domain_config = final_state.get("domain_config", {})
    domain_name = domain_config.get("name", "Unknown Domain")
    
    domain_map = {
        "retail": "Retail Sales",
        "ecommerce": "E-Commerce Orders",
        "inventory": "Inventory Management",
        "restaurant": "Restaurant Sales",
        "saas": "SaaS Subscriptions",
        "generic": "Generic Data",
        "unknown": "Unknown Domain"
    }
    
    display_domain = domain_map.get(domain_detected, domain_name)
    
    print(f"\nDomain: {display_domain}")
    
    if final_state["cleaned_data"] is not None:
        original_rows = raw_data.shape[0]
        cleaned_rows = final_state["cleaned_data"].shape[0]
        rows_removed = original_rows - cleaned_rows
        
        print(f"Data: {original_rows:,} rows → {cleaned_rows:,} rows ({rows_removed} removed)")
    
    print(f"Output: Saved to {dataset_folder}/")
    
    return True

def main():
    """Main function - automatically finds and tests all datasets"""
    
    print("\n" + "="*80)
    print("  PRODUCTION-GRADE MULTI-AGENT PIPELINE - PHASE 3")
    print("  Testing Across Multiple Domains")
    print("="*80)
    
    # Define expected dataset names in order
    expected_datasets = [
        "retail_data.csv",
        "ecommerce_data.csv",
        "inventory_data.csv",
        "restaurant_data.csv",
        "saas_data.csv"
    ]
    
    # Look for datasets in test-datasets folder
    test_files = []
    for dataset_name in expected_datasets:
        dataset_path = os.path.join("test-datasets", dataset_name)
        if os.path.exists(dataset_path):
            test_files.append(dataset_path)
    
    # If not enough datasets found, look in data folder as backup
    if len(test_files) < 5:
        data_files = glob.glob("data/*.csv")
        for data_file in data_files:
            if data_file not in test_files:
                test_files.append(data_file)
    
    if not test_files:
        print("\nNo datasets found. Please add CSV files to test-datasets/ folder")
        return False
    
    print(f"\nFound {len(test_files)} datasets to process:")
    for i, file in enumerate(test_files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    # Run pipeline for each dataset
    results = {}
    for idx, csv_file in enumerate(test_files, 1):
        dataset_name = os.path.basename(csv_file)
        try:
            success = run_pipeline_for_dataset(csv_file, idx)
            results[dataset_name] = "✓ PASSED" if success else "✗ FAILED"
        except Exception as e:
            print(f"\nError processing {dataset_name}: {e}")
            results[dataset_name] = "✗ FAILED"
        
        print("\n")
    
    # Summary
    print("\n" + "="*80)
    print("  SUMMARY")
    print("="*80)
    
    for dataset, status in results.items():
        print(f"  {status} {dataset}")
    
    passed = sum(1 for v in results.values() if "PASSED" in v)
    total = len(results)
    print(f"\nProcessed: {passed}/{total} datasets")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)