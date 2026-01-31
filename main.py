"""
main.py - CLI Interface for Expense Tracker Application

HOW TO RUN:
1. Ensure you have Python 3.6+ installed
2. Navigate to the project directory in your terminal
3. Run: python main.py
4. Follow the menu prompts to manage your expenses

The application will create an 'expenses.json' file automatically to store data.
Exported CSV files will be saved as 'expenses.csv' in the same directory.

FEATURES:
- Add, edit, and delete expenses
- View all expenses with formatted output
- Get expense summaries by category and month
- Export expenses to CSV format
- All data persists between sessions
"""

from storage import StorageManager
from expense_manager import ExpenseManager
from datetime import datetime


def print_header(title: str) -> None:
    """
    Print a formatted header for better UI.
    
    Args:
        title (str): Title to display
    """
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_menu() -> None:
    """Display the main menu options."""
    print("\n" + "-" * 60)
    print("EXPENSE TRACKER - MAIN MENU")
    print("-" * 60)
    print("1. Add an expense")
    print("2. Edit an expense")
    print("3. Delete an expense")
    print("4. View all expenses")
    print("5. View category-wise summary")
    print("6. View monthly summary")
    print("7. Export expenses to CSV")
    print("8. Exit")
    print("-" * 60)


def display_expenses(expenses: list) -> None:
    """
    Display expnses in a formatted table.
    
    Args:
        expenses (list): List of expenses to display
    """
    if not expenses:
        print("No expenses found.")
        return
    
    # Print table header
    print(f"\n{'ID':<5} {'Amount':<12} {'Category':<15} {'Date':<12} {'Description':<30}")
    print("-" * 80)
    
    # Print each expense
    for expense in expenses:
        amount_str = f"${expense['amount']:.2f}"
        description = expense['description'][:27] + "..." if len(expense['description']) > 27 else expense['description']
        print(f"{expense['id']:<5} {amount_str:<12} {expense['category']:<15} {expense['date']:<12} {description:<30}")


