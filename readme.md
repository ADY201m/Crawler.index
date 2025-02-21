# Vietnam Inflation Prediction Project

This project collects, scrapes, and processes economic data from various sources (e.g., Tổng cục Thống kê, Ngân hàng Nhà nước, Bộ Tài chính, Petrolimex, EIA, FAO, etc.) to predict inflation trends in Vietnam. The project is built using Node.js with the Crawlee framework and PostgreSQL as the data store (using Aiven VM for the DB).

## Project Structure

```
inflation-prediction-project/

├── crawlers/
│   ├── gso/                      # Tổng cục Thống kê (GSO) crawlers (https://www.gso.gov.vn/en/statistical-data/) (recheck)
│   │   ├── cpi_crawler.js        # Chỉ số giá tiêu dùng (CPI) 
│   │   ├── core_inflation.js     # Lạm phát cơ bản
│   │   ├── food_price_inflation.js  # Lạm phát giá lương thực
│   │   ├── industrial_production.js  # Chỉ số sản xuất công nghiệp
│   │   ├── exports_crawler.js    # Xuất khẩu 
│   │   ├── imports_crawler.js    # Nhập khẩu
│   │   ├── trade_balance.js      # Cán cân thương mại
│   │   └── unemployment_rate.js  # Tỷ lệ thất nghiệp
│   │
│   ├── investing/                # Investing.com
│   |   ├── exchange_rate.js      # Tỷ giá USD/VND (https://www.investing.com/currencies/usd-vnd-historical-data) (done)
│   │   └── gold_price.js         # Giá vàng (https://vn.investing.com/commodities/gold-historical-data)
│   │   └── brent_crude.js        # Giá dầu Brent (https://vn.investing.com/commodities/brent-oil-historical-data)
│   │   └── china_cpi.js          # Lạm phát Trung Quốc (https://www.investing.com/economic-calendar/chinese-cpi-459)
│   │
│   └── trading_economics/        # Trading Economics
│       ├── coffee_price.js       # Giá cà phê (https://tradingeconomics.com/commodity/coffee)
│       ├── gasoline_price.js     # Giá xăng (https://tradingeconomics.com/vietnam/gasoline-prices)
│       ├── money_supply.js       # Cung tiền M2 (https://tradingeconomics.com/vietnam/money-supply-m2)
│       ├── fiscal_deficit.js     # Thâm hụt ngân sách (https://tradingeconomics.com/vietnam/fiscal-expenditure)
│       ├── rice_price.js         # Giá gạo (https://tradingeconomics.com/commodity/rice)
│       └── policy_interest_rate.js  # Lãi suất cơ bản (https://tradingeconomics.com/vietnam/interest-rate)

│
├── data/
│   ├── raw/                      # Raw data dumps from crawlers (organized by source)
│   │   ├── gso/
│   │   ├── investing/
│   │   ├── imf/
│   │   └── trading_economics/
│   └── processed/                # Cleaned and normalized data ready for analysis
│ 
└── README.md                     # Project overview and documentation
```

