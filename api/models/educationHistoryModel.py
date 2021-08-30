from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from .userModel import User


class EducationHistory(models.Model):
    user = models.ForeignKey(User, related_name="education_history", on_delete=models.DO_NOTHING)
    degree_name = models.CharField(max_length=120, blank=True, null=True)
    college_name = models.CharField(max_length=300, blank=True, null=True)
    start = models.CharField(max_length=150, blank=True, null=True)
    end = models.CharField(max_length=150, blank=True, null=True)
    is_currenty = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(table_name='education_history_history')

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'education_history'
        indexes = [
            models.Index(fields=['id'])
        ]
