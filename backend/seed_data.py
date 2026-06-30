"""
Seed script: import existing expenses from expenses.json into MySQL.
Run from: c:\Projects\Expense Tracker\backend\
Command:  python seed_data.py
"""
import os, sys, json, django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from expenses.models import Expense, AppSettings
from datetime import datetime, timezone

JSON_FILE = Path(__file__).parent.parent / 'expenses.json'

with open(JSON_FILE) as f:
    data = json.load(f)

# Daily limit
daily_limit = data.get('daily_limit')
if daily_limit:
    settings = AppSettings.get_settings()
    settings.daily_limit = daily_limit
    settings.save()
    print(f"[OK] Daily limit set to {daily_limit}")

# Expenses
created = 0
for exp in data.get('expenses', []):
    ts_str = exp.get('timestamp')
    if ts_str:
        try:
            ts = datetime.fromisoformat(ts_str).replace(tzinfo=timezone.utc)
        except ValueError:
            ts = None
    else:
        ts = None

    e = Expense(
        amount=exp['amount'],
        category=exp['category'],
        date=exp['date'],
        description=exp.get('description', ''),
        suspicious=exp.get('suspicious', False),
        suspicious_reason=exp.get('suspicious_reason'),
    )
    e.save()

    # Override auto_now_add timestamp if we have one
    if ts:
        Expense.objects.filter(pk=e.pk).update(timestamp=ts)

    created += 1
    print(f"  Imported expense #{e.pk}: {e.category} ₹{e.amount}")

print(f"\n[OK] Imported {created} expense(s) into MySQL.")
