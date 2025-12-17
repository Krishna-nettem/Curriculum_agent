import streamlit as st
from graph import build_graph
from state import GraphState
from logger import get_logger
import markdown
from weasyprint import HTML
import io

logger = get_logger()

st.set_page_config(page_title="Course Creator Pro", layout="wide")
st.title("Curriculum Generator")


if "curriculum_text" not in st.session_state:
    st.session_state.curriculum_text = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

topic = st.text_input("Course topic")
gen_btn = st.button("Generate Curriculum")

if gen_btn and topic.strip():
    try:
        with st.status("Generating Curriculum...", expanded=True) as status:
            st.write("🔍 Searching the web for relevant content...")
            graph = build_graph()
            state = GraphState(topic=topic)
            logger.info(f"UI triggered graph for topic: {topic}")
            
            result = graph.invoke(state)
            
            st.write("✍️ Generating structured curriculum...")
            
            st.session_state.curriculum_text = result.get("curriculum_draft", "No curriculum generated.")
            st.session_state.topic = topic
            
            status.update(label="Curriculum Generated!", state="complete", expanded=False)
    except Exception:
        logger.exception("Top-level UI execution failed")
        st.error("❌ Something went wrong. Check logs.json.")


if st.session_state.curriculum_text:
    st.success("Curriculum Generated Successfully!")
    st.subheader("📚 Your Curriculum")
    st.markdown(st.session_state.curriculum_text)
    
    if st.session_state.curriculum_text != "No curriculum generated.":
        try:
            
            html = markdown.markdown(st.session_state.curriculum_text)
            pdf_buffer = io.BytesIO()
            HTML(string=html).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            
            st.download_button(
                "Download as PDF",
                pdf_buffer,
                file_name=f"{st.session_state.topic.replace(' ', '_')}_curriculum.pdf",
                mime="application/pdf"
            )
        except Exception:
            logger.exception("PDF generation failed")
            st.download_button(
                "Download as Markdown",
                st.session_state.curriculum_text,
                file_name=f"{st.session_state.topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )
