# 1. Cover Page

**CAPSTONE PROJECT REPORT**
<br><br>
**ON**
<br><br>
**AI-Driven Multi-Asset Trading System with Predictive Modeling, Sentiment Analysis, and Portfolio Optimization**
<br><br>
**Submitted in partial fulfillment of the requirements for the award of the degree of**
<br><br>
**Bachelor of Technology**
<br>
**in**
<br>
**Computer Science and Engineering**
<br><br>
**By:**
<br>
[Student Name 1] (Reg. No: [12345678])
<br>
[Student Name 2] (Reg. No: [12345679])
<br><br>
**Under the Guidance of:**
<br>
[Mentor Name, Designation]
<br><br>
**Course Code:** [Course Code, e.g., CSE441]
<br><br>
**School of Computer Science and Engineering**
<br>
**LOVELY PROFESSIONAL UNIVERSITY**
<br>
**Phagwara, Punjab**
<br>
**(Year: 2026)**

---

# 2. Inner Page

*(This page is an exact replica of the Cover Page. Please duplicate the Cover Page here when finalizing your Word document.)*

---

# 3. PAC Form

**PROJECT APPROVAL COMMITTEE (PAC) FORM**

- **Project Title:** AI-Driven Multi-Asset Trading System with Predictive Modeling, Sentiment Analysis, and Portfolio Optimization
- **Student Details:**
  1. [Name 1] - [Registration No.]
  2. [Name 2] - [Registration No.]
- **Mentor Name:** [Mentor Name]
- **Domain:** Artificial Intelligence / Financial Technology (FinTech)
- **Problem Domain:** Algorithmic Trading & Portfolio Management

**Signatures:**
<br><br>
[Signature of Student 1] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Signature of Student 2]
<br><br>
[Signature of Mentor] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [Signature of PAC Member]

---

# 4. Declaration

**DECLARATION**

We, [Student Name 1] and [Student Name 2], hereby declare that the capstone project entitled **"AI-Driven Multi-Asset Trading System with Predictive Modeling, Sentiment Analysis, and Portfolio Optimization"** submitted to Lovely Professional University, Phagwara, is a record of an original work done by us under the guidance of [Mentor Name]. This project is submitted in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering. The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma.

<br><br>
**Date:** [Date]
<br>
**Place:** Phagwara, Punjab
<br><br>
[Signature of Student 1] ([Student Name 1] - [Reg. No.])
<br>
[Signature of Student 2] ([Student Name 2] - [Reg. No.])

---

# 5. Certificate

**CERTIFICATE**

This is to certify that the capstone project report entitled **"AI-Driven Multi-Asset Trading System with Predictive Modeling, Sentiment Analysis, and Portfolio Optimization"** submitted by [Student Name 1] ([Reg. No.]) and [Student Name 2] ([Reg. No.]) to Lovely Professional University, Phagwara, in partial fulfillment of the requirement for the award of the degree of Bachelor of Technology in Computer Science and Engineering, is a bonafide record of work carried out by them under my supervision. The contents of this report, in full or in parts, have not been submitted to any other Institute or University for the award of any degree or diploma.

<br><br>
**[Signature of Mentor]**
<br>
**[Mentor Name]**
<br>
[Designation]
<br>
School of Computer Science and Engineering
<br>
Lovely Professional University

---

# 6. Acknowledgement

**ACKNOWLEDGEMENT**

We express our deepest gratitude to our mentor, **[Mentor Name]**, for their continuous guidance, valuable feedback, and encouragement throughout the duration of this Capstone Project. Their expertise and support were instrumental in the successful completion of this research and development.

We also wish to thank the **School of Computer Science and Engineering, Lovely Professional University**, for providing us with the resources, environment, and curriculum necessary to undertake a project of this magnitude. 

Lastly, we are grateful to our families and peers for their unwavering moral support.

<br>
[Student Name 1]
<br>
[Student Name 2]

---

# 7. Table of Contents

1. INTRODUCTION
2. PROFILE OF THE PROBLEM
3. EXISTING SYSTEM
4. PROBLEM ANALYSIS
5. SOFTWARE REQUIREMENT ANALYSIS
6. DESIGN
7. TESTING
8. IMPLEMENTATION
9. PROJECT LEGACY
10. USER MANUAL
11. SYSTEM SNAPSHOTS
12. BIBLIOGRAPHY

---

# 1. INTRODUCTION

## 1.1 Overview of Financial Markets
The global financial market is a complex ecosystem where assets such as equities, commodities, and derivatives are traded. Market prices are driven by an intricate combination of historical momentum, macroeconomic indicators, and public sentiment. Traditionally, analyzing these factors required extensive manual labor, making it difficult for individual investors to compete with institutional trading firms.

