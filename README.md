# Expense Tracker - Python CLI Application

A simple, menu-driven command-line expense tracking application that helps you manage and analyze your spending.

## Features

✅ **Add Expenses** - Record new expenses with amount, category, date, and description  
✅ **Edit Expenses** - Modify existing expense details  
✅ **Delete Expenses** - Remove unwanted expenses  
✅ **View All Expenses** - Display all expenses in a formatted table  
✅ **Category Summary** - See total spending by category  
✅ **Monthly Summary** - View spending trends by month  
✅ **Export to CSV** - Save expenses to a CSV file for analysis  
✅ **Persistent Storage** - All data is saved to `expenses.json`  

## Project Structure

```
Expense Tracker/
├── main.py              # CLI menu and user interactions
├── expense_manager.py   # Business logic for expense operations
├── storage.py           # File handling (JSON & CSV operations)
├── expenses.json        # Data storage file (auto-created)
└── README.md           # This file
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation & Running

### Step 1: Navigate to the Project Directory
```bash
cd "c:\Projects\Expense Tracker"
```

### Step 2: Run the Application
```bash
python main.py
```

Or on some systems:
```bash
python3 main.py
```

### Step 3: Follow the Menu
The application will display an interactive menu with 8 options. Simply enter the number corresponding to your desired action.

## Usage Examples

### Adding an Expense
1. Select option `1` from the menu
2. Enter the amount (e.g., `45.50`)
3. Enter the category (e.g., `Food`)
4. Enter the date (YYYY-MM-DD format or press Enter for today)
5. Enter a description (optional)

### Viewing Expenses
- **Option 4**: View all expenses in a formatted table with totals
- **Option 5**: See a summary of total spending by category
- **Option 6**: Check monthly spending trends

### Exporting Data
- **Option 7**: Export all expenses to a CSV file for use in Excel or other tools

## Data Structure

Expenses are stored in `expenses.json` with the following format:

```json
{
    "expenses": [
        {
            "id": 1,
            "amount": 45.50,
            "category": "Food",
            "date": "2026-01-28",
            "description": "Lunch at downtown cafe"
        }
    ]
}
```

Each expense has:
- **id**: Unique identifier (auto-generated)
- **amount**: Expense amount (rounded to 2 decimal places)
- **category**: Spending category
- **date**: Date in YYYY-MM-DD format
- **description**: Optional description

## Date Format

All dates must be in `YYYY-MM-DD` format. When adding an expense, you can:
- Enter a specific date: `2026-01-31`
- Press Enter to use today's date automatically

## Error Handling

The application includes comprehensive error handling for:
- Invalid numeric inputs
- Invalid date formats
- Missing required fields
- File I/O errors
- Missing expense IDs

## Clean Code Practices

This project follows best practices:
- **Modular Design**: Separate concerns across multiple files
- **Docstrings**: All functions include detailed documentation
- **Type Hints**: Clear parameter and return type annotations
- **Comments**: Inline comments explain complex logic
- **Validation**: Input validation for all user entries
- **Error Messages**: Helpful error messages guide users

## Features Breakdown

### Module: main.py
- CLI menu interface
- User input handling
- Formatted output display
- Menu-driven flow control

### Module: expense_manager.py
- Add, edit, delete operations
- Data validation (amounts, dates, categories)
- Summary generation (by category, by month)
- ID management

### Module: storage.py
- JSON file operations (read/write)
- CSV export functionality
- File initialization and error handling

## Tips

- Use meaningful category names for better summaries (e.g., "Food", "Transport", "Entertainment", "Utilities")
- Check the monthly summary to identify spending patterns
- Export to CSV before important financial reviews
- The application automatically saves changes to `expenses.json`

## Sample Data

A sample `expenses.json` file is included with 7 example expenses to demonstrate the functionality. Feel free to delete these and start with your own!

## Troubleshooting

**Issue**: Module not found error
- **Solution**: Ensure all three Python files are in the same directory

**Issue**: Can't run python command
- **Solution**: Check that Python is installed: `python --version`

**Issue**: "Permission denied" on expenses.json
- **Solution**: Check file permissions or move the application to a different directory

## Future Enhancements

Potential features for future versions:
- Budget tracking and alerts
- Recurring expenses
- Data visualization with charts
- Search and filter functionality
- Multi-user support
- Import from CSV
- Database backend (SQLite/PostgreSQL)

---

**Happy Expense Tracking!** 💰
