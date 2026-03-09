# MARVEL Microreactor TRL Assessment System

Automated Technology Readiness Level (TRL) assessment for the MARVEL microreactor subsystems using multi-agent AI and web scraping.

## 🎯 Project Overview

This system automatically assesses the Technology Readiness Levels (TRL 1-9) of six critical subsystems in the MARVEL microreactor by:
- Systematically searching technical literature (OSTI, arXiv, DOE reports)
- Extracting TRL indicators from documents
- Classifying subsystem maturity based on evidence
- Tracking technology progression over time

## 📊 Target Subsystems

1. **Reactor Core & Fuel Assembly** - Metallic HALEU fuel
2. **Heat Transport System** - Sodium heat pipes
3. **Reactivity Control System** - Control drums and shutdown rods
4. **Decay Heat Removal** - Passive cooling systems
5. **Instrumentation & Control** - Research reactor I&C
6. **Structural Support & Containment** - Guard vessel and reactor vessel

## 🛠️ Technology Stack

- **Agent Framework:** LangChain + LangGraph
- **LLM:** Claude (Anthropic)
- **Caching/State:** Redis
- **Data Sources:** OSTI.gov API, arXiv API, web scraping
- **Language:** Python 3.11+

## 📁 Project Structure
```
marvel-trl-assessment/
├── src/
│   ├── agents/          # AI agents (Search, Analysis, Classification)
│   ├── tools/           # Search and scraping tools
│   ├── prompts/         # LLM prompt templates
│   └── utils/           # Redis cache, helpers
├── config/              # Subsystem definitions, TRL mappings
├── data/
│   ├── raw/             # Retrieved documents (gitignored)
│   └── processed/       # TRL assessments (gitignored)
├── tests/               # Unit tests
├── notebooks/           # Jupyter notebooks for analysis
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Redis (local or cloud)
- Anthropic API key

### Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/marvel-trl-assessment.git
cd marvel-trl-assessment

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Redis Setup

**Option 1: Local Redis**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Windows - Use Docker
docker run -d -p 6379:6379 redis:latest
```

**Option 2: Redis Cloud** (free tier available)
- Sign up at https://redis.com/try-free/
- Update `.env` with connection details

### Run Test
```bash
# Test scraping on one subsystem
python test_scraper.py
```

## 📖 Usage

### Search for Subsystem Documentation
```python
from src.tools.search_tools import MARVELSearcherSimple
from config.subsystems import MARVEL_SUBSYSTEMS

searcher = MARVELSearcherSimple()
results = searcher.search_subsystem("heat_transport", MARVEL_SUBSYSTEMS["heat_transport"])
```

### Full Pipeline (Coming Soon)
```python
# Run complete TRL assessment
from src.pipeline import TRLPipeline

pipeline = TRLPipeline()
assessment = pipeline.assess_all_subsystems()
```

## 🗺️ Roadmap

- [x] Phase 1: Project setup and infrastructure
- [x] Phase 2: Search and scraping tools (OSTI, arXiv)
- [ ] Phase 3: Document analysis agent
- [ ] Phase 4: TRL classification agent
- [ ] Phase 5: Multi-agent orchestration with LangGraph
- [ ] Phase 6: Streamlit dashboard
- [ ] Phase 7: Scale to KRONOS MMR and eVinci reactors

## 📚 Data Sources

### Public Technical Literature
- **OSTI.gov** - DOE technical reports and lab publications
- **arXiv** - Academic papers on nuclear microreactor concepts
- **INL Publications** - Idaho National Laboratory MARVEL updates
- **Conference Proceedings** - ANS, ICAPP, NURETH

### TRL Source Mapping
- **TRL 8-9:** Operational reports, NRC inspections, deployment news
- **TRL 6-7:** NRC filings, construction permits, commercial announcements
- **TRL 4-5:** Lab reports, DOE project updates, prototype testing
- **TRL 1-3:** Academic papers, conference proceedings, conceptual designs

## 🔒 Security Notes

- **Never commit `.env` file** (contains API keys)
- **Raw data is gitignored** (may contain proprietary info)
- All data sources are publicly available technical literature

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Lasyapriya**
- Project: Advanced Nuclear Microreactor TRL Assessment Capstone
- Focus: Agentic AI for technology maturity tracking

## 🙏 Acknowledgments

- Idaho National Laboratory for MARVEL reactor documentation
- DOE ARDP program for microreactor development insights
- Anthropic for Claude API access

---

**Status:** 🚧 Active Development - Phase 2 Complete