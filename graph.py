from langgraph.graph import StateGraph, END
from state import GraphState
from agents import research_agent, curriculum_agent
from logger import get_logger

logger = get_logger()

def build_graph():
    graph = StateGraph(GraphState)

    def research_node(state: GraphState) -> dict:
        try:
            research_data = research_agent(state.topic)
            return {"research_data": research_data}
        except Exception:
            logger.exception("Research node failed")
            return {"research_data": {}}

    def curriculum_node(state: GraphState) -> dict:
        try:
            result = curriculum_agent(
                topic=state.topic,
                research_data=state.research_data
            )
            return {"curriculum_draft": result.get("text")}
        except Exception:
            logger.exception("Curriculum node failed")
            return {"curriculum_draft": "Curriculum generation failed."}

    graph.add_node("research", research_node)
    graph.add_node("curriculum", curriculum_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "curriculum")
    graph.add_edge("curriculum", END)  

    return graph.compile()
