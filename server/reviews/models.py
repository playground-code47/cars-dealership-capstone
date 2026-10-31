from django.conf import settings
from django.db import models

from dealer_details.models import Dealership


class Review(models.Model):
    dealership = models.ForeignKey(
        Dealership, related_name="reviews", on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="dealer_reviews", on_delete=models.CASCADE
    )
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.reviewer} for {self.dealership}"
