"""
expense_manager.py - Business logic module for Expense Tracker

This module handles all expense-related operations:
- Adding, editing, and deleting expenses
- Retrieving and filtering expenses
- Generating summaries (by category and by month)
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


class ExpenseManager:
    """Manages expense operations and business logic."""
    
    def __init__(self, expenses: List[Dict[str, Any]]):
        """
        Initialize the expense manager with a list of expenses.
        
        Args:
            expenses (List[Dict]): List of existing expenses
        """
        self.expenses = expenses
    
    def _get_next_id(self) -> int:
        """
        Get the next available ID for a new expense.
        
        Returns:
            int: The next ID to use
        """
        if not self.expenses:
            return 1
        return max(expense["id"] for expense in self.expenses) + 1
    
    def _validate_date(self, date_str: str) -> bool:
        """
        Validate if a date string is in the correct format (YYYY-MM-DD).
        
        Args:
            date_str (str): Date string to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _validate_amount(self, amount: float) -> bool:
        """
        Validate if an amount is positive.
        
        Args:
            amount (float): Amount to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        return amount > 0
    
    def add_expense(self, amount: float, category: str, date: str, 
                    description: str) -> bool:
        """
        Add a new expense.
        
        Args:
            amount (float): Expense amount
            category (str): Expense category
            date (str): Expense date in YYYY-MM-DD format
            description (str): Expense description
        
        Returns:
            bool: True if added successfully, False otherwise
        """
        # Validate inputs
        if not self._validate_amount(amount):
            print("Error: Amount must be greater than 0.")
            return False
        
        if not self._validate_date(date):
            print("Error: Date must be in YYYY-MM-DD format.")
            return False
        
        if not category.strip():
            print("Error: Category cannot be empty.")
            return False
        
        # Create new expense
        new_expense = {
            "id": self._get_next_id(),
            "amount": round(amount, 2),
            "category": category.strip(),
            "date": date,
            "description": description.strip() if description else "No description"
        }
        
        self.expenses.append(new_expense)
        print(f"Expense added successfully! (ID: {new_expense['id']})")
        return True
    
    def edit_expense(self, expense_id: int, amount: Optional[float] = None,
                     category: Optional[str] = None, date: Optional[str] = None,
                     description: Optional[str] = None) -> bool:
        """
        Edit an existing expense.
        
        Args:
            expense_id (int): ID of the expense to edit
            amount (float, optional): New amount
            category (str, optional): New category
            date (str, optional): New date
            description (str, optional): New description
        
        Returns:
            bool: True if edited successfully, False otherwise
        """
        # Find the expense
        expense = self._find_expense_by_id(expense_id)
        if not expense:
            print(f"Error: Expense with ID {expense_id} not found.")
            return False
        
        # Validate and update fields
        if amount is not None:
            if not self._validate_amount(amount):
                print("Error: Amount must be greater than 0.")
                return False
            expense["amount"] = round(amount, 2)
        
        if category is not None:
            if not category.strip():
                print("Error: Category cannot be empty.")
                return False
            expense["category"] = category.strip()
        
        if date is not None:
            if not self._validate_date(date):
                print("Error: Date must be in YYYY-MM-DD format.")
                return False
            expense["date"] = date
        
        if description is not None:
            expense["description"] = description.strip() if description else "No description"
        
        print(f"Expense ID {expense_id} updated successfully!")
        return True
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id (int): ID of the expense to delete
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        for i, expense in enumerate(self.expenses):
            if expense["id"] == expense_id:
                deleted_expense = self.expenses.pop(i)
                print(f"Expense ID {expense_id} deleted successfully!")
                return True
        
        print(f"Error: Expense with ID {expense_id} not found.")
        return False
    
    def _find_expense_by_id(self, expense_id: int) -> Optional[Dict[str, Any]]:
        """
        Find an expense by its ID.
        
        Args:
            expense_id (int): ID of the expense to find
        
        Returns:
            Dict or None: The expense dictionary or None if not found
        """
        for expense in self.expenses:
            if expense["id"] == expense_id:
                return expense
        return None
    
    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """
        Get all expenses.
        
        Returns:
            List[Dict]: List of all expenses
        """
        return self.expenses
    
    def get_category_summary(self) -> Dict[str, float]:
        """
        Get a summary of expenses by category.
        
        Returns:
            Dict: Dictionary with categories as keys and total amounts as values
        """
        summary = {}
        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]
            summary[category] = summary.get(category, 0) + amount
        
        return dict(sorted(summary.items()))
    
    def get_monthly_summary(self) -> Dict[str, float]:
        """
        Get a summary of expenses by month (YYYY-MM format).
        
        Returns:
            Dict: Dictionary with months as keys and total amounts as values
        """
        summary = {}
        for expense in self.expenses:
            # Extract YYYY-MM from date
            month = expense["date"][:7]
            amount = expense["amount"]
            summary[month] = summary.get(month, 0) + amount
        
        return dict(sorted(summary.items()))
