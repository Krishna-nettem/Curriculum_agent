<div align="center">

# 🎓 AI Curriculum Generator

### *Intelligent Course Design Powered by Multi-Agent AI*

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-FF4B4B.svg)](https://streamlit.io)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api-reference)

---

</div>

## 🌟 Overview

AI Curriculum Generator is a **production-ready, multi-agent system** that autonomously researches any topic and generates comprehensive, structured curricula. Built with LangGraph for orchestration, it combines advanced web search, intelligent content extraction, and LLM-powered generation to create professional course outlines in seconds.

### Why This Project?

- 🎯 **Autonomous Research**: No manual content curation needed
- 🧠 **Multi-Agent Architecture**: Specialized agents for research and curriculum design
- 🔍 **High-Quality Sources**: Tavily AI ensures academically sound content
- 📊 **State Management**: LangGraph provides robust workflow orchestration
- 🎨 **Professional Output**: Export to beautifully formatted PDFs

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🔍 **Intelligent Search** | Tavily AI API with advanced search depth for quality sources |
| 🕷️ **Smart Scraping** | Crawl4AI with content filtering (removes navigation, ads, footers) |
| 🤖 **Dual LLM Support** | Gemini (primary) + Ollama (fallback) for reliability |
| 📝 **Structured Output** | Markdown-formatted curricula with modules, objectives, projects |
| 📥 **PDF Export** | WeasyPrint-generated professional documents |
| 💾 **Session Persistence** | Streamlit state management prevents data loss |
| 📊 **Progress Tracking** | Real-time status updates during generation |
| 🔄 **Error Handling** | Graceful fallbacks and comprehensive logging |

---

## 🎬 Demo

```
# Input
Topic: "Generative AI for Beginners"

# Output
✅ 6-8 high-quality sources researched
✅ 15,000+ characters of curated content
✅ Professional curriculum with 6 modules
✅ Learning objectives, projects, and resources
✅ Downloadable PDF in <60 seconds
```

---

## 🏗️ Architecture

### System Flow

```
User Input (Topic)
     ↓
┌────────────────────┐
│  LangGraph Entry   │
└────────────────────┘
     ↓
┌────────────────────┐
│  Research Agent    │
│  -  Tavily Search   │
│  -  URL Discovery   │
│  -  Crawl4AI Scrape │
└────────────────────┘
     ↓
┌────────────────────┐
│  Quality Gate      │
│  (500+ char check) │
└────────────────────┘
     ↓
┌────────────────────┐
│ Curriculum Agent   │
│  -  Gemini LLM      │
│  -  Prompt Template │
│  -  Markdown Output │
└────────────────────┘
     ↓
┌────────────────────┐
│   Streamlit UI     │
│  -  Display         │
│  -  PDF Export      │
└────────────────────┘
```

### Tech Stack

**Frontend**: Streamlit 1.52+  
**AI Framework**: LangGraph, LangChain  
**LLMs**: Google Gemini Flash, Ollama (llama3.2:3b)  
**Search**: Tavily AI (advanced depth)  
**Web Scraping**: Crawl4AI (async, filtered)  
**PDF Generation**: WeasyPrint + Markdown  
**State**: Pydantic models with session persistence  

---

## 🚀 Installation

### Prerequisites

- Python 3.12+
- Ollama (optional, for local LLM fallback)
- API Keys: Gemini, Tavily

### Quick Start

```
# Clone repository
git clone https://github.com/YOUR_USERNAME/curriculum-agent.git
cd curriculum-agent

# Create virtual environment
python3 -m venv langgraph-env
source langgraph-env/bin/activate  # Windows: langgraph-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

### Environment Variables

```
# Required
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional (for Ollama fallback)
OLLAMA_MODEL=llama3.2:3b
```

### Ollama Setup (Optional)

```
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.2:3b

# Verify
ollama run llama3.2:3b "test"
```

---

## 💻 Usage

### Run the Application

```
streamlit run app.py
```

### Command Line Options

```
# Custom port
streamlit run app.py --server.port 8080

# Production mode
streamlit run app.py --server.headless true
```

### Example Workflow

1. **Enter Topic**: "Machine Learning Fundamentals"
2. **Wait**: Research agent searches + scrapes (30-45s)
3. **Generate**: LLM creates curriculum (15-30s)
4. **Download**: Export as PDF with one click

---

## 📂 Project Structure

```
curriculum-agent/
├── app.py                 # Streamlit UI with session state
├── graph.py              # LangGraph workflow definition
├── agents.py             # Research & curriculum agents
│   ├── tavily_search()   # Web search with Tavily
│   ├── crawl_urls_full() # Content extraction
│   └── curriculum_agent() # LLM generation
├── llm.py                # Gemini + Ollama integrations
├── prompts.py            # Curriculum generation prompts
├── state.py              # Pydantic state models
├── logger.py             # Structured JSON logging
├── .env                  # API keys (gitignored)
├── .gitignore            # Exclusions
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## 🔧 API Reference

### Research Agent

```
def research_agent(topic: str) -> dict:
    """
    Searches web and extracts content for curriculum generation.
    
    Args:
        topic: Course topic (e.g., "React.js")
    
    Returns:
        {
            "summary": str,
            "notes": List[{"url": str, "text": str}],
            "images": List[str],
            "sources": List[str]
        }
    """
```

### Curriculum Agent

```
def curriculum_agent(topic: str, difficulty: str, research_data: dict) -> dict:
    """
    Generates structured curriculum from research data.
    
    Args:
        topic: Course topic
        difficulty: "Beginner" | "Intermediate" | "Advanced"
        research_data: Output from research_agent()
    
    Returns:
        {
            "text": str,  # Markdown curriculum
            "source": "gemini" | "ollama" | "fallback",
            "sources": List[str]
        }
    """
```

---

## 🐛 Troubleshooting

### Ollama Timeout

**Error**: `ReadTimeout: Read timed out. (read timeout=120)`

**Solution**:
```
# In llm.py, increase timeout
timeout=600  # 10 minutes

# Or use faster model
ollama pull llama3.2:3b  # 3B is 3-4x faster than 8B
```

### Crawl4AI Content Issues

**Problem**: Too much navigation/junk scraped

**Solution**: Already configured in `agents.py` with:
- `excluded_tags=['nav', 'footer', 'header', 'aside']`
- `css_selector="article, main, .content"`
- Custom text cleaning filters

### PDF Generation Fails

**Error**: WeasyPrint installation issues

**Solution**:
```
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0

# macOS
brew install cairo pango gdk-pixbuf libffi
```

---

## 🛣️ Roadmap

- [ ] **Multi-language support** (Spanish, French, Hindi)
- [ ] **Custom difficulty levels** (user-adjustable)
- [ ] **Video integration** (YouTube API for resource links)
- [ ] **Collaborative editing** (multi-user curriculum refinement)
- [ ] **Vector search** (semantic similarity for better sources)
- [ ] **Analytics dashboard** (track generation metrics)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Setup

```
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration framework
- [Tavily AI](https://tavily.com) - Search API for AI applications
- [Crawl4AI](https://github.com/unclecode/crawl4ai) - LLM-friendly web scraping
- [Streamlit](https://streamlit.io) - Rapid web app framework

---



<div align="center">

### ⭐ Star this repo if you find it useful!

Made with ❤️ by [Your Name]

</div>
```

**To use it:**

1. Copy everything between the backticks
2. Create a file: `nano README.md`
3. Paste the content
4. Save and commit: `git add README.md && git commit -m "Add comprehensive README" && git push`


