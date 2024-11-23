from django.db import models
from django.utils.text import slugify
import uuid

class Session(models.Model):
    name=models.CharField(max_length=50, null = True, blank = True, default= "test sniffer")
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug=models.SlugField(null=True, blank=True)
    packets= models.JSONField(null= True, blank=True)
    running = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} - {self.session_id}"
