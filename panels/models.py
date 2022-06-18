from django.core.exceptions import PermissionDenied
from django.db import models
from accounts.models import Trader, BankEmployee
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
    status = models.CharField(max_length=10, default='Waiting', choices=STATUS_OPTS)
    is_processed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.id}: {self.status}'


class EmployeeDiscountAction(BaseModel):
    employee = models.ForeignKey(BankEmployee, on_delete=models.CASCADE, related_name='discount_actions')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='discount_actions')
    state = models.BooleanField()

    def __str__(self):
        return f'{self.discount}: {self.state}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'discount'], name='unique_employee_discount')
        ]
