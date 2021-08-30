from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from .userModel import User
from .classSectionModel import ClassSection
from .UserClassesDetailsModel import UserClassDetails

class UserSectionDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user_class = models.ForeignKey(UserClassDetails, related_name="user_sections", on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    history = HistoricalRecords(table_name='user_section_details_history')
    can_delete = models.BooleanField(default=True)

    def __str__(self):
        return (self.id)

    class Meta:
        db_table = 'user_section_details'
        indexes = [
            models.Index(fields=['id'])
        ]
