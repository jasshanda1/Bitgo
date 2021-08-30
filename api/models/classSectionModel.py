from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from .classModel import Classes

class ClassSection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    section_class = models.ForeignKey(Classes, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(table_name='class_section_history')
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'class_section'
        indexes = [
            models.Index(fields=['id', 'name'])
        ]
