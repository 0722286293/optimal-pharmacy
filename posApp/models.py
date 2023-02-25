from django.db import models
from pharmacy.models import Stock


class StockNotifications(models.Model):
    title = models.CharField(max_length=155)
    drug = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="stock_notify")
    resolved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Low Stock Notifications"
        verbose_name_plural = verbose_name