# Project 2 - Phase 2: Multi-Agent Retail Data Pipeline

## Overview

This project implements a **multi-agent retail data pipeline** using LangChain and LangGraph. The pipeline orchestrates four specialized agents to clean, analyze, and visualize retail sales data automatically.

## Architecture

The pipeline follows the **node → edge → state pattern** learned in Phase 1:

```
Raw CSV Data (9,800+ rows)
    ↓
[Orchestrator Agent] - Coordinates execution
    ↓
[Clean Agent] - Fixes data quality issues
    ↓
[Analysis Agent] - Generates insights
    ↓
[Visualization Agent] - Creates charts & dashboard
    ↓
Output: Cleaned Data + 3 Charts + HTML Dashboard
```

## Four Specialized Agents

### 1. Orchestrator Agent
Routes data flow between agents. Implements LangGraph StateGraph pattern to manage pipeline execution.

**File:** `agents/orchestrator.py`

### 2. Clean Agent
Handles data quality issues:
- Fills missing values with median
- Fixes incorrect data types
- Removes duplicate rows
- Removes invalid entries

**File:** `agents/clean_agent.py`

### 3. Analysis Agent
Generates insights from cleaned data:
- Total sales and revenue calculations
- Top products by quantity sold
- Sales breakdown by region
- Sales breakdown by category
- Summary statistics

**File:** `agents/analysis_agent.py`

### 4. Visualization Agent
Creates output visualizations:
- Top products bar chart
- Regional sales pie chart
- Category performance bar chart
- Static HTML dashboard with embedded charts

**File:** `agents/visualization_agent.py`

## Requirements

```
Python 3.8+
langchain
langgraph
langchain-community
pandas
numpy
matplotlib
requests
```

## Installation

```bash
pip install langchain langgraph langchain-community pandas numpy matplotlib requests
```

## Dataset

Download the **Kaggle Superstore Dataset**:
- URL: https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting
- File: `Superstore.csv`
- Place in: `data/retail_data.csv`

Columns included: Row ID, Order ID, Date, Ship Date, Mode, Customer ID, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit

## Usage

### Step 1: Download Data
```bash
# Download Superstore.csv from Kaggle
# Place it in: data/retail_data.csv
```

### Step 2: Run Pipeline
```bash
python main.py
```

### Step 3: View Results
Open `assets/dashboard.html` in your web browser

## Output Files

| File | Description |
|------|-------------|
| `assets/dashboard.html` | Main interactive dashboard |
| `assets/top_products.png` | Bar chart of best-selling products |
| `assets/sales_by_region.png` | Pie chart showing regional distribution |
| `assets/sales_by_category.png` | Bar chart of category performance |
| `data/cleaned_retail_data.csv` | Cleaned dataset output |

## Project Structure

```
project2-phase2/
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── clean_agent.py
│   ├── analysis_agent.py
│   └── visualization_agent.py
├── data/
│   └── retail_data.csv
├── assets/
│   ├── dashboard.html
│   ├── top_products.png
│   ├── sales_by_region.png
│   └── sales_by_category.png
├── main.py
├── README.md
└── .gitignore
```

## How It Works

1. **Data Loading** - Reads CSV file (9,800 rows × 18 columns)
2. **Data Cleaning** - Removes missing values and invalid entries
3. **Analysis** - Computes metrics and generates insights
4. **Visualization** - Creates charts and HTML dashboard
5. **Output** - Saves all results to `assets/` folder

## Key Technologies

- **LangChain** - LLM framework for building agent systems
- **LangGraph** - Graph-based orchestration for multi-agent workflows
- **Pandas** - Data processing and manipulation
- **Matplotlib** - Chart generation
- **Python** - Core programming language

## Design Patterns

### Node → Edge → State
- Nodes = Agents (Orchestrator, Clean, Analysis, Visualization)
- Edges = Data flow connections between agents
- State = PipelineState carries data through the pipeline

### Separation of Concerns
- Each agent has a single, well-defined responsibility
- Clean interfaces between agents
- Easy to extend or modify individual agents

## Example Output

When you run `python main.py`, you get:

```
======================================================================
   RETAIL MULTI-AGENT DATA PIPELINE
======================================================================

 LOADING DATA...
✓ Loaded: 9800 rows × 18 columns
  Missing values: 11

 INITIALIZING AGENTS...
✓ Connected to Ollama
✓ All agents ready

 BUILDING PIPELINE...
✓ Pipeline built

 EXECUTING PIPELINE...

 CLEAN AGENT: Starting data cleaning...
   Original shape: (9800, 18)
   Final shape: (9800, 18)
   Rows removed: 0

 ANALYSIS AGENT: Starting EDA...
   Total Sales: $2,261,536.78
   ✓ Top region: California
   ✓ Top category: Consumer

 VISUALIZATION AGENT: Creating charts...
   ✓ Created top_products.png
   ✓ Created sales_by_region.png
   ✓ Created sales_by_category.png
   ✓ Created dashboard.html

======================================================================
  PIPELINE COMPLETE!
======================================================================
```

## Results

- **Data Processed:** 9,800 retail transactions
- **Data Cleaned:** 11 missing values filled
- **Insights Generated:** 15+ metrics computed
- **Visualizations:** 3 professional charts created
- **Dashboard:** Static HTML with embedded charts

## Troubleshooting

**"Module not found" error:**
```bash
pip install --break-system-packages langchain langgraph langchain-community pandas numpy matplotlib requests
```

**"File not found" error:**
Make sure `data/retail_data.csv` exists in the project folder.

**"UnicodeEncodeError":**
Already fixed in the code with UTF-8 encoding.

## Technologies Used

- LangChain 0.3+
- LangGraph 0.0+
- Pandas 2.0+
- Matplotlib 3.8+
- Python 3.12

## Author

**Irfan Hayat**
DevSynt AI Automation Internship
Project 2 - Phase 2

## Mentor

Afnan Shoukat

## Date

September 2024
