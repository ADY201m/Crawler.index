# Vietnam Inflation Prediction Project

This project collects, scrapes, and processes economic data from various sources (e.g., Tổng cục Thống kê, Ngân hàng Nhà nước, Bộ Tài chính, Petrolimex, EIA, FAO, etc.) to predict inflation trends in Vietnam. The project is built using Node.js with the Crawlee framework and PostgreSQL as the data store (using Aiven VM for the DB).

## Project Structure

```
inflation-prediction-project/

├── crawlers/
│   ├── gso/                      # Tổng cục Thống kê (GSO) crawlers (https://www.gso.gov.vn/en/statistical-data/) 
│   │   ├── cpi_crawler           # Chỉ số giá tiêu dùng (CPI) 
│   │   ├── core_inflation        # Lạm phát cơ bản
│   │   ├── food_price_inflation  # Lạm phát giá lương thực
│   │   ├── industrial_production # Chỉ số sản xuất công nghiệp
│   │   ├── exports_crawler       # Xuất khẩu 
│   │   ├── imports_crawler       # Nhập khẩu
│   │   └── unemployment_rate     # Tỷ lệ thất nghiệp
│   │
│   ├── investing/                # Investing.com
│   |   ├── exchange_rate         # Tỷ giá USD/VND (https://www.investing.com/currencies/usd-vnd-historical-data) (done)
│   │   └── gold_price            # Giá vàng (https://vn.investing.com/commodities/gold-historical-data)
│   │   └── brent_crude           # Giá dầu Brent (https://vn.investing.com/commodities/brent-oil-historical-data)
│   │   └── china_cpi             # Lạm phát Trung Quốc (https://www.investing.com/economic-calendar/chinese-cpi-459)
│   │
│   └── trading_economics/     # Trading Economics
│       ├── coffee_price       # Giá cà phê (https://tradingeconomics.com/commodity/coffee)
│       ├── gasoline_price     # Giá xăng (https://tradingeconomics.com/vietnam/gasoline-prices)
│       ├── money_supply       # Cung tiền M2 (https://tradingeconomics.com/vietnam/money-supply-m2)
│       ├── fiscal_deficit     # Thâm hụt ngân sách (https://tradingeconomics.com/vietnam/fiscal-expenditure)
│       ├── rice_price         # Giá gạo (https://tradingeconomics.com/vietnam/exports/china/rice)
│   │   ├── trade_balance      # Cán cân thương mại (https://tradingeconomics.com/vietnam/balance-of-trade)
│       └── policy_interest_rate  # Lãi suất cơ bản (https://tradingeconomics.com/vietnam/interest-rate)

│
├── data/
│   ├── raw/                      # Raw data dumps from crawlers (organized by source)
│   │   ├── gso/
│   │   ├── investing/
│   │   └── trading_economics/
│   └── processed/                # Cleaned and normalized data ready for analysis
│ 
└── README.md                     # Project overview and documentation
```

