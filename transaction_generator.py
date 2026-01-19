import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)
START_ID = 10001
MONTHLY_SALARY = 50000  # Fixed salary

# Helper function to round numbers
def round_to_nice_number(amount):
    """Round amounts to nice numbers like 100, 150, 175, 200, 250, etc."""
    if amount < 50:
        # Round to nearest 5 or 10
        return round(amount / 5) * 5
    elif amount < 100:
        # Round to nearest 10
        return round(amount / 10) * 10
    elif amount < 500:
        # Round to nearest 25
        return round(amount / 25) * 25
    elif amount < 1000:
        # Round to nearest 50
        return round(amount / 50) * 50
    else:
        # Round to nearest 100
        return round(amount / 100) * 100

# Category structure with realistic subcategories and amount ranges
CATEGORIES = {
    'Food': {
        'subcategories': ['Groceries', 'Restaurants', 'Fast Food', 'Delivery', 'Coffee Shop', 'Bakery'],
        'amount_range': (50, 300),
        'frequency': 18  # Transactions per month
    },
    'Travel': {
        'subcategories': ['Fuel', 'Ride-share', 'Public Transport', 'Parking', 'Taxi', 'Flight', 'Hotel'],
        'amount_range': (50, 500),
        'frequency': 10
    },
    'Shopping': {
        'subcategories': ['Clothing', 'Electronics', 'Online', 'Household', 'Personal Care', 'Books'],
        'amount_range': (100, 800),
        'frequency': 8
    },
    'Entertainment': {
        'subcategories': ['Movies', 'Streaming', 'Gaming', 'Events', 'Sports', 'Hobbies'],
        'amount_range': (50, 250),
        'frequency': 6
    },
    'Bills': {
        'subcategories': ['Electricity', 'Internet', 'Phone', 'Gas', 'Rent', 'Insurance'],
        'amount_range': (100, 1500),
        'frequency': 8
    },
    'Healthcare': {
        'subcategories': ['Medical', 'Pharmacy', 'Insurance', 'Gym', 'Wellness'],
        'amount_range': (100, 400),
        'frequency': 4
    },
    'Investment': {
        'subcategories': ['Mutual Funds', 'Stocks', 'Fixed Deposit', 'SIP', 'Crypto'],
        'amount_range': (500, 2000),
        'frequency': 4
    },
    'Salary': {
        'subcategories': ['Monthly Salary', 'Bonus', 'Freelance', 'Reimbursement'],
        'amount_range': (50000, 50000),
        'frequency': 1
    },
    'Investment Returns': {
        'subcategories': ['Dividend', 'Interest', 'Capital Gains', 'Mutual Fund Returns'],
        'amount_range': (500, 3000),
        'frequency': 2  # Occasional returns
    },
    'Other': {
        'subcategories': ['ATM Withdrawal', 'Transfer', 'Miscellaneous', 'Gifts', 'Donations'],
        'amount_range': (100, 500),
        'frequency': 5
    }
}

