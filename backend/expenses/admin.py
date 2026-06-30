from django.contrib import admin
from .models import Expense, AppSettings


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'category', 'date', 'suspicious', 'timestamp']
    list_filter = ['category', 'suspicious', 'date']
    search_fields = ['description', 'category']
    readonly_fields = ['timestamp', 'suspicious', 'suspicious_reason']


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_limit']