## 1.2 Role of AI in Trading
Artificial Intelligence (AI) and Machine Learning (ML) have revolutionized modern finance. Through Predictive Modeling (such as LSTMs and Random Forests) and Natural Language Processing (NLP), systems can now digest millions of data points and news articles in seconds. AI provides objective, data-driven insights that mitigate human biases and emotional trading.

## 1.3 Motivation of the Project
Retail investors frequently struggle with building balanced portfolios because they lack access to institutional-grade analytics. Furthermore, investors often have to use separate platforms for analysis and trade execution. The motivation behind this project is to democratize advanced quantitative analysis by building an accessible, intelligent trading dashboard capable of analyzing multiple assets simultaneously and executing trades live within a single integrated environment.

## 1.4 Objectives
- To develop a multi-asset data pipeline that aggregates historical pricing and technical indicators.
- To implement NLP-based sentiment analysis using FinBERT to evaluate financial news via NewsAPI.
- To train predictive ML models to forecast price trends.
- To engineer a Portfolio Optimizer that calculates risk, expected return, and dynamically allocates capital.
- To integrate a live Broker API (Alpaca) for seamless real-time paper and live trade execution.
- To present all insights via an intuitive, interactive, premium Streamlit dashboard.

---

# 2. PROFILE OF THE PROBLEM

## 2.1 Problem Statement
To design and develop an intelligent, multi-asset portfolio management system that leverages machine learning and sentiment analysis to generate actionable BUY/SELL/HOLD signals and dynamically allocates capital to maximize returns while mitigating risk, complete with a live execution interface.

## 2.2 Limitations of Manual Trading
- **Information Overload:** Human traders cannot efficiently process thousands of news articles and price ticks simultaneously.
- **Emotional Bias:** Fear and greed often lead to suboptimal trading decisions.
- **Platform Fragmentation:** Users must analyze data on one platform and execute trades on a completely separate broker application.

## 2.3 Need for an AI-Based System
An AI-driven system solves the aforementioned limitations by replacing human emotion with statistical probability. A computerized Decision Engine can evaluate multiple indicators (RSI, MACD) and sentiment scores concurrently, applying a strict, weighted heuristic to determine the optimal entry and exit points for various assets, and then instantly execute the trade without human hesitation.

## 2.4 Scope of Study
This project focuses on the U.S. Equity market (e.g., AAPL, TSLA, MSFT). It encompasses historical data fetching, technical feature engineering, sentiment analysis of headlines, predictive modeling, portfolio capital optimization, and direct API trade execution using the Alpaca Broker API. The scope covers the backend computational pipeline and the frontend web dashboard, culminating in cloud deployment.

---

# 3. EXISTING SYSTEM

## 3.1 Traditional Trading Systems
Current retail systems (e.g., standard brokerage apps) act purely as execution platforms. They provide raw charting capabilities and historical data but place the entire analytical burden on the user.

## 3.2 Existing Tools and Basic Bots
There are basic algorithmic bots that execute trades based on simple crossovers (e.g., 50-day moving average crossing a 200-day moving average). Additionally, some platforms offer isolated sentiment scores or standalone AI price predictions.

## 3.3 Limitations of Existing Systems
- **Isolated Analysis:** Most tools do not combine technical indicators with NLP sentiment analysis.
- **Execution Disconnect:** Analytics platforms rarely feature embedded execution engines.
- **Lack of Capital Allocation Guidance:** Existing systems tell a user *what* to buy, but rarely *how much* capital to allocate based on risk-adjusted models.

## 3.4 What is New in Your System
Our system introduces a cohesive **AI Portfolio Manager and Execution Engine**. It synthesizes technical trend analysis, ML predictions, and FinBERT sentiment into a unified **Confidence Score**. Furthermore, it utilizes a rigorous **Heuristic Allocation Engine** to mathematically distribute capital across multiple assets based on expected returns and historical volatility. Finally, a seamlessly integrated **Manual Trade Module** allows users to route trades directly to Alpaca without leaving the application.

---

# 4. PROBLEM ANALYSIS

## 4.1 Product Definition
The proposed product is a web-based "AI Trading Platform and Portfolio Manager". It operates as a strategic advisor and broker proxy, presenting users with an overview of their selected assets, identifying top opportunities, suggesting precise portfolio weightings, and providing the tools to execute trades securely.

## 4.2 Feasibility Analysis
- **Technical Feasibility:** Highly feasible. The system relies on proven open-source libraries (Python, Pandas, Scikit-learn, TensorFlow/PyTorch, Streamlit). Live execution is achieved securely via Alpaca APIs.
- **Economic Feasibility:** The project utilizes free-tier APIs (NewsAPI, Alpaca Paper Trading) and open-source models (FinBERT). The financial cost of development and hosting is zero.
- **Operational Feasibility:** The system is operationally viable. The use of a precomputed CSV architecture ensures that the heavy ML training happens offline, while the web dashboard (and live API trade tracking) remains highly responsive for the end-user.

