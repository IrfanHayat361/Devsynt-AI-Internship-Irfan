from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Any
import pandas as pd

class PipelineState(TypedDict):
    raw_data: Any
    domain: str
    domain_config: dict
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class OrchestratorAgent:
    def __init__(self):
        self.graph = None
    
    def orchestrator_node(self, state: PipelineState) -> PipelineState:
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            print(f"\n📍 ORCHESTRATOR: Pipeline started")
            state["current_step"] = "domain_config"
        elif current_step == "domain_config":
            print(f"\n✅ ORCHESTRATOR: Domain detected. Routing to cleaning...")
            state["current_step"] = "clean"
        elif current_step == "clean":
            print(f"\n✅ ORCHESTRATOR: Data cleaned. Routing to analysis...")
            state["current_step"] = "analyze"
        elif current_step == "analyze":
            print(f"\n📈 ORCHESTRATOR: Analysis complete. Routing to dashboard...")
            state["current_step"] = "dashboard"
        elif current_step == "dashboard":
            print(f"\n🎨 ORCHESTRATOR: Dashboard created. Pipeline complete!")
            state["current_step"] = "end"
        
        return state