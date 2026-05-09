from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Visitor(models.Model):
    STATUS_CHOICES = [
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    purpose_of_visit = models.CharField(max_length=200)
    host_name = models.CharField(max_length=100, help_text="Whom the visitor is here to see")
    
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Checked In')
    
    # Links the visitor record to the security personnel who logged them in
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
