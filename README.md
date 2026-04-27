# AI-Driven Trading System

A complete, production-ready AI-driven trading system built with Python. This system integrates machine learning (LSTM, Random Forest, XGBoost), sentiment analysis (FinBERT, VADER, TextBlob), technical indicators (via `ta`), and a strategy backtesting engine (via `backtrader`). It features an interactive dashboard built with `Streamlit`.

## Features
- **Data Collection**: Automatic fetching of historical data via `yfinance` and financial news via NewsAPI.
- **Feature Engineering**: Extensive technical indicators including Moving Averages, RSI, MACD, and Bollinger Bands.
- **Machine Learning**: Predicts future price action or returns using LSTM, Random Forest, or XGBoost.
- **Sentiment Analysis**: Scrapes news and computes a daily sentiment score.
- **Strategy Engine**: Combines price predictions and sentiment to generate actionable BUY/SELL/HOLD signals.
- **Backtesting**: Validates strategy performance against historical data, calculating Sharpe Ratio and Drawdown.
- **Dashboard**: A comprehensive UI to monitor the market and AI signals.

## Setup Instructions

### 1. Local Environment Setup

Ensure you have Python 3.9+ installed.

```bash
# Clone the repository
git clone <repository_url>
cd ai-trading-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory (optional, but recommended for actual news):
```env
NEWS_API_KEY=your_news_api_key_here
```
If no key is provided, the system will use a synthetic mock news generator for demonstration purposes.

### 3. Running the System

**Step 1: Execute the Pipeline**
Run the orchestrator script to fetch data, train models, generate signals, and perform backtesting.

```bash
# Default run (LSTM model on AAPL)
python main.py

# Specify ticker and model (choices: lstm, rf, xgb)
python main.py --ticker TSLA --model xgb
```

**Step 2: Launch the Dashboard**
Once the pipeline has completed and saved the data, launch the Streamlit dashboard on your localhost:

```bash
streamlit run app/streamlit_app.py
```

## Architecture

- `data/`: Fetches market data and engineers technical features.
- `sentiment/`: Handles news fetching and NLP sentiment analysis.
- `models/`: Contains the ML/DL model implementations.
- `strategy/`: Generates trading signals based on a hybrid logic system.
- `backtesting/`: Simulates historical trades and calculates performance metrics.
- `app/`: Streamlit web interface.
- `config/`: Global settings and API key management.
- `utils/`: Structured logging.

## Disclaimer
This software is for educational and research purposes only. Do not use it for actual trading without extensive forward testing. The authors are not responsible for any financial losses incurred.
