from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Any
import pandas as pd

class PipelineState(TypedDict):
    raw_data: Any
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class OrchestratorAgent:
    def __init__(self, model_name: str = "gemma:2b", base_url: str = "http://localhost:11434"):
        try:
            self.llm = Ollama(model=model_name, base_url=base_url)
        except:
            self.llm = None
        self.graph = None
        
    def orchestrator_node(self, state: PipelineState) -> PipelineState:
        current_step = state.get("current_step", "start")
        
        if current_step == "start":
            print(f"\n📍 ORCHESTRATOR: Received dataset")
            state["current_step"] = "clean"
        elif current_step == "clean":
            print(f"\n✅ ORCHESTRATOR: Data cleaned. Routing to analysis...")
            state["current_step"] = "analyze"
        elif current_step == "analyze":
            print(f"\n📈 ORCHESTRATOR: Analysis complete. Routing to visualization...")
            state["current_step"] = "visualize"
        elif current_step == "visualize":
            print(f"\n🎨 ORCHESTRATOR: Pipeline complete!")
            state["current_step"] = "end"
        
        return state
    
    def build_graph(self) -> StateGraph:
        graph = StateGraph(PipelineState)
        graph.add_node("orchestrator", self.orchestrator_node)
        graph.add_edge(START, "orchestrator")
        
        def route_step(state: PipelineState):
            step = state.get("current_step", "start")
            if step == "clean":
                return "clean"
            elif step == "analyze":
                return "analyze"
            elif step == "visualize":
                return "visualize"
            else:
                return "end"
        
        graph.add_conditional_edges("orchestrator", route_step)
        graph.add_edge("clean", "orchestrator")
        graph.add_edge("analyze", "orchestrator")
        graph.add_edge("visualize", "orchestrator")
        graph.add_edge("end", END)
        
        self.graph = graph
        return graph