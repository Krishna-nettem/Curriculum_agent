import os
import requests
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

import google.generativeai as genai
from langgraph.graph import StateGraph

load_dotenv()

st.set_page_config(page_title="AI Curriculum Generator", layout="wide")
st.title("AI Curriculum Generator")

class GraphState(BaseModel):
    topic: str
    research_data: List[str] = []
    curriculum_draft: Optional[str] = None
    confidence: float = 0.0
    retry_count: int = 0
    needs_human: bool = False


def google_search(query: str):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("SEARCH_ENGINE_ID"),
        "q": query,
        "num": 5
    }

    response = requests.get(url, params=params)
    data = response.json()

    summaries = []
    for item in data.get("items", []):
        summaries.append(item.get("snippet", ""))

    return summaries


def research_agent(state: GraphState) -> GraphState:
    query = f"{state.topic} beginner roadmap key concepts"
    results = google_search(query)

    if not results:
        results = [
            "Introduction to AI and Machine Learning",
            "What is Generative AI",
            "Large Language Models",
            "Prompt Engineering",
            "Image Generation",
            "Ethical AI"
        ]

    state.research_data = results
    state.confidence = min(1.0, len(results) / 5)
    state.retry_count += 1
    return state


def human_review(state: GraphState) -> GraphState:
    state.needs_human = False
    return state


def quality_gate(state: GraphState):
    if state.confidence >= 0.6:
        return "approved"

    if state.retry_count >= 2:
        state.needs_human = True
        return "human_review"

    return "retry"


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")


def curriculum_writer(state: GraphState) -> GraphState:
    prompt = f"""
Create a professional structured curriculum in Markdown format.

Topic: {state.topic}

Research:
{state.research_data}

Include:
- Overview
- Learning Outcomes
- 6 Modules
- Projects
- Capstone
"""
    response = model.generate_content(prompt)
    state.curriculum_draft = response.text
    return state


graph = StateGraph(GraphState)

graph.add_node("research_agent", research_agent)
graph.add_node("human_review", human_review)
graph.add_node("curriculum_writer", curriculum_writer)

graph.set_entry_point("research_agent")

graph.add_conditional_edges(
    "research_agent",
    quality_gate,
    {
        "retry": "research_agent",
        "human_review": "human_review",
        "approved": "curriculum_writer"
    }
)

graph.add_edge("human_review", "curriculum_writer")
graph.set_finish_point("curriculum_writer")

app_graph = graph.compile()


topic = st.text_input("Enter Course Topic", "Generative AI for Beginners")

if st.button("Generate Curriculum"):
    with st.spinner("Researching & Generating Curriculum..."):
        state = GraphState(topic=topic)
        result = app_graph.invoke(state)
        st.success("Curriculum Generated Successfully!")
        st.markdown(result["curriculum_draft"])
