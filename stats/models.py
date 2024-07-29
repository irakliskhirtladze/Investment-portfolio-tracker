from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()

class PortfolioValue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_('Timestamp'))
    total_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Total Value'))
    cash_balance = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Cash Balance'))
    investments_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Investments Value'))

    class Meta:
        unique_together = ('user', 'timestamp')
        verbose_name = _('Portfolio Value')
        verbose_name_plural = _('Portfolio Values')
        indexes = [
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.timestamp}"
