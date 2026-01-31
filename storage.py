"""
storage.py - File handling module for Expense Tracker

This module handles:
- Reading and writing expenses from/to JSON file
- Exporting expenses to CSV format
- Creating initial data file if it doesn't exist

Sample JSON structure:
{
    "expenses": [
        {
            "id": 1,
            "amount": 50.00,
            "category": "Food",
            "date": "2026-01-31",
            "description": "Lunch at restaurant"
        }
    ]
}
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


class StorageManager:
    """Manages reading and writing expense data to JSON and CSV files."""
    
    def __init__(self, filename: str = "expenses.json"):
        """
        Initialize the storage manager.
        
        Args:
            filename (str): Name of the JSON file to store expenses
        """
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the JSON file with initial structure if it doesn't exist."""
        if not Path(self.filename).exists():
            initial_data = {"expenses": []}
            with open(self.filename, 'w') as f:
                json.dump(initial_data, f, indent=4)
    
    def load_expenses(self) -> List[Dict[str, Any]]:
        """
        Load all expenses from the JSON file.
        
        Returns:
            List[Dict]: List of expense dictionaries
        """
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            return data.get("expenses", [])
        except (json.JSONDecodeError, FileNotFoundError):
            print("Warning: Could not load expenses. Starting with empty list.")
            return []
    
    def save_expenses(self, expenses: List[Dict[str, Any]]) -> None:
        """
        Save expenses to the JSON file.
        
        Args:
            expenses (List[Dict]): List of expense dictionaries to save
        """
        try:
            data = {"expenses": expenses}
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving expenses: {e}")
    
    def export_to_csv(self, expenses: List[Dict[str, Any]], filename: str = "expenses.csv") -> bool:
        """
        Export expenses to a CSV file.
        
        Args:
            expenses (List[Dict]): List of expense dictionaries to export
            filename (str): Name of the CSV file to create
        
        Returns:
            bool: True if export was successful, False otherwise
        """
        if not expenses:
            print("No expenses to export.")
            return False
        
        try:
            # Define CSV column headers
            fieldnames = ["ID", "Amount", "Category", "Date", "Description"]
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write headers
                writer.writeheader()
                
                # Write expense data
                for expense in expenses:
                    writer.writerow({
                        "ID": expense["id"],
                        "Amount": f"${expense['amount']:.2f}",
                        "Category": expense["category"],
                        "Date": expense["date"],
                        "Description": expense["description"]
                    })
            
            print(f"Successfully exported {len(expenses)} expense(s) to '{filename}'")
            return True
        
        except IOError as e:
            print(f"Error exporting to CSV: {e}")
            return False