# Fixed recurring transactions
RECURRING_TRANSACTIONS = [
    {'category': 'Bills', 'subcategory': 'Rent', 'amount': 12000, 'day_of_month': 1, 'type': 'Expense', 'has_variation': False},
    {'category': 'Healthcare', 'subcategory': 'Gym', 'amount': 500, 'day_of_month': 1, 'type': 'Expense', 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Internet', 'amount': 600, 'day_of_month': 5, 'type': 'Expense', 'has_variation': False},
    {'category': 'Investment', 'subcategory': 'SIP', 'amount': 5000, 'day_of_month': 5, 'type': 'Savings', 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Electricity', 'amount': 800, 'day_of_month': 7, 'type': 'Expense', 'has_variation': True},
    {'category': 'Bills', 'subcategory': 'Phone', 'amount': 400, 'day_of_month': 10, 'type': 'Expense', 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Gas', 'amount': 600, 'day_of_month': 12, 'type': 'Expense', 'has_variation': False},
    {'category': 'Entertainment', 'subcategory': 'Streaming', 'amount': 200, 'day_of_month': 15, 'type': 'Expense', 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Insurance', 'amount': 1500, 'day_of_month': 20, 'type': 'Expense', 'has_variation': False},
]

def generate_transaction_date(start, end):
    # Random date between start and end
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def generate_amount(category_name, subcategory):
    # Realistic rounded amount based on category and subcategory
    min_amt, max_amt = CATEGORIES[category_name]['amount_range']
    
    # Subcategory-specific adjustments
    if subcategory in ['Rent', 'Flight', 'Hotel']:
        amount = random.uniform(max_amt * 0.7, max_amt)
    elif subcategory in ['Coffee Shop', 'Fast Food', 'Public Transport']:
        amount = random.uniform(min_amt, min_amt * 2)
    elif subcategory in ['Monthly Salary']:
        amount = MONTHLY_SALARY
    else:
        # Uniform distribution for simpler amounts
        amount = random.uniform(min_amt, max_amt)
    
    # Round to nice number
    return round_to_nice_number(amount)

def generate_transactions():
    # Generating all transactions
    transactions = []
    transaction_id = START_ID
    
    # Tracking recurring transactions to avoid duplicates
    recurring_subcategories = set([r['subcategory'] for r in RECURRING_TRANSACTIONS])
    
    # Generating recurring transactions first
    current_date = START_DATE
    while current_date <= END_DATE:
        for recurring in RECURRING_TRANSACTIONS:
            try:
                trans_date = current_date.replace(day=recurring['day_of_month'])
            except ValueError:
                # Handle months with fewer days (e.g., Feb 30)
                trans_date = current_date.replace(day=28)
                
            if trans_date <= END_DATE and trans_date >= START_DATE:
                # Apply variation only if specified
                if recurring.get('has_variation', False):
                    # Add ±15% variation for bills like electricity
                    variance = recurring['amount'] * random.uniform(-0.15, 0.15)
                    amount = round_to_nice_number(recurring['amount'] + variance)
                else:
                    # Use fixed amount for other recurring transactions
                    amount = recurring['amount']
                    
                transactions.append({
                    'transaction_id': transaction_id,
                    'transaction_date': trans_date.strftime('%d/%m/%Y'),
                    'transaction_type': recurring['type'],
                    'amount': amount,
                    'category': recurring['category'],
                    'sub_category': recurring['subcategory']
                })
                transaction_id += 1
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Generate salary on 1st of every month
    current_date = START_DATE
    while current_date <= END_DATE:
        salary_date = current_date.replace(day=1)
        if salary_date <= END_DATE and salary_date >= START_DATE:
            transactions.append({
                'transaction_id': transaction_id,
                'transaction_date': salary_date.strftime('%d/%m/%Y'),
                'transaction_type': 'Income',
                'amount': MONTHLY_SALARY,
                'category': 'Salary',
                'sub_category': 'Monthly Salary'
            })
            transaction_id += 1
        
        # Occasional bonus (10% chance per quarter)
        if current_date.month in [3, 6, 9, 12] and random.random() < 0.1:
            bonus_date = generate_transaction_date(
                current_date.replace(day=15),
                current_date.replace(day=28)
            )
            if bonus_date <= END_DATE:
                bonus_amount = round_to_nice_number(random.uniform(5000, 15000))
                transactions.append({
                    'transaction_id': transaction_id,
                    'transaction_date': bonus_date.strftime('%d/%m/%Y'),
                    'transaction_type': 'Income',
                    'amount': bonus_amount,
                    'category': 'Salary',
                    'sub_category': random.choice(['Bonus', 'Freelance'])
                })
                transaction_id += 1
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Generating random transactions for each category
    for category_name, category_data in CATEGORIES.items():
        if category_name == 'Salary':  # Already handled
            continue
        
        # Calculate total transactions for this category over 3 years
        total_transactions = int(category_data['frequency'] * 36)  # 36 months
        
        for _ in range(total_transactions):
            trans_date = generate_transaction_date(START_DATE, END_DATE)
            
            # Get available subcategories (exclude recurring ones)
            available_subcategories = [
                sub for sub in category_data['subcategories'] 
                if sub not in recurring_subcategories
            ]
            
            # Skip if no available subcategories
            if not available_subcategories:
                continue
                
            subcategory = random.choice(available_subcategories)
            amount = generate_amount(category_name, subcategory)
            
            # Determine transaction type
            if category_name == 'Investment':
                trans_type = 'Savings'
            elif category_name == 'Investment Returns':
                trans_type = 'Income'
            else:
                trans_type = 'Expense'
            
            transactions.append({
                'transaction_id': transaction_id,
                'transaction_date': trans_date.strftime('%d/%m/%Y'),
                'transaction_type': trans_type,
                'amount': amount,
                'category': category_name,
                'sub_category': subcategory
            })
            transaction_id += 1
    
    return transactions

# Generate transactions
print("Generating 3 years of realistic transaction data...")
transactions = generate_transactions()

# Convert to DataFrame and sort by date
df = pd.DataFrame(transactions)
df['date_sort'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y')
df = df.sort_values('date_sort')
df = df.drop('date_sort', axis=1)

# Reset transaction IDs to be sequential
df['transaction_id'] = range(START_ID, START_ID + len(df))

# Display statistics
print(f"\nGenerated {len(df)} transactions")
print(f"Date Range: {df['transaction_date'].iloc[0]} to {df['transaction_date'].iloc[-1]}")

# Save to CSV
csv_filename = 'transactions.csv'
df.to_csv(csv_filename, index=False)
print(f"\nSaved to: {csv_filename}")

# Display sample data
print(f"\nSample Transactions:")
print(df.head(15).to_string(index=False))

print("\nData generation complete!")
