from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser

class PortfolioValue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('User'))
    date = models.DateField(default=timezone.now, verbose_name=_('Date'))
    total_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Total Value'))
    cash_balance = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Cash Balance'))
    investments_value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_('Investments Value'))

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.date}"