## 4.3 Project Planning
1. **Phase 1:** Setup Data Fetcher and Technical Indicators.
2. **Phase 2:** Integrate Sentiment Analysis (FinBERT/NewsAPI).
3. **Phase 3:** Train ML Models (LSTM/XGBoost).
4. **Phase 4:** Develop AI Decision and Risk Allocation Engines.
5. **Phase 5:** Build Premium Streamlit Dashboard with Routing.
6. **Phase 6:** Integrate Alpaca for Live & Paper Trade Execution.
7. **Phase 7:** Testing, Optimization, and Deployment.

---

# 5. SOFTWARE REQUIREMENT ANALYSIS

## 5.1 Functional Requirements
- **Multi-Asset Analysis:** The system must accept multiple ticker symbols and process them concurrently.
- **Sentiment Analysis:** The system must evaluate news headlines and return a normalized sentiment score.
- **Prediction Models:** The system must predict the expected return of an asset over the next timeframe.
- **Portfolio Allocation:** The system must calculate historical volatility (risk) and recommend a percentage capital allocation.
- **Trade Execution:** The system must allow users to execute Market, Limit, and Stop orders via the Alpaca API.
- **Access Control:** The system must secure the dashboard via a Login Portal.

## 5.2 Non-Functional Requirements
- **Performance:** The web dashboard must load within 3 seconds using cached data.
- **Security:** API keys and trade logic must be secured via `.env` variables and session state authentication.
- **Usability:** The UI must feature premium fintech aesthetics, including glassmorphism, responsive grids, and strict safety confirmations before executing trades.

---

# 6. DESIGN

## 6.1 System Architecture
The system follows a modular, decoupled architecture:
1. **Data Layer:** Fetches raw data (`yfinance`) and computes technical indicators (`ta`).
2. **Sentiment Engine:** Processes text data via `transformers` (FinBERT) using the `NewsAPI`.
3. **Machine Learning Layer:** Uses Scikit-learn/TensorFlow to train predictive models on the merged dataset.
4. **Strategy & Broker Layer:** Analyzes predictions and risk, and routes trade orders via `PaperTradingEngine` or `LiveTradingEngine` (Alpaca).
5. **Presentation Layer:** A premium Streamlit web application with advanced routing (Landing -> Login -> Dashboard).

## 6.2 Application Routing & Workflow
1. User lands on the **Home / Landing Page** detailing platform features.
2. User clicks "Get Started" and is routed to the **Secure Login Portal**.
3. Upon authentication, the **Dashboard** is unlocked.
4. The user interacts with the **Sidebar**, which toggles modular views:
   - *Portfolio Manager* (AI Allocations)
   - *Trade Execution Panel* (Live Alpaca Orders)
   - *Prediction & Analysis* (LSTM Charts)

## 6.3 Pseudocode Examples

**Secure Routing Protocol:**
```text
IF user accesses "Dashboard":
    IF session.authenticated IS FALSE:
        redirect to "Login"
    ELSE:
        render_dashboard()
```

**Trade Execution Flow:**
```text
FUNCTION execute_trade(symbol, quantity, action):
    IF action == "BUY" AND account.buying_power >= (quantity * current_price):
        SHOW confirmation_dialog
        IF confirmed:
            broker_api.place_order(symbol, quantity, action)
            log_trade_history()
            refresh_account_balances()
    ELSE:
        SHOW error("Insufficient Buying Power")
```

---

# 7. TESTING

## 7.1 Unit Testing
Individual modules were tested in isolation. 
- The `RiskAnalyzer` was fed mock data with a known standard deviation to verify the annualized volatility math.
- The `BrokerAPI` was tested to gracefully fall back to local "Mock Mode" if `.env` keys were missing.

## 7.2 Integration Testing
The interaction between the Streamlit Session State and the Trade Execution Engine was heavily tested to ensure that executing a trade immediately refreshes the user's Buying Power and Open Positions without requiring a manual page reload.

## 7.3 System Testing
The entire pipeline was run end-to-end. We verified that unauthenticated users could not access the dashboard by manipulating URL query parameters, ensuring platform security.

## 7.4 Results and Observations
By strictly utilizing native Streamlit layout components rather than heavy HTML/CSS injections for the core UI, the application remained exceptionally stable. A specialized CSS block was utilized exclusively for the global glassmorphism footer and Glowing Action Buttons, achieving a premium aesthetic without risking UI corruption.

---

# 8. IMPLEMENTATION

