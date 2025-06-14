from django.db import models
from users.models import User
from groups.models import EqubGroup


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(EqubGroup, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    round_number = models.PositiveIntegerField()
    class Meta:
        unique_together = ('user', 'group', 'round_number')  # Prevents double payments

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.status})"