def add_expense_menu(manager: ExpenseManager) -> None:
    """
    Handle adding a new expense through user input.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("ADD NEW EXPENSE")
    
    try:
        # Get amount
        while True:
            try:
                amount = float(input("Enter amount: $"))
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        
        # Get category
        category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
        if not category:
            print("Error: Category cannot be empty.")
            return
        
        # Get date
        while True:
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
                break
            if len(date) == 10 and date[4] == '-' and date[7] == '-':
                break
            print("Error: Please use YYYY-MM-DD format.")
        
        # Get description
        description = input("Enter description (optional): ").strip()
        
        # Add expense
        manager.add_expense(amount, category, date, description)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


def edit_expense_menu(manager: ExpenseManager) -> None:
    """
    Handle editing an existing expense through user input.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("EDIT EXPENSE")
    
    expenses = manager.get_all_expenses()
    if not expenses:
        print("No expenses to edit.")
        return
    
    display_expenses(expenses)
    
    try:
        expense_id = int(input("\nEnter the ID of the expense to edit: "))
        
        # Find the expense to show current values
        expense = None
        for exp in expenses:
            if exp["id"] == expense_id:
                expense = exp
                break
        
        if not expense:
            print(f"Error: Expense with ID {expense_id} not found.")
            return
        
        print(f"\nCurrent details:")
        print(f"  Amount: ${expense['amount']:.2f}")
        print(f"  Category: {expense['category']}")
        print(f"  Date: {expense['date']}")
        print(f"  Description: {expense['description']}")
        
        # Get new values (optional)
        new_amount = None
        new_category = None
        new_date = None
        new_description = None
        
        amount_input = input("\nEnter new amount (or press Enter to skip): ").strip()
        if amount_input:
            try:
                new_amount = float(amount_input)
            except ValueError:
                print("Error: Invalid amount.")
                return
        
        new_category = input("Enter new category (or press Enter to skip): ").strip()
        if not new_category:
            new_category = None
        
        new_date = input("Enter new date (or press Enter to skip): ").strip()
        if not new_date:
            new_date = None
        
        new_description = input("Enter new description (or press Enter to skip): ").strip()
        if not new_description:
            new_description = None
        
        # Update expense
        manager.edit_expense(expense_id, new_amount, new_category, new_date, new_description)
    
    except ValueError:
        print("Error: Please enter a valid ID.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


def delete_expense_menu(manager: ExpenseManager) -> None:
    """
    Handle deleting an expense through user input.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("DELETE EXPENSE")
    
    expenses = manager.get_all_expenses()
    if not expenses:
        print("No expenses to delete.")
        return
    
    display_expenses(expenses)
    
    try:
        expense_id = int(input("\nEnter the ID of the expense to delete: "))
        
        # Confirm deletion
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm == 'yes' or confirm == 'y':
            manager.delete_expense(expense_id)
        else:
            print("Deletion cancelled.")
    
    except ValueError:
        print("Error: Please enter a valid ID.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")


def view_all_expenses_menu(manager: ExpenseManager) -> None:
    """
    Display all expenses in a formatted table.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("ALL EXPENSES")
    
    expenses = manager.get_all_expenses()
    if expenses:
        display_expenses(expenses)
        total = sum(exp["amount"] for exp in expenses)
        print("-" * 80)
        print(f"{'TOTAL':<5} {'$' + f'{total:.2f}':<12}")
    else:
        print("No expenses found. Add one to get started!")


def view_category_summary_menu(manager: ExpenseManager) -> None:
    """
    Display expenses summarized by category.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("CATEGORY-WISE SUMMARY")
    
    summary = manager.get_category_summary()
    
    if not summary:
        print("No expenses found.")
        return
    
    # Print table
    print(f"\n{'Category':<20} {'Total Amount':<20}")
    print("-" * 40)
    
    total = 0
    for category, amount in summary.items():
        print(f"{category:<20} ${amount:>18.2f}")
        total += amount
    
    print("-" * 40)
    print(f"{'GRAND TOTAL':<20} ${total:>18.2f}")


def view_monthly_summary_menu(manager: ExpenseManager) -> None:
    """
    Display expenses summarized by month.
    
    Args:
        manager (ExpenseManager): The expense manager instance
    """
    print_header("MONTHLY SUMMARY")
    
    summary = manager.get_monthly_summary()
    
    if not summary:
        print("No expenses found.")
        return
    
    # Print table
    print(f"\n{'Month (YYYY-MM)':<20} {'Total Amount':<20}")
    print("-" * 40)
    
    total = 0
    for month, amount in summary.items():
        print(f"{month:<20} ${amount:>18.2f}")
        total += amount
    
    print("-" * 40)
    print(f"{'GRAND TOTAL':<20} ${total:>18.2f}")


def export_to_csv_menu(manager: ExpenseManager, storage: StorageManager) -> None:
    """
    Export expenses to a CSV file.
    
    Args:
        manager (ExpenseManager): The expense manager instance
        storage (StorageManager): The storage manager instance
    """
    print_header("EXPORT TO CSV")
    
    expenses = manager.get_all_expenses()
    
    filename = input("Enter filename (default: expenses.csv): ").strip()
    if not filename:
        filename = "expenses.csv"
    elif not filename.endswith('.csv'):
        filename += '.csv'
    
    storage.export_to_csv(expenses, filename)


def main() -> None:
    """
    Main function to run the Expense Tracker application.
    Manages the menu loop and user interactions.
    """
    # Initialize storage and expense manager
    storage = StorageManager("expenses.json")
    expenses = storage.load_expenses()
    manager = ExpenseManager(expenses)
    
    print_header("WELCOME TO EXPENSE TRACKER")
    print("Track your expenses efficiently and get insightful summaries!")
    
    # Main menu loop
    while True:
        print_menu()
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            add_expense_menu(manager)
            storage.save_expenses(manager.get_all_expenses())
        
        elif choice == '2':
            edit_expense_menu(manager)
            storage.save_expenses(manager.get_all_expenses())
        
        elif choice == '3':
            delete_expense_menu(manager)
            storage.save_expenses(manager.get_all_expenses())
        
        elif choice == '4':
            view_all_expenses_menu(manager)
        
        elif choice == '5':
            view_category_summary_menu(manager)
        
        elif choice == '6':
            view_monthly_summary_menu(manager)
        
        elif choice == '7':
            export_to_csv_menu(manager, storage)
        
        elif choice == '8':
            print("\nThank you for using Expense Tracker. Goodbye!")
            break
        
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Exiting...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again or contact support if the problem persists.")
