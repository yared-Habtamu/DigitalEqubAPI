from django.db import models
from users.models import User
from django.core.validators import MinValueValidator


class EqubGroup(models.Model):
    CYCLE_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('BIWEEKLY', 'Bi-weekly'),
        ('MONTHLY', 'Monthly'),
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    cycle_duration = models.CharField(max_length=10, choices=CYCLE_CHOICES, default='MONTHLY')
    created_at = models.DateTimeField(auto_now_add=True)
    current_round = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    next_payout_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey(EqubGroup, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)
    has_received_payout = models.BooleanField(default=False)
    payout_order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'group')
        ordering = ['payout_order']

    def __str__(self):
        return f"{self.user.email} in {self.group.name}"


class Payout(models.Model):
    group = models.ForeignKey(EqubGroup, on_delete=models.CASCADE, related_name='payouts')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    round_number = models.PositiveIntegerField()
    payout_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Round {self.round_number} payout to {self.recipient.email}"