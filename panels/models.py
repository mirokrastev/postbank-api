from django.db import models
from accounts.models import Trader
from base.models import BaseModel


class Discount(BaseModel):
    STATUS_OPTS = (
        ('Active', 'Active'),
        ('Rejected', 'Rejected'),
        ('Expired', 'Expired'),
        ('Waiting', 'Waiting')
    )

    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    discount_percent = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_OPTS)
    is_processed = models.BooleanField(default=False, blank=True)
