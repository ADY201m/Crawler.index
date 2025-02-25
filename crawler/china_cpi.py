from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os

def get_china_cpi(output_dir='data/raw/'):
    """
    Retrieves China's Consumer Price Index (CPI) historical data from Investing.com
    and saves it to a CSV file in the specified directory.
    
    Args:
        output_dir (str): Directory path where the CSV file will be saved
        
    Returns a dictionary with a 'china_cpi' key containing a DataFrame of historical data
    or an error message if unsuccessful.
    """
    url = 'https://www.investing.com/economic-calendar/chinese-cpi-459'
    result = {'china_cpi': None}
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"china_cpi.csv")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            # Navigate to page with extended timeout
            page.goto(url, timeout=120000, wait_until='domcontentloaded')

            # Handle cookie consent
            try:
                page.click('button#onetrust-accept-btn-handler', timeout=5000)
            except Exception:
                pass

            # Wait for history table to load
            page.wait_for_selector('#eventHistoryTable459', timeout=30000)

            # Improved "Show More" handling
            max_clicks = 30  # Adjust based on expected clicks
            click_count = 0
            previous_row_count = 0

            while click_count < max_clicks:
                # Check if button is present and visible
                show_more_btn = page.query_selector('#showMoreHistory459 a:visible')
                if not show_more_btn:
                    print("No more visible 'Show More' button.")
                    break

                # Get current row count
                current_row_count = len(page.query_selector_all('#eventHistoryTable459 tbody tr'))
                print(f"Current rows before click: {current_row_count}")

                if current_row_count == previous_row_count:
                    print("Row count didn't increase after previous click. Exiting.")
                    break

                try:
                    # Click using JavaScript to bypass potential overlay issues
                    page.evaluate('document.querySelector("#showMoreHistory459 a").click()')
                    # Wait for new rows to load with increased timeout
                    page.wait_for_function(
                        f"document.querySelectorAll('#eventHistoryTable459 tbody tr').length > {current_row_count}",
                        timeout=45000
                    )
                    click_count += 1
                    new_row_count = len(page.query_selector_all('#eventHistoryTable459 tbody tr'))
                    print(f"Successfully clicked {click_count} times. New row count: {new_row_count}")
                    previous_row_count = current_row_count
                except Exception as e:
                    print(f"Error during click/wait: {str(e)}")
                    break

            # Final data extraction
            table = page.query_selector('#eventHistoryTable459')
            headers = [th.inner_text().strip() for th in table.query_selector_all('thead th')[:5]]
            data = []

            for row in table.query_selector_all('tbody tr'):
                cells = row.query_selector_all('td')
                if len(cells) < 5:
                    continue

                # Parse release date and reference month
                date_text = cells[0].inner_text().strip()
                date_parts = date_text.split(' (')
                release_date = pd.to_datetime(date_parts[0], format='%b %d, %Y', errors='coerce')
                reference_month = date_parts[1][:-1] if len(date_parts) > 1 else None

                # Parse actual value and status
                actual_span = cells[2].query_selector('span')
                actual_value = actual_span.inner_text().strip() if actual_span else None
                actual_status = actual_span.get_attribute('title') if actual_span else None

                data.append({
                    'Release Date': release_date,
                    'Reference Month': reference_month,
                    'Time': cells[1].inner_text().strip(),
                    'Actual': actual_value,
                    'Actual Status': actual_status,
                    'Forecast': cells[3].inner_text().strip(),
                    'Previous': cells[4].inner_text().strip()
                })

            browser.close()

            # Create DataFrame
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values('Release Date', ascending=False).reset_index(drop=True)
                
                # Convert numeric columns
                for col in ['Actual', 'Forecast', 'Previous']:
                    df[col] = pd.to_numeric(df[col].str.replace('%', '', regex=False), errors='coerce') / 100
                
                # Save to CSV file
                df.to_csv(output_file, index=False)
                print(f"Data successfully saved to {output_file}")
                
                result['china_cpi'] = df
            else:
                result['china_cpi'] = 'No data found'

    except Exception as e:
        result['china_cpi'] = f'Error during scraping: {str(e)}'

    return result, output_file

# Example usage
if __name__ == "__main__":
    data, saved_file_path = get_china_cpi()
    
    if isinstance(data['china_cpi'], pd.DataFrame):
        print(f"Retrieved {len(data['china_cpi'])} records")
        print(f"Data saved to {saved_file_path}")
        print("Latest 5 entries:")
        print(data['china_cpi'].head(5))
    else:
        print("Error:", data['china_cpi'])