from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from api.models.userModel import User

class UserBitgoWalletAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True,related_name="user_bitgo_wallet_address")
    wallet_address = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(table_name='user_bitgo_wallet_address_history')
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.wallet_address

    class Meta:
        db_table = 'user_bitgo_wallet_address'
        indexes = [
            models.Index(fields=['id', 'wallet_address'])
        ]
