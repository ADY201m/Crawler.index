import pandas as pd
import os
from playwright.sync_api import sync_playwright

def get_coffee_data():
    data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in headed mode for debugging
        page = browser.new_page()
        
        # Navigate to the page
        page.goto('https://tradingeconomics.com/commodity/coffee', timeout=60000)
        
        # Handle cookie consent if present
        try:
            page.click('button:has-text("Accept")', timeout=5000)
        except Exception as e:
            print("Cookie consent not found or clickable:", e)
        
        # Wait for Highcharts to load and chart data to be available
        page.wait_for_function('''() => {
            return window.Highcharts && 
                   window.Highcharts.charts[0] && 
                   window.Highcharts.charts[0].series.length > 0;
        }''', timeout=60000)
        
        # Extract data from Highcharts
        chart_data = page.evaluate('''() => {
            const chart = window.Highcharts.charts[0];
            if (!chart) return null;
            
            const series = chart.series[0];  // Main price series
            return series.data.map(point => ({
                date: new Date(point.x).toISOString().slice(0,8),
                value: point.y
            }));
        }''')

        if chart_data:
            data = chart_data
            
        browser.close()
    
    return pd.DataFrame(data)

# Make sure the directory exists
os.makedirs('data/raw', exist_ok=True)

# Get data
df = get_coffee_data()
print(df.head(10))

# Save to CSV in data/raw directory
df.to_csv('data/raw/coffee_prices.csv', index=False)