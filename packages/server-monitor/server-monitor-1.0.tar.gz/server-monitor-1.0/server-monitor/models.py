from django.db import models
import uuid

class CronJobs(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    job_name = models.CharField(max_length=20, unique=True)
    job_description = models.TextField(default="No Description Provided")