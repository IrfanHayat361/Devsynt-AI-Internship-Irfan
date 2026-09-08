import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import TypedDict, Any
from datetime import datetime

class PipelineState(TypedDict):
    raw_data: Any
    domain: str
    domain_config: dict
    cleaned_data: Any
    analysis_results: Any
    dashboard_data: Any
    current_step: str
    messages: list

class DynamicDashboardAgent:
    def __init__(self):
        self.charts_created = []
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_dashboard(self, state: PipelineState) -> PipelineState:
        """Dynamically create dashboard based on domain and data"""
        
        print("\n🎨 DYNAMIC DASHBOARD AGENT: Building adaptive dashboard...")
        
        insights = state["analysis_results"]
        domain = state.get("domain", "generic")
        domain_config = state.get("domain_config", {})
        
        os.makedirs("assets", exist_ok=True)
        
        # Create adaptive charts based on domain
        self._create_domain_charts(insights, domain, domain_config)
        
        # Create dynamic HTML dashboard
        html = self._generate_dynamic_html(insights, domain, domain_config)
        with open('assets/dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("   ✓ Created dynamic dashboard.html")
        
        state["messages"].append({
            "role": "dashboard_agent",
            "content": f"Created {len(self.charts_created)} adaptive charts for {domain} domain"
        })
        
        return state
    
    def _create_domain_charts(self, insights, domain, domain_config):
        """Create charts based on detected domain"""
        
        # Chart 1: Top items
        if "top_products" in insights or "top_items" in insights:
            data = insights.get("top_products") or insights.get("top_items")
            if data:
                top_items = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:8])
                plt.figure(figsize=(10, 5))
                plt.bar(top_items.keys(), top_items.values(), color='steelblue')
                title = f"Top Items by {domain.title()}"
                plt.title(title, fontsize=14, fontweight='bold')
                plt.xlabel('Item')
                plt.ylabel('Count/Value')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('assets/top_items.png', dpi=150)
                plt.close()
                self.charts_created.append('top_items.png')
                print("   ✓ Created top_items.png")
        
        # Chart 2: Distribution by region/location
        if "sales_by_region" in insights or "distribution_by_location" in insights:
            data = insights.get("sales_by_region") or insights.get("distribution_by_location")
            if data and len(data) > 0:
                plt.figure(figsize=(8, 6))
                plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
                plt.title('Distribution by Region/Location', fontsize=14, fontweight='bold')
                plt.tight_layout()
                plt.savefig('assets/distribution.png', dpi=150)
                plt.close()
                self.charts_created.append('distribution.png')
                print("   ✓ Created distribution.png")
        
        # Chart 3: Category/Segment breakdown
        if "sales_by_category" in insights or "breakdown_by_category" in insights:
            data = insights.get("sales_by_category") or insights.get("breakdown_by_category")
            if data:
                categories = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
                plt.figure(figsize=(10, 5))
                plt.bar(categories.keys(), categories.values(), color='coral')
                plt.title('Performance by Category', fontsize=14, fontweight='bold')
                plt.xlabel('Category')
                plt.ylabel('Value')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('assets/category_performance.png', dpi=150)
                plt.close()
                self.charts_created.append('category_performance.png')
                print("   ✓ Created category_performance.png")
    
    def _generate_dynamic_html(self, insights, domain, domain_config) -> str:
        """Generate HTML dashboard dynamically based on domain"""
        
        domain_name = domain_config.get("name", "Data Analysis")
        domain_desc = domain_config.get("description", "Analysis results")
        
        # Get key metrics
        key_metrics = domain_config.get("key_metrics", [])
        
        # Build metrics section dynamically
        metrics_html = ""
        for i, metric in enumerate(key_metrics[:6]):  # Show first 6 metrics
            metric_key = metric.lower().replace(" ", "_")
            metric_value = insights.get(metric_key, "N/A")
            
            if isinstance(metric_value, (int, float)):
                if metric_value > 1000:
                    formatted = f"${metric_value:,.0f}" if "revenue" in metric_key or "sales" in metric_key else f"{metric_value:,.0f}"
                else:
                    formatted = f"{metric_value:.2f}"
            else:
                formatted = str(metric_value)
            
            metrics_html += f"""
            <div class="metric-card">
                <h3>{metric}</h3>
                <div class="metric-value">{formatted}</div>
            </div>
            """
        
        # Build charts section
        charts_html = ""
        chart_files = ['top_items.png', 'distribution.png', 'category_performance.png']
        chart_titles = ['Top Performers', 'Geographic Distribution', 'Category Breakdown']
        
        for chart_file, title in zip(chart_files, chart_titles):
            if os.path.exists(f'assets/{chart_file}'):
                charts_html += f"""
                <div class="chart-box">
                    <h3>{title}</h3>
                    <img src="{chart_file}" alt="{title}">
                </div>
                """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dynamic Dashboard - {domain_name}</title>
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
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #667eea;
            font-size: 2.8em;
            margin-bottom: 10px;
        }}
        .domain-info {{
            color: #764ba2;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .description {{
            color: #666;
            font-size: 1em;
            margin-bottom: 10px;
        }}
        .timestamp {{
            color: #888;
            font-size: 0.9em;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .metric-card h3 {{
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
            opacity: 0.9;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .chart-box {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .chart-box h3 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .chart-box img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        .summary {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .summary h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        .summary p {{
            color: #333;
            font-size: 1.05em;
            line-height: 1.8;
            margin-bottom: 15px;
        }}
        footer {{
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Dynamic Analytics Dashboard</h1>
            <p class="domain-info">Domain: {domain_name}</p>
            <p class="description">{domain_desc}</p>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="metrics">
            {metrics_html}
        </div>
        
        <div class="charts">
            {charts_html}
        </div>
        
        <div class="summary">
            <h2>Analysis Summary</h2>
            <p>This dashboard has been dynamically generated based on the detected domain type: <strong>{domain_name}</strong>.</p>
            <p>The pipeline has automatically configured itself to extract the most relevant metrics, groupings, and visualizations for this type of data.</p>
            <p>Charts and metrics adapt to your data structure, making this pipeline reusable across different domains and datasets.</p>
        </div>
        
        <footer>
            <p>Multi-Agent Production Dashboard | DevSynt AI Internship - Project 2 Phase 3</p>
        </footer>
    </div>
</body>
</html>
"""
        return html