# Project 2 - Phase 3: Production-Grade Multi-Agent Retail Data Pipeline
 
## Overview
 
This is Phase 3 of a multi-agent data pipeline project that demonstrates advanced domain adaptation and intelligent orchestration. Building upon Phase 1 (fundamentals) and Phase 2 (basic multi-agent systems), Phase 3 introduces **automatic domain detection** and **adaptive processing** across 5 different business domains.
 
The pipeline automatically identifies the type of data being processed and configures itself to extract the most relevant insights, making it a truly production-grade solution.
 
## What's New in Phase 3
 
### 1. Domain Configuration Agent (NEW)
The pipeline now detects what type of data it's working with:
- **Retail Sales** - Analyzes sales, revenue, regions, categories
- **E-Commerce Orders** - Focuses on customer orders, product performance
- **Inventory Management** - Tracks stock levels, warehouse data
- **Restaurant Sales** - Analyzes menu items, orders, locations
- **SaaS Subscriptions** - Examines users, plans, churn metrics
### 2. Dynamic Dashboard Agent (NEW)
Instead of static dashboards, the pipeline now creates **adaptive dashboards** that:
- Show different metrics based on domain
- Generate domain-specific charts
- Adapt column names and groupings automatically
### 3. Updated Orchestrator
The orchestrator now:
- Routes based on domain configuration
- Passes domain metadata through the pipeline
- Ensures all agents adapt to the detected domain
## Architecture
 
```
Raw CSV Data (Any Domain)
    ↓
[Domain Configuration Agent] ← Detects: Retail, E-Commerce, Inventory, Restaurant, SaaS
    ↓
[Orchestrator Agent] ← Routes based on domain config
    ↓
[Clean Agent] → [Analysis Agent] → [Dynamic Dashboard Agent]
    ↓
Output Files (dashboard.html + charts for each domain)
```
 
## How It Works
 
### Step 1: Domain Detection
When you run the pipeline with a new dataset, the Domain Configuration Agent analyzes the column names and data structure to determine what type of data it is. It looks for keywords like:
- "sales", "revenue", "region" → Retail
- "order", "customer", "product" → E-Commerce
- "inventory", "stock", "warehouse" → Inventory
- "restaurant", "menu", "dish" → Restaurant
- "subscription", "mrr", "churn" → SaaS
### Step 2: Dynamic Orchestration
Based on the detected domain, the Orchestrator configures the rest of the pipeline with:
- Relevant metric names
- Key grouping columns
- Important numeric fields
- Domain-specific descriptions
### Step 3: Adaptive Processing
The Clean, Analysis, and Dashboard agents all receive the domain configuration and adapt their behavior:
- Clean Agent focuses on cleaning relevant columns
- Analysis Agent computes domain-specific metrics
- Dashboard Agent creates visualizations for that domain
### Step 4: Output Generation
Each dataset produces its own output folder with:
- `dashboard.html` - Interactive dashboard for that domain
- `top_items.png` - Chart of top performers
- `distribution.png` - Distribution breakdown
- `category_performance.png` - Category/segment analysis
## Test Results
 
The pipeline was tested on 5 different domains with 100% success:
 
### Dataset 1: Retail Sales Data
- **Domain Detected:** Retail Sales ✓
- **Rows Processed:** 9,800
- **Key Metrics:** Sales by region, top products, category performance
- **Output Location:** assets/dataset1/
### Dataset 2: E-Commerce Orders
- **Domain Detected:** E-Commerce Orders ✓
- **Rows Processed:** 500+
- **Key Metrics:** Orders by customer, product performance
- **Output Location:** assets/dataset2/
### Dataset 3: Inventory Management
- **Domain Detected:** Inventory Management ✓
- **Rows Processed:** 1,000+
- **Key Metrics:** Stock levels, warehouse distribution
- **Output Location:** assets/dataset3/
### Dataset 4: Restaurant Sales
- **Domain Detected:** Restaurant Sales ✓
- **Rows Processed:** 1,000+
- **Key Metrics:** Orders by menu item, restaurant performance
- **Output Location:** assets/dataset4/
### Dataset 5: SaaS Metrics
- **Domain Detected:** SaaS Subscriptions ✓
- **Rows Processed:** 5,000+
- **Key Metrics:** MRR, churn rate, subscription tiers
- **Output Location:** assets/dataset5/
## Technology Stack
 
