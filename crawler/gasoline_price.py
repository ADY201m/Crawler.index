import pandas as pd
import os
from playwright.sync_api import sync_playwright

def get_gasoline_data():
    data = []
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Keep headless=False for debugging
        
        # Create a new context with cookies
        context = browser.new_context()
        
        # Set cookies for tradingeconomics.com
        cookies = [
            {
                "name": "ASP.NET_SessionId",
                "value": "rjvgp1a4zbzykuoipg2004zv",
                "domain": "tradingeconomics.com",
                "path": "/"
            },
            {
                "name": ".ASPXAUTH",
                "value": "B04DA19728379F4B42EC0DD6A9C07B61683E20D1C13D8CB4A08D1D3E568157257736092BBF3ED7C450B4E3A6561179288B16912D4E5266F28FB6C2361B7AE27C4B779001603A7F9F8437215B6443FB437BA3E56A75BB0C2CE7689752DF5583D45496FA04289ED036F06BF0FFD0EAE1DC3384D698",
                "domain": ".tradingeconomics.com",
                "path": "/"
            },
            {
                "name": "TEUsername",
                "value": "sqDLFuB/42qowTBDv8zrCdH41cQJzv9ZnXy5NkuD5bOANBHNdoRtObCLNy8J19kE",
                "domain": ".tradingeconomics.com",
                "path": "/"
            },
            {
                "name": "TEUserInfo",
                "value": "07a31fed-e8a8-4aae-b5d1-a68047c654fe",
                "domain": ".tradingeconomics.com",
                "path": "/"
            },
            {
                "name": "TEUserEmail",
                "value": "maiphuocminhtai21032005@gmail.com",
                "domain": ".tradingeconomics.com",
                "path": "/"
            }
        ]
        
        # Add cookies to the context
        context.add_cookies(cookies)
        print("Cookies added to browser context")
        
        # Open a new page with the authenticated context
        page = context.new_page()
        
        # Navigate to the gasoline prices page
        page.goto('https://tradingeconomics.com/vietnam/gasoline-prices', timeout=60000)
        
        # Wait for the chart to load
        try:
            page.wait_for_selector('.highcharts-series-group', timeout=20000)
            print("Chart loaded")
        except Exception as e:
            print("Error waiting for chart:", e)
            browser.close()
            return pd.DataFrame()

        # Click the "Max" button to load all data
        try:
            page.click('a[data-span_str="MAX"]', timeout=5000)
            print("Clicked 'Max' button")
            # Wait for chart to update
            page.wait_for_timeout(3000)  # 3 seconds to allow data to load
        except Exception as e:
            print("Could not click 'Max' button:", e)

        # Verify more data loaded (optional check)
        try:
            page.wait_for_function(
                'Highcharts.charts[0].series[0].data.length > 12',
                timeout=15000
            )
            print("Confirmed chart loaded more data")
        except Exception as e:
            print("Timeout waiting for more data:", e)
            print("Proceeding with extraction anyway")

        # Extract data from Highcharts
        chart_data = page.evaluate('''() => {
            try {
                const chart = Highcharts.charts[0];
                if (!chart || !chart.series[0]) return [];
                
                return chart.series[0].data.map(point => {
                    const date = new Date(point.x);
                    return {
                        date: date.toISOString().slice(0,7),
                        price: point.y
                    };
                });
            } catch (error) {
                console.error('Chart extraction error:', error);
                return [];
            }
        }''')

        if chart_data:
            data = [d for d in chart_data if d['price'] is not None]
            print(f"Extracted {len(data)} data points")
            if data:
                print(f"Data range: {data[0]['date']} to {data[-1]['date']}")
        
        browser.close()
    
    return pd.DataFrame(data)

# Create directory if not exists
os.makedirs('data/raw', exist_ok=True)

# Get and save data
try:
    df = get_gasoline_data()
    if not df.empty:
        print("Successfully retrieved data:")
        print(df.head())
        df.to_csv('data/raw/vietnam_gasoline_prices.csv', index=False)
        print(f"Saved {len(df)} records to CSV")
    else:
        print("No valid data retrieved")
except Exception as e:
    print("Error occurred:", e)