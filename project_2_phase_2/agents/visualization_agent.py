import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import TypedDict, Any
from datetime import datetime

class PipelineState(TypedDict):
    raw_data: Any
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class VisualizationAgent:
    def __init__(self):
        self.charts_created = []
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def create_visualizations(self, state: PipelineState) -> PipelineState:
        print("\n🎨 VISUALIZATION AGENT: Creating charts...")
        
        insights = state["analysis_results"]
        os.makedirs("assets", exist_ok=True)
        
        # Create charts from available data
        if "top_products" in insights:
            top_prods = dict(sorted(insights["top_products"].items(), key=lambda x: x[1], reverse=True)[:8])
            plt.figure(figsize=(10, 5))
            plt.bar(top_prods.keys(), top_prods.values(), color='steelblue')
            plt.title('Top Products by Quantity Sold', fontsize=14, fontweight='bold')
            plt.xlabel('Product')
            plt.ylabel('Quantity Sold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('assets/top_products.png', dpi=150)
            plt.close()
            self.charts_created.append('top_products.png')
            print("   ✓ Created top_products.png")
        
        if "sales_by_region" in insights:
            regions = insights["sales_by_region"]
            plt.figure(figsize=(8, 6))
            plt.pie(regions.values(), labels=regions.keys(), autopct='%1.1f%%', startangle=90)
            plt.title('Sales Distribution Across Regions', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('assets/sales_by_region.png', dpi=150)
            plt.close()
            self.charts_created.append('sales_by_region.png')
            print("   ✓ Created sales_by_region.png")
        
        if "sales_by_category" in insights:
            categories = dict(sorted(insights["sales_by_category"].items(), key=lambda x: x[1], reverse=True))
            plt.figure(figsize=(10, 5))
            plt.bar(categories.keys(), categories.values(), color='coral')
            plt.title('Sales Performance by Category', fontsize=14, fontweight='bold')
            plt.xlabel('Category')
            plt.ylabel('Total Sales ($)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('assets/sales_by_category.png', dpi=150)
            plt.close()
            self.charts_created.append('sales_by_category.png')
            print("   ✓ Created sales_by_category.png")
        
        # Create HTML dashboard with UTF-8 encoding
        html = self._generate_html(insights)
        with open('assets/dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("   ✓ Created dashboard.html")
        
        state["messages"].append({
            "role": "visualization_agent",
            "content": f"Created {len(self.charts_created)} charts and dashboard"
        })
        
        return state
    
    def _generate_html(self, insights: dict) -> str:
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Retail Sales Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            color: #666;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .timestamp {{
            color: #888;
            font-size: 0.9em;
        }}
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .chart-box h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        .chart-box img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        .summary {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .summary h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .summary p {{
            margin: 10px 0;
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }}
        .insights {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .insights h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .insight-item {{
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }}
        .insight-item strong {{
            color: #667eea;
        }}
        footer {{
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 30px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Our Retail Sales Dashboard</h1>
            <p class="subtitle">Multi-Agent Data Pipeline Analysis</p>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="summary">
            <h2>Dashboard Overview</h2>
            <p>This dashboard presents a comprehensive analysis of our retail sales data. Our multi-agent pipeline has processed, cleaned, and analyzed our dataset to provide key insights into our sales performance across different regions and product categories.</p>
        </div>
        
        <div class="charts">
            <div class="chart-box">
                <h3>Our Top Products</h3>
                <img src="top_products.png" alt="Our Top Products">
            </div>
            <div class="chart-box">
                <h3>Our Regional Sales</h3>
                <img src="sales_by_region.png" alt="Our Sales by Region">
            </div>
            <div class="chart-box">
                <h3>Our Category Performance</h3>
                <img src="sales_by_category.png" alt="Our Sales by Category">
            </div>
        </div>
        
        <div class="insights">
            <h2>Key Insights from Our Data</h2>
            <div class="insight-item">
                <strong>Total Sales Revenue:</strong> Our dataset shows strong overall sales performance with comprehensive market coverage.
            </div>
            <div class="insight-item">
                <strong>Regional Distribution:</strong> Our sales are distributed across multiple regions, with varying performance levels that provide growth opportunities.
            </div>
            <div class="insight-item">
                <strong>Product Performance:</strong> Our product categories show diverse sales patterns, indicating a well-rounded portfolio.
            </div>
            <div class="insight-item">
                <strong>Data Quality:</strong> Our cleaning process has ensured that all missing values have been handled and our data is ready for strategic decision-making.
            </div>
        </div>
        
        <footer>
            <p>Powered by Our Multi-Agent Retail Data Pipeline | DevSynt AI Internship Project</p>
        </footer>
    </div>
</body>
</html>
"""
        return html