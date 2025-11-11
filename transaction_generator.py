import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configuration
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 11, 4)
START_ID = 10001

# Category structure with realistic subcategories and amount ranges
CATEGORIES = {
    'Food': {
        'subcategories': ['Groceries', 'Restaurants', 'Fast Food', 'Delivery', 'Coffee Shop', 'Bakery'],
        'amount_range': (50, 1000),
        'frequency': 25  # transactions per month
    },
    'Travel': {
        'subcategories': ['Fuel', 'Ride-share', 'Public Transport', 'Parking', 'Taxi', 'Flight', 'Hotel'],
        'amount_range': (50, 2500),
        'frequency': 15
    },
    'Shopping': {
        'subcategories': ['Clothing', 'Electronics', 'Online', 'Household', 'Personal Care', 'Books'],
        'amount_range': (500, 10000),
        'frequency': 5
    },
    'Entertainment': {
        'subcategories': ['Movies', 'Streaming', 'Gaming', 'Events', 'Sports', 'Hobbies'],
        'amount_range': (100, 5000),
        'frequency': 4
    },
    'Bills': {
        'subcategories': ['Electricity', 'Water', 'Internet', 'Phone', 'Gas', 'Rent', 'Insurance'],
        'amount_range': (1000, 10000),
        'frequency': 1
    },
    'Healthcare': {
        'subcategories': ['Medical', 'Pharmacy', 'Insurance', 'Gym', 'Wellness'],
        'amount_range': (1000, 10000),
        'frequency': 3
    },
    'Investment': {
        'subcategories': ['Mutual Funds', 'Stocks', 'SIP', 'Crypto'],
        'amount_range': (500, 2000),
        'frequency': 2
    },
    'Salary': {
        'subcategories': ['Monthly Salary', 'Bonus', 'Freelance', 'Reimbursement'],
        'amount_range': (20000, 80000),
        'frequency': 1.5  # Sometimes bonus/freelance
    },
    'Other': {
        'subcategories': ['ATM Withdrawal', 'Transfer', 'Miscellaneous', 'Gifts', 'Donations'],
        'amount_range': (1000, 10000),
        'frequency': 3
    }
}

