from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Expense, AppSettings
from .serializers import ExpenseSerializer, AppSettingsSerializer
from . import business_logic as bl


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    CRUD + custom actions for expenses.

    Routes (via DefaultRouter):
      GET    /api/expenses/                 → list
      POST   /api/expenses/                 → create
      GET    /api/expenses/<id>/            → retrieve
      PUT    /api/expenses/<id>/            → update
      PATCH  /api/expenses/<id>/            → partial_update
      DELETE /api/expenses/<id>/            → destroy
      GET    /api/expenses/analytics/       → analytics dashboard
      POST   /api/expenses/detect_suspicious/ → run suspicious scan
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    # ── After create: run daily-limit check + suspicious detection ──────

    def perform_create(self, serializer):
        expense = serializer.save()

        # Run suspicious detection on all expenses
        bl.detect_suspicious_activity(Expense.objects.all())
        
        # Refresh from database so the serialized data contains updated suspicious flags
        expense.refresh_from_db()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Append daily-limit warning to the response body
        settings = AppSettings.get_settings()
        if settings.daily_limit:
            expense_date = response.data.get('date')
            warning = bl.check_daily_limit(
                expense_date, settings.daily_limit, Expense.objects.all()
            )
            response.data['daily_limit_check'] = warning

        return response

    # ── After update: run daily-limit check + suspicious detection ──────

    def perform_update(self, serializer):
        expense = serializer.save()

        # Re-run suspicious detection on all expenses
        bl.detect_suspicious_activity(Expense.objects.all())
        
        # Refresh from database
        expense.refresh_from_db()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        # Append daily-limit warning to the response body
        settings = AppSettings.get_settings()
        if settings.daily_limit:
            expense_date = response.data.get('date')
            warning = bl.check_daily_limit(
                expense_date, settings.daily_limit, Expense.objects.all()
            )
            response.data['daily_limit_check'] = warning

        return response

    # ── GET /api/expenses/analytics/ ────────────────────────────────────

    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        """Return full analytics dashboard data."""
        bl.detect_suspicious_activity(Expense.objects.all())
        settings = AppSettings.get_settings()
        data = bl.get_analytics(Expense.objects.all(), settings.daily_limit)
        data['daily_limit'] = float(settings.daily_limit) if settings.daily_limit else None
        return Response(data)

    # ── POST /api/expenses/detect_suspicious/ ───────────────────────────

    @action(detail=False, methods=['post'], url_path='detect_suspicious')
    def detect_suspicious(self, request):
        """Run suspicious activity detection and return flagged expenses."""
        flagged = bl.detect_suspicious_activity(Expense.objects.all())
        serializer = ExpenseSerializer(flagged, many=True)
        return Response({
            "flagged_count": len(flagged),
            "flagged_expenses": serializer.data,
        })


class AppSettingsView(viewsets.ViewSet):
    """
    Singleton settings endpoint.

    Routes:
      GET  /api/settings/  → retrieve daily limit
      PUT  /api/settings/  → update daily limit
    """

    def list(self, request):
        settings = AppSettings.get_settings()
        serializer = AppSettingsSerializer(settings)
        return Response(serializer.data)

    def create(self, request):
        """PUT semantics — update the singleton."""
        settings = AppSettings.get_settings()
        serializer = AppSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
