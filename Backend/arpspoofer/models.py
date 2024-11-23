from django.db import models
import uuid
class Spoofer(models.Model):
    spoofer_id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=100)
    target_ip = models.CharField(max_length=20)
    target_mac = models.CharField(max_length=20, null=True, blank=True)
    gateway_ip = models.CharField(max_length=20)
    gateway_mac = models.CharField(max_length=20, null=True, blank=True)
    total_count = models.IntegerField(null = True , blank = True)
    time_ran = models.TimeField(null = True, blank = True)
    is_running = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.name