# Special transaction patterns
RECURRING_TRANSACTIONS = [
    {'category': 'Bills', 'subcategory': 'Rent', 'amount': 20000, 'day_of_month': 1, 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Internet', 'amount': 2000, 'day_of_month': 1, 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Electricity', 'amount': 2000, 'day_of_month': 10, 'has_variation': True},
    {'category': 'Bills', 'subcategory': 'Phone', 'amount': 1000, 'day_of_month': 10, 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Water', 'amount': 500, 'day_of_month': 10, 'has_variation': False},
    {'category': 'Bills', 'subcategory': 'Gas', 'amount': 1000, 'day_of_month': 15, 'has_variation': True},
    {'category': 'Bills', 'subcategory': 'Insurance', 'amount': 500, 'day_of_month': 20, 'has_variation': False},
    {'category': 'Entertainment', 'subcategory': 'Streaming', 'amount': 1500, 'day_of_month': 15, 'has_variation': False},
    {'category': 'Healthcare', 'subcategory': 'Gym', 'amount': 2000, 'day_of_month': 1, 'has_variation': False},
    {'category': 'Investment', 'subcategory': 'SIP', 'amount': 2000, 'day_of_month': 5, 'has_variation': False},
]

def generate_transaction_date(start, end):
    """Generate random date between start and end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def add_time_patterns(date):
    """Add realistic time patterns (weekday vs weekend, time of day)"""
    # More transactions on weekends for shopping/entertainment
    if date.weekday() >= 5:  # Saturday or Sunday
        return random.random() < 0.7  # 70% chance
    return random.random() < 0.5  # 50% chance on weekdays

def generate_amount(category_name, subcategory):
    """Generate realistic amount based on category and subcategory"""
    min_amt, max_amt = CATEGORIES[category_name]['amount_range']
    
    # Add subcategory-specific adjustments
    if subcategory in ['Rent', 'Flight', 'Hotel']:
        amount = random.uniform(max_amt * 0.7, max_amt)
    elif subcategory in ['Coffee Shop', 'Fast Food', 'Public Transport']:
        amount = random.uniform(min_amt, min_amt * 3)
    elif subcategory in ['Monthly Salary']:
        amount = random.uniform(50000, 70000)
    else:
        # Use log-normal distribution for realistic spending (most small, some large)
        mean = (min_amt + max_amt) / 2
        std = (max_amt - min_amt) / 4
        amount = np.random.lognormal(np.log(mean), 0.5)
        amount = max(min_amt, min(amount, max_amt))
    
    return round(amount, 2)

def generate_transactions():
    """Generate all transactions"""
    transactions = []
    transaction_id = START_ID
    
    # Track recurring transactions to avoid duplicates
    recurring_subcategories = set([r['subcategory'] for r in RECURRING_TRANSACTIONS])
    
    # Generate recurring transactions first
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
                    amount = round(recurring['amount'] + variance, 2)
                else:
                    # Use fixed amount for other recurring transactions
                    amount = recurring['amount']
                    
                transactions.append({
                    'transaction_id': transaction_id,
                    'transaction_date': trans_date.strftime('%d/%m/%Y'),
                    'transaction_type': 'Credit' if recurring['category'] == 'Salary' else 'Debit',
                    'amount': round(amount, 2),
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
            # Salary varies slightly
            salary = random.uniform(55000, 65000)
            transactions.append({
                'transaction_id': transaction_id,
                'transaction_date': salary_date.strftime('%d/%m/%Y'),
                'transaction_type': 'Credit',
                'amount': round(salary, 2),
                'category': 'Salary',
                'sub_category': 'Monthly Salary'
            })
            transaction_id += 1
        
        # Occasional bonus/freelance (20% chance per quarter)
        if current_date.month in [3, 6, 9, 12] and random.random() < 0.2:
            bonus_date = generate_transaction_date(
                current_date.replace(day=15),
                current_date.replace(day=28)
            )
            if bonus_date <= END_DATE:
                transactions.append({
                    'transaction_id': transaction_id,
                    'transaction_date': bonus_date.strftime('%d/%m/%Y'),
                    'transaction_type': 'Credit',
                    'amount': round(random.uniform(20000, 50000), 2),
                    'category': 'Salary',
                    'sub_category': random.choice(['Bonus', 'Freelance'])
                })
                transaction_id += 1
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Generate random transactions for each category
    for category_name, category_data in CATEGORIES.items():
        if category_name == 'Salary':  # Already handled
            continue
        
        # Calculate total transactions for this category over 2 years
        total_transactions = int(category_data['frequency'] * 24)  # 24 months
        
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
            if category_name == 'Salary':
                trans_type = 'Credit'
            elif category_name == 'Investment':
                # 90% debit (investing), 10% credit (returns/withdrawal)
                trans_type = 'Debit' if random.random() < 0.9 else 'Credit'
            elif category_name == 'Other' and subcategory == 'Transfer':
                # 50-50 for transfers
                trans_type = random.choice(['Debit', 'Credit'])
            else:
                trans_type = 'Debit'
            
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
print("Generating 2 years of realistic transaction data...")
transactions = generate_transactions()

# Convert to DataFrame and sort by date
df = pd.DataFrame(transactions)
df['date_sort'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y')
df = df.sort_values('date_sort')
df = df.drop('date_sort', axis=1)

# Reset transaction IDs to be sequential
df['transaction_id'] = range(START_ID, START_ID + len(df))

# Display statistics
print(f"\n✅ Generated {len(df)} transactions")
print(f"📅 Date Range: {df['transaction_date'].iloc[0]} to {df['transaction_date'].iloc[-1]}")
print(f"\n📊 Transaction Type Distribution:")
print(df['transaction_type'].value_counts())
print(f"\n💰 Amount Statistics:")
print(df['amount'].describe())
print(f"\n🏷️ Category Distribution:")
print(df['category'].value_counts())

# Calculate total income and expenses
total_credit = df[df['transaction_type'] == 'Credit']['amount'].sum()
total_debit = df[df['transaction_type'] == 'Debit']['amount'].sum()
net_savings = total_credit - total_debit

print(f"\n💵 Financial Summary:")
print(f"Total Income (Credits): ${total_credit:,.2f}")
print(f"Total Expenses (Debits): ${total_debit:,.2f}")
print(f"Net Savings: ${net_savings:,.2f}")
print(f"Savings Rate: {(net_savings/total_credit)*100:.1f}%")

# Save to CSV
csv_filename = 'transactions.csv'
df.to_csv(csv_filename, index=False)
print(f"\n💾 Saved to: {csv_filename}")