- **LangChain** - LLM framework and orchestration
- **LangGraph** - Graph-based state management
- **Pandas** - Data processing and analysis
- **Matplotlib** - Chart generation
- **Python 3.12** - Core language
- **Ollama + Gemma 2B** - Local LLM (optional)
## Project Structure
 
```
project2-phase3/
├── agents/
│   ├── orchestrator.py          (UPDATED - domain-aware routing)
│   ├── domain_config.py         (NEW - domain detection)
│   ├── clean_agent.py
│   ├── analysis_agent.py
│   ├── dynamic_dashboard.py     (NEW - adaptive visualizations)
│   └── __init__.py
├── test-datasets/
│   ├── retail_data.csv
│   ├── ecommerce_data.csv
│   ├── inventory_data.csv
│   ├── restaurant_data.csv
│   └── saas_data.csv
├── assets/
│   ├── dataset1/
│   ├── dataset2/
│   ├── dataset3/
│   ├── dataset4/
│   ├── dataset5/
│   ├── flow-diagram.png
│   └── prompt-evolution-log.md
├── main.py                      (Phase 3 version)
├── README.md                    (this file)
└── PROMPT_EVOLUTION.md
```
 
## Key Improvements from Phase 2
 
| Feature | Phase 2 | Phase 3 |
|---------|---------|---------|
| Domain Detection | Manual | Automatic |
| Supported Domains | 1 (Retail only) | 5 (Retail, E-Commerce, Inventory, Restaurant, SaaS) |
| Dashboard Adaptation | Static | Dynamic (adapts to domain) |
| Configuration | Hard-coded | Data-driven |
| Scalability | Limited | Extensible to new domains |
| Orchestration | Basic routing | Domain-aware routing |
 
## Running the Pipeline
 
### Prerequisites
```
Python 3.8+
langchain, langgraph, langchain-community
pandas, numpy, matplotlib
```
 
### Installation
```bash
pip install langchain langgraph langchain-community pandas numpy matplotlib requests
```
 
### Execution
```bash
python main.py
```
 
### Output
The pipeline will:
1. Detect all 5 datasets
2. Process each through the domain-aware pipeline
3. Generate separate output for each domain
4. Display: `Processed: 5/5 datasets`
## Design Decisions
 
### Why Domain Detection?
In real-world scenarios, data comes in many forms. Rather than requiring manual configuration, the pipeline automatically adapts. This makes it:
- **Easier to use** - Just drop in a CSV
- **More flexible** - Handles new domains automatically
- **More maintainable** - Configuration is data-driven
### Why Separate Output per Dataset?
Each dataset gets its own folder to:
- Prevent file overwrites
- Keep results organized
- Enable comparison across domains
- Support batch processing
### Why Adaptive Dashboards?
A fixed dashboard template won't work for all domains. By making dashboards adaptive:
- Retail dashboards show regional breakdowns
- E-Commerce dashboards show customer segmentation
- SaaS dashboards show subscription metrics
- Each is optimized for its domain
## Future Enhancements
 
1. **More Domains** - Add healthcare, finance, supply chain, etc.
2. **Predictive Analytics** - ML models for forecasting
3. **Real-time Processing** - Stream data instead of batch
4. **Custom Metrics** - User-defined domain metrics
5. **API Endpoint** - REST API for production deployment
6. **Web Interface** - Flask/FastAPI dashboard
7. **Export Options** - PDF reports, email distribution
8. **Multi-language** - Support multiple prompt languages
## Lessons Learned
 
### Domain Detection Challenge
Initial approach used simple keyword matching. Refined to:
- Count keyword occurrences
- Use threshold-based detection
- Fallback to generic domain if needed
### Orchestrator Design
Started with fixed routing. Updated to:
- Accept domain configuration
- Pass domain metadata through state
- Make all agents domain-aware
### File Management
Initial version overwrote files. Fixed by:
- Creating dataset-specific folders
- Moving files after processing
- Preventing conflicts in batch mode
## Performance Metrics
 
- **Total Datasets Processed:** 5/5 (100%)
- **Average Processing Time:** ~2-5 seconds per dataset
- **File Generation Success:** 5/5 (100%)
- **Domain Detection Accuracy:** 5/5 (100%)
## Credits
 
**Project:** DevSynt AI Internship - Project 2 Phase 3
**Developer:** Irfan Hayat
**Mentor:** Afnan Shoukat
**Date:** September 2026
