import sys
import os
import pandas as pd

# Add agents to path
sys.path.insert(0, 'agents')

from orchestrator import OrchestratorAgent, PipelineState
from clean_agent import CleanAgent
from analysis_agent import AnalysisAgent
from visualization_agent import VisualizationAgent
from langgraph.graph import StateGraph, START, END

def main():
    print("\n" + "="*70)
    print("  🚀 RETAIL MULTI-AGENT DATA PIPELINE")
    print("="*70)
    
    # Step 1: Load data
    print("\n📁 LOADING DATA...")
    
    if not os.path.exists("data/retail_data.csv"):
        print("❌ Error: data/retail_data.csv not found!")
        print("Please download Superstore.csv from Kaggle and place it in data/")
        return False
    
    raw_data = pd.read_csv("data/retail_data.csv", encoding='utf-8')
    print(f"✓ Loaded: {raw_data.shape[0]} rows × {raw_data.shape[1]} columns")
    print(f"  Columns: {', '.join(raw_data.columns[:5])}...")
    print(f"  Missing values: {raw_data.isnull().sum().sum()}")
    
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
    clean_agent = CleanAgent(llm)
    analysis_agent = AnalysisAgent(llm)
    viz_agent = VisualizationAgent()
    print("✓ All agents ready")
    
    # Step 3: Build graph
    print("\n⚙️ BUILDING PIPELINE...")
    
    graph = StateGraph(PipelineState)
    
    # Add nodes
    def start_node(state):
        state["current_step"] = "clean"
        return state
    
    graph.add_node("start", start_node)
    graph.add_node("clean", clean_agent.clean_data)
    graph.add_node("analyze", analysis_agent.analyze_data)
    graph.add_node("visualize", viz_agent.create_visualizations)
    
    # Connect
    graph.add_edge(START, "start")
    graph.add_edge("start", "clean")
    graph.add_edge("clean", "analyze")
    graph.add_edge("analyze", "visualize")
    graph.add_edge("visualize", END)
    
    print("✓ Pipeline built")
    
    # Step 4: Run
    print("\n🔄 EXECUTING PIPELINE...")
    
    compiled_graph = graph.compile()
    
    initial_state = PipelineState(
        raw_data=raw_data,
        cleaned_data=None,
        analysis_results=None,
        dashboard_data=None,
        current_step="start",
        messages=[]
    )
    
    final_state = compiled_graph.invoke(initial_state)
    
    # Step 5: Results
    print("\n" + "="*70)
    print("  ✨ PIPELINE COMPLETE!")
    print("="*70)
    
    if final_state["cleaned_data"] is not None:
        cleaned = final_state["cleaned_data"]
        print(f"\n📊 Cleaning Results:")
        print(f"   Input:  {raw_data.shape[0]} rows")
        print(f"   Output: {cleaned.shape[0]} rows")
        print(f"   Removed: {raw_data.shape[0] - cleaned.shape[0]} rows")
        
        # Save cleaned data with UTF-8 encoding
        cleaned.to_csv("data/cleaned_retail_data.csv", index=False, encoding='utf-8')
        print(f"   Saved to: data/cleaned_retail_data.csv")
    
    if final_state["analysis_results"] is not None:
        insights = final_state["analysis_results"]
        print(f"\n📈 Analysis Results:")
        print(f"   Generated {len(insights)} insight types")
    
    print(f"\n📁 Output Files:")
    print(f"   ✓ assets/dashboard.html ← OPEN THIS IN BROWSER")
    print(f"   ✓ assets/top_products.png")
    print(f"   ✓ assets/sales_by_region.png")
    print(f"   ✓ assets/sales_by_category.png")
    print(f"   ✓ data/cleaned_retail_data.csv")
    
    print(f"\n🌐 VIEW DASHBOARD:")
    print(f"   Right-click on assets/dashboard.html → Open with Browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)