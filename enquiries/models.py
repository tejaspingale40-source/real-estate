from django.db import models
from properties.models import Property


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Follow Up', 'Follow Up'),
        ('Closed', 'Closed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        prop_str = f" for {self.property.title}" if self.property else ""
        return f"Enquiry from {self.name}{prop_str} ({self.status})"