## 8.1 Tools & Technologies Used
- **Language:** Python 3.10+
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** TensorFlow (Keras), Scikit-learn, XGBoost
- **Natural Language Processing:** HuggingFace Transformers (FinBERT), VADER
- **Web Framework:** Streamlit (with custom Glassmorphism CSS styling)
- **Data & Broker APIs:** Yahoo Finance (`yfinance`), NewsAPI, Alpaca Trading API

## 8.2 Deployment Setup
To deploy on **Render (Web Service)** while bypassing strict Free Tier memory limits:
- The heavy ML pipeline (`main.py`) runs offline/locally to generate signals.
- The lightweight Streamlit app reads pre-computed CSV files and handles live API broker calls instantly.
- Environment variables (`NEWS_API_KEY`, `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`) are stored securely on the server.

## 8.3 Execution Steps
1. Execute `python main.py --tickers AAPL,TSLA,MSFT` to compute portfolio data.
2. Start the dashboard via `python3 -m streamlit run app/streamlit_app.py`.
3. Log in using the secure credential portal.
4. Access the Trade Execution engine to send orders directly to Alpaca.

---

# 9. PROJECT LEGACY

## 9.1 Current Status
The project is fully functional and production-ready. It successfully aggregates multiple assets, computes advanced predictive metrics, distributes capital via an intelligent optimizer, securely handles user sessions, and seamlessly executes live/paper trades directly against a brokerage account.

## 9.2 Limitations
- The predictive system currently relies on static end-of-day data rather than real-time intraday tick data (though the Trade Execution engine fetches live pricing upon execution).
- The portfolio optimizer utilizes a heuristic risk-adjusted weighting model rather than a strict Markowitz Mean-Variance Optimization.

## 9.3 Future Scope
- **Live Trading Automation:** Transition from a Manual Trade Execution panel to fully autonomous, algorithm-driven executions (bot trading).
- **Crypto Support:** Expand the data fetcher and broker API to include cryptocurrency exchanges like Binance or Coinbase.
- **Multi-User Database:** Add a SQL database (like PostgreSQL) to allow thousands of users to track their distinct portfolios instead of relying on session state.

## 9.4 Lessons Learned
- Handling multiple heavy ML frameworks (TensorFlow + PyTorch) simultaneously requires strict memory and thread management to avoid crashes.
- Utilizing Streamlit's `st.session_state` is incredibly powerful for building Single Page Application (SPA) architectures and multi-step routing.

---

# 10. USER MANUAL

## 10.1 Running the System
1. Open the terminal and activate the virtual environment (`source venv/bin/activate`).
2. Run the pipeline: `python main.py --tickers AAPL,TSLA,NVDA`
3. Launch the UI: `python3 -m streamlit run app/streamlit_app.py`

## 10.2 Navigation & Login
Upon opening the application, you will see the Landing Page. Click **Get Started** or **Login** in the Navbar. Enter the demo credentials (Username: `admin`, Password: `admin123`) to unlock the secure dashboard.

## 10.3 Manual Trade Execution
Navigate to the **💱 Trade (Buy / Sell)** tab in the sidebar. Select your desired asset, observe the live price, and input your quantity. Click the **BUY** or **SELL** button to spawn a confirmation dialog. Upon confirmation, the trade will be sent directly to your Alpaca account, and your new Buying Power and Open Positions will update instantly on the screen.

---

# 11. SYSTEM SNAPSHOTS

*(In your final Word document, insert actual screenshots here based on these descriptions)*

**11.1 Landing & Login Portal**
*Description:* A snapshot showing the premium landing page and the secure, centrally aligned Login Portal required to access the dashboard.

**11.2 Trade Execution Engine**
*Description:* A snapshot of the Trade Panel displaying the Live Asset Price, Quantity Inputs, Glowing Buy/Sell action buttons, the Confirmation Dialog, and the Live Account Balance overview fetched from Alpaca.

**11.3 The AI Portfolio Manager Overview**
*Description:* A snapshot showing the AI Capital Allocation Recommendation Pie Chart alongside critical Portfolio Metrics (Total Expected Return, Portfolio Volatility, Diversification Score).

---

# 12. BIBLIOGRAPHY

1. Brownlee, J. (2018). *Deep Learning for Time Series Forecasting*. Machine Learning Mastery.
2. Araci, D. (2019). *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models*. arXiv preprint arXiv:1908.10063.
3. Alpaca Trading API Documentation: *https://alpaca.markets/docs/*
4. Yahoo Finance API Documentation (`yfinance` library).
5. Streamlit Documentation: *https://docs.streamlit.io/*
6. Markowitz, H. (1952). *Portfolio Selection*. The Journal of Finance, 7(1), 77-91. (Reference for Risk/Return paradigms).
