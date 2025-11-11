# Personal Finance Tracker - Automated Data Pipeline and Dashboard
## 🧾 Executive Summary
- This project automates personal finance tracking from message-based inputs to interactive financial dashboards.  
- It integrates **Telegram, n8n, AI-powered message parsing, PostgreSQL,** and **Power BI** to deliver real-time financial insights and visual analytics.  
- The pipeline automatically converts unstructured expense messages into structured transactions, stores them in a database, and visualizes key spending metrics.

## 🚩 Problem
Managing personal expenses manually often leads to:
- Missing small but frequent transactions
- Difficulty identifying spending patterns
- Time-consuming data entry and report generation

The goal is to **automate data collection and transform raw transactions into clear, visual insights.**

## 🧠 Methodology

### 1️⃣ Data Generation (Python)
A custom python script ([transaction_generator.py](transaction_generator.py)) simulates 2 years of realistic financial data.  

Features:
- Random yet statistically realistic transaction amounts
- Recurring expenses (e.g., rent, bills, SIPs)
- Variable spending patterns across weekdays/weekends
- Distinction between debit (expenses) and credit (income)

```
python transaction_generator.py
```

This generates [transactions.csv](transactions.csv), which serves as the initial dataset for Power BI and n8n testing.

### 1️⃣ Data Collection (Telegram → n8n)  

Messages sent on Telegram are automatically parsed into structured financial entries via n8n:  

- Transaction details (e.g. “Paid ₹250 for groceries”) are sent on Telegram.
- The n8n workflow triggers automatically when a message is received.
<img src="Screenshots/telegram.png" height="310.5">

### 2️⃣ Data Processing (AI Agent)
A Google Gemini Chat Model node interprets each message and extracts structured fields:

- transaction_date
- transaction_type
- amount
- category
- sub_category

Output is parsed into a JSON structure using the Structured Output Parser.

<img src="Screenshots/n8n_workflow.png" height="300">

### 3️⃣ Data Storage (PostgreSQL on Supabase)
- Parsed transactions are inserted into the ``transactions`` table in PostgreSQL with auto-incrementing ``transaction_id``.
- Schema:
<img src="Screenshots/postgres(supabase).png" height="250">

- A confirmation message is sent back to Telegram once a transaction is logged.

### 4️⃣ Data Visualization (Power BI)
- Power BI connects directly to the Supabase PostgreSQL database.
- It provides interactive dashboards for:
  - Expense distribution by category
  - Spending trends over time
  - Weekday vs. weekend spending
  - Key KPIs like **average daily expense, monthly spend,** and **average transactions per day**
<img src="Screenshots/dashboard.png" height="350">


## 🧰 Skills Demonstrated
- **Data Analytics:** Power BI (DAX, measures, visuals)
- **Data Engineering**: n8n workflow automation, Supabase (PostgreSQL)
- **Data Processing**: Prompt engineering, structured output parsing, AI-based NLP extraction
- **Data Simulation**: Python (NumPy, pandas, random distributions)
- **Database Design**: SQL schema design, identity columns, sequence management
- **ETL Automation**: No-code pipeline from Telegram → n8n → PostgreSQL → Power BI
- **Soft Skills**: Problem-solving, data storytelling, automation mindset 


## 📈 Results & Impact
- **Saved 90–95% of manual tracking time** — reduced daily expense logging from 20-30 min to under 1 min using n8n automation.
- **Achieved 100% accurate, real-time recording** of transactions through Telegram → AI → PostgreSQL pipeline.
- **Two years of complete, structured financial data** now available for continuous analytics and forecasting.
- **Identified key spending insights:**
  - Food was the **largest expense category** (~37% of transactions).
  - Weekend spending was **~15% higher** than weekdays.
  - Fixed bills and subscriptions showed **stable monthly recurrence.**
- **Improved financial awareness** — instant Telegram confirmations and Power BI visuals encouraged disciplined spending.
- **Data-driven budgeting decisions** enabled—clear visibility into expense trends, top categories, and saving potential.
- **Foundation for predictive analytics** — dataset prepared for future ML models (spending forecasts, anomaly detection, behavior clustering).


## 🔮 Next Steps:
- **Predict Future Spending:** Build time-series models to forecast monthly expenses and income trends.
- **Category-Level Forecasting:** Use regression models to anticipate spending by category (e.g., Food, Travel, Bills).
- **Anomaly Detection:** Implement ML models (Isolation Forest) to flag irregular or unusually high expenses.
- **User Segmentation:** Apply clustering (K-Means) to identify behavior patterns like “Saver” vs “Weekend Spender.”
