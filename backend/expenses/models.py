from django.db import models


class Expense(models.Model):
    """Represents a single expense record."""

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    suspicious = models.BooleanField(default=False)
    suspicious_reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-timestamp']
        db_table = 'expenses'

    def __str__(self):
        return f"[{self.id}] {self.category} ₹{self.amount} on {self.date}"


class AppSettings(models.Model):
    """Singleton settings row (always id=1)."""

    daily_limit = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = 'app_settings'

    def __str__(self):
        return f"Settings (daily_limit={self.daily_limit})"

    @classmethod
    def get_settings(cls):
        """Return the singleton settings object, creating it if absent."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
