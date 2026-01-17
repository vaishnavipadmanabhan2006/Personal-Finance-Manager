import json
from datetime import datetime
from typing import Dict, Optional
import matplotlib.pyplot as plt

class PersonalFinanceManager:
    def __init__(self, user_name: str):   # ✅ Fixed __init__
        self.user_name = user_name
        self.transactions = []
        self.categories = {
            'income': ['Salary', 'Freelance', 'Investment'],
            'expense': ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping']
        }
        self.load_data()
    
    def add_transaction(self, amount: float, category: str, 
                       transaction_type: str, description: str = ""):
        """Add a new transaction"""
        transaction = {
            'id': len(self.transactions) + 1,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount,
            'category': category,
            'type': transaction_type,  # 'income' or 'expense'
            'description': description
        }
        self.transactions.append(transaction)
        self.save_data()
        print(f"✅ Transaction added: {description} - ${amount}")
    
    def get_balance(self) -> float:
        """Calculate current balance"""
        income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        return income - expense
    
    def generate_report(self, month: Optional[str] = None):
        """Generate spending report with visualization"""
        print(f"\n📊 FINANCIAL REPORT for {self.user_name}")
        print("=" * 40)
        
        # Filter by month if specified
        filtered_transactions = self.transactions
        if month:
            filtered_transactions = [t for t in self.transactions 
                                   if t['date'].startswith(month)]
        
        # Calculate totals
        total_income = sum(t['amount'] for t in filtered_transactions 
                          if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in filtered_transactions 
                           if t['type'] == 'expense')
        
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Current Balance: ${self.get_balance():.2f}")
        print(f"Savings Rate: {(total_income - total_expense)/total_income*100:.1f}%" 
              if total_income > 0 else "N/A")
        
        # Category breakdown
        expense_by_category = {}
        for t in filtered_transactions:
            if t['type'] == 'expense':
                expense_by_category[t['category']] = expense_by_category.get(
                    t['category'], 0) + t['amount']
        
        if expense_by_category:
            print("\n📈 Expense Breakdown:")
            for category, amount in sorted(expense_by_category.items(), 
                                          key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expense * 100) if total_expense > 0 else 0
                print(f"  {category}: ${amount:.2f} ({percentage:.1f}%)")
            
            # Generate visualization
            self.create_pie_chart(expense_by_category)
    
    def create_pie_chart(self, data: Dict):
        """Create visualization of expenses"""
        if not data:
            return
        
        labels = list(data.keys())
        sizes = list(data.values())
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Expense Distribution')
        plt.savefig('expense_distribution.png', dpi=100, bbox_inches='tight')
        print("\n📈 Chart saved as 'expense_distribution.png'")
    
    def set_budget(self, category: str, limit: float):
        """Set spending limits for categories"""
        print(f"Budget set for {category}: ${limit}")
        # Budget tracking logic here
    
    def save_data(self):
        """Save transactions to JSON file"""
        with open('finance_data.json', 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def load_data(self):
        """Load transactions from JSON file"""
        try:
            with open('finance_data.json', 'r') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []

# Interactive usage
def demo_finance_manager():
    print("=" * 50)
    print("PERSONAL FINANCE MANAGER - PYTHON PROJECT")
    print("=" * 50)
    
    name = input("Enter your name: ")
    manager = PersonalFinanceManager(name)
    
    while True:
        print("\nOptions: 1) Add Transaction  2) Report  3) Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            t_type = input("Type (income/expense): ")
            desc = input("Description: ")
            manager.add_transaction(amount, category, t_type, desc)
        
        elif choice == "2":
            month = input("Enter month (YYYY-MM) or leave blank: ")
            manager.generate_report(month if month else None)
        
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":   # ✅ Fixed entry point
    demo_finance_manager()
