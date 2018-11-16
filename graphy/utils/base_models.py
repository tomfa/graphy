import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier of the instance.',
    )
    created_at = models.DateTimeField(
        editable=False, help_text='Timestamp when instance was created.'
    )
    updated_at = models.DateTimeField(
        editable=False, help_text='Timestamp when instance was last updated.'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created_at'
        ordering = ('created_at',)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.created_at is None:
            self.created_at = now
        self.updated_at = now
        return super().save(*args, **kwargs)
