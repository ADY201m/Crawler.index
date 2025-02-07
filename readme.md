# Vietnam Inflation Prediction Project

This project collects, scrapes, and processes economic data from various sources (e.g., Tổng cục Thống kê, Ngân hàng Nhà nước, Bộ Tài chính, Petrolimex, EIA, FAO, etc.) to predict inflation trends in Vietnam. The project is built using Node.js with the Crawlee framework and PostgreSQL as the data store (using Aiven VM for the DB).

## Project Structure

```plaintext
inflation-prediction-project/
├── configs/
│   ├── crawler_config.js         # Global settings for crawlers
│   ├── database_config.js        # DB connection and insertion config
│   ├── proxy_config.js           # Proxy settings if needed
│   ├── scheduler_config.js       # Scheduler and cron job configuration
│   ├── docker-compose.yaml       # Docker deployment settings
│   └── prometheus.yml            # Monitoring configuration
│
├── crawlers/
│   ├── gso/                      # Tổng cục Thống kê (GSO) crawlers
│   │   ├── cpi_crawler.js        # Chỉ số giá tiêu dùng (CPI)
│   │   ├── core_inflation.js     # Lạm phát cơ bản
│   │   ├── food_price_inflation.js  # Lạm phát giá lương thực
│   │   ├── industrial_production.js  # Chỉ số sản xuất công nghiệp
│   │   ├── exports_crawler.js    # Xuất khẩu
│   │   ├── imports_crawler.js    # Nhập khẩu
│   │   ├── trade_balance.js      # Cán cân thương mại
│   │   └── unemployment_rate.js  # Tỷ lệ thất nghiệp
│   │
│   ├── evn/                      # Tập đoàn Điện lực (EVN)
│   │   └── electricity_price.js  # Giá điện
│   │
│   ├── eia/                      # U.S. Energy Information Administration (EIA)
│   │   └── brent_crude.js        # Giá dầu Brent
│   │
│   ├── investing/                # Investing.com
│   │   ├── exchange_rate.js      # Tỷ giá USD/VND
│   │   └── gold_price.js         # Giá vàng
│   │
│   ├── china/                    # National Bureau of Statistics of China
│   │   └── china_cpi.js          # Lạm phát Trung Quốc
│   │
│   ├── imf/                      # IMF
│   │   └── external_shocks.js    # Cú sốc ngoại sinh
│   │
│   └── trading_economics/        # Trading Economics
│       ├── coffee_price.js       # Giá cà phê
│       ├── gasoline_price.js     # Giá xăng
│       ├── money_supply.js       # Cung tiền M2
│       ├── fiscal_deficit.js     # Thâm hụt ngân sách
│       ├── rice_price.js         # Giá gạo
│       └── policy_interest_rate.js  # Lãi suất cơ bản
│
├── parsers/
│   ├── common_parser.js          # Shared parsing utilities and functions
│   ├── gso_parser.js             # Parsing rules for GSO data
│   ├── sbv_parser.js             # Parsing rules for SBV data
│   ├── mof_parser.js             # Parsing rules for MOF data
│   ├── evn_parser.js             # Parsing rules for EVN data
│   ├── petrolimex_parser.js      # Parsing rules for Petrolimex data
│   ├── eia_parser.js             # Parsing rules for EIA data
│   ├── fao_parser.js             # Parsing rules for FAO data
│   ├── investing_parser.js       # Parsing rules for Investing data
│   ├── china_parser.js           # Parsing rules for Chinese data
│   ├── imf_parser.js             # Parsing rules for IMF data
│   └── trading_economics_parser.js  # Parsing rules for Trading Economics data
│
├── data/
│   ├── raw/                      # Raw data dumps from crawlers (organized by source)
│   │   ├── gso/
│   │   ├── sbv/
│   │   ├── mof/
│   │   ├── evn/
│   │   ├── petrolimex/
│   │   ├── eia/
│   │   ├── fao/
│   │   ├── investing/
│   │   ├── china/
│   │   ├── imf/
│   │   └── trading_economics/
│   └── processed/                # Cleaned and normalized data ready for analysis
│
├── scheduler/
│   ├── scheduler.js              # Centralized scheduling for all crawlers
│   └── tasks.js                  # Task definitions for periodic scraping jobs
│
├── utils/
│   ├── logger.js                 # Logging utility (info, error, debug)
│   ├── error_handler.js          # Centralized error handling functions
│   ├── scraper_helpers.js        # Helper functions for scraping tasks
│   ├── data_cleaner.js           # Data cleaning and normalization functions
│   └── db.js                     # Database connection and insertion logic
│
├── tests/
│   ├── test_crawlers/            # Unit tests for crawlers
│   ├── test_parsers/             # Unit tests for parsers
│   └── test_utils/               # Unit tests for utilities
│
├── README.md                     # Project overview and documentation
└── package.json                  # Project dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js (>= 16.x)
- PostgreSQL
- Docker (optional, for deployment)

### Installation

```sh
git clone https://github.com/your-repo/inflation-prediction-project.git
cd inflation-prediction-project
npm install
```

### Running the Crawlers

```sh
npm run start-crawlers
```

### Running the Scheduler

```sh
npm run start-scheduler
```

### Running Tests

```sh
npm test
```