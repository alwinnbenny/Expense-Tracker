"""
business_logic.py
Ported and adapted from expense_manager.py for use with Django ORM querysets.
"""
from datetime import timedelta
from decimal import Decimal
from collections import defaultdict


# ── Constants ──────────────────────────────────────────────────────────────

RAPID_WINDOW_MINUTES = 1     # time window for rapid-transaction check
RAPID_THRESHOLD = 3           # min expenses in window to flag
LARGE_EXPENSE_MULTIPLIER = 5  # multiple of average to flag as large


# ── Daily Limit ────────────────────────────────────────────────────────────

def check_daily_limit(date, daily_limit, expenses_qs):
    """
    Return a dict describing whether daily spending exceeded the limit.

    Args:
        date (datetime.date): The date to check
        daily_limit (Decimal): The configured daily limit
        expenses_qs: Django queryset of all expenses

    Returns:
        dict: {exceeded, daily_total, daily_limit, percentage, overage}
    """
    day_expenses = expenses_qs.filter(date=date)
    daily_total = sum(e.amount for e in day_expenses) or Decimal('0')
    limit = Decimal(str(daily_limit))
    percentage = float(daily_total / limit * 100) if limit > 0 else 0.0
    exceeded = daily_total > limit
    overage = float(max(Decimal('0'), daily_total - limit))

    return {
        "exceeded": exceeded,
        "daily_total": float(daily_total),
        "daily_limit": float(limit),
        "percentage": round(percentage, 1),
        "overage": round(overage, 2),
    }


# ── Suspicious Activity Detection ──────────────────────────────────────────

def detect_suspicious_activity(expenses_qs):
    """
    Scan all expenses in the queryset and flag suspicious ones.

    Rules:
    1. Rapid transactions: RAPID_THRESHOLD+ expenses within RAPID_WINDOW_MINUTES.
    2. Unusually large: expense > LARGE_EXPENSE_MULTIPLIER × average.

    Mutates and saves matching Expense records in place.

    Returns:
        List of flagged Expense objects.
    """
    # Reset all database entries in this queryset before re-evaluating
    expenses_qs.update(suspicious=False, suspicious_reason=None)

    expenses = list(expenses_qs)
    if not expenses:
        return []

    # Compute average
    total = sum(e.amount for e in expenses)
    average = total / len(expenses) if expenses else Decimal('0')

    # Rule 1: Rapid transactions (sort by timestamp)
    timed = [(e, e.timestamp) for e in expenses if e.timestamp]
    timed.sort(key=lambda x: x[1])
    window = timedelta(minutes=RAPID_WINDOW_MINUTES)

    for i, (exp_i, ts_i) in enumerate(timed):
        cluster = [(exp_i, ts_i)]
        for j in range(i + 1, len(timed)):
            exp_j, ts_j = timed[j]
            if ts_j - ts_i <= window:
                cluster.append((exp_j, ts_j))
            else:
                break
        if len(cluster) >= RAPID_THRESHOLD:
            for exp, _ in cluster:
                if not exp.suspicious:
                    exp.suspicious = True
                    exp.suspicious_reason = (
                        f"rapid_transactions: {len(cluster)} expenses "
                        f"within {RAPID_WINDOW_MINUTES} min"
                    )
                    exp.save(update_fields=['suspicious', 'suspicious_reason'])

    # Rule 2: Unusually large amount
    if average > 0:
        threshold = average * LARGE_EXPENSE_MULTIPLIER
        for expense in expenses:
            if expense.amount >= threshold and not expense.suspicious:
                expense.suspicious = True
                expense.suspicious_reason = (
                    f"unusually_large: ₹{expense.amount:.2f} exceeds "
                    f"{LARGE_EXPENSE_MULTIPLIER}x average (₹{average:.2f})"
                )
                expense.save(update_fields=['suspicious', 'suspicious_reason'])

    return [e for e in expenses if e.suspicious]


# ── Analytics Dashboard ────────────────────────────────────────────────────

def get_analytics(expenses_qs, daily_limit=None):
    """
    Build a comprehensive analytics report from a queryset.

    Returns:
        dict with overall totals, category breakdown, monthly trend,
        daily totals, suspicious counts, and highest/lowest indicators.
    """
    expenses = list(expenses_qs)

    if not expenses:
        return {
            "overall_total": 0,
            "total_count": 0,
            "average_expense": 0,
            "highest_expense": None,
            "highest_category": None,
            "lowest_category": None,
            "daily_average": 0,
            "category_summary": {},
            "monthly_summary": {},
            "spending_trend": [],
            "daily_totals": [],
            "suspicious_count": 0,
            "suspicious_expenses": [],
        }

    overall_total = float(sum(e.amount for e in expenses))
    total_count = len(expenses)
    average_expense = round(overall_total / total_count, 2)

    # Highest single expense
    highest = max(expenses, key=lambda e: e.amount)
    highest_expense = {
        "id": highest.id,
        "amount": float(highest.amount),
        "category": highest.category,
        "date": str(highest.date),
        "description": highest.description,
    }

    # Category summary
    cat_totals: dict = defaultdict(float)
    for e in expenses:
        cat_totals[e.category] += float(e.amount)
    category_summary = dict(sorted(cat_totals.items()))
    highest_category = max(category_summary, key=category_summary.get)
    lowest_category = min(category_summary, key=category_summary.get)

    # Monthly summary
    month_totals: dict = defaultdict(float)
    for e in expenses:
        month_key = str(e.date)[:7]  # YYYY-MM
        month_totals[month_key] += float(e.amount)
    monthly_summary = dict(sorted(month_totals.items()))
    spending_trend = [
        {"month": m, "total": round(t, 2)}
        for m, t in monthly_summary.items()
    ]

    # Daily totals
    daily_map: dict = defaultdict(float)
    for e in expenses:
        daily_map[str(e.date)] += float(e.amount)

    limit_val = float(daily_limit) if daily_limit else None
    daily_totals = []
    for date_str, total in sorted(daily_map.items()):
        entry = {"date": date_str, "total": round(total, 2)}
        if limit_val:
            entry["pct"] = round(total / limit_val * 100, 1)
            entry["exceeded"] = total > limit_val
        daily_totals.append(entry)

    daily_average = round(
        sum(d["total"] for d in daily_totals) / len(daily_totals), 2
    ) if daily_totals else 0

    # Suspicious
    suspicious_expenses = [
        {
            "id": e.id,
            "amount": float(e.amount),
            "category": e.category,
            "date": str(e.date),
            "description": e.description,
            "suspicious_reason": e.suspicious_reason,
        }
        for e in expenses if e.suspicious
    ]

    return {
        "overall_total": round(overall_total, 2),
        "total_count": total_count,
        "average_expense": average_expense,
        "highest_expense": highest_expense,
        "highest_category": highest_category,
        "lowest_category": lowest_category,
        "daily_average": daily_average,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "spending_trend": spending_trend,
        "daily_totals": daily_totals,
        "suspicious_count": len(suspicious_expenses),
        "suspicious_expenses": suspicious_expenses,
    }
