from django.db import models


class Dealership(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, db_index=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["state", "city", "name"]

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, related_name="models", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["make", "name"], name="unique_car_model_per_make")
        ]

    def __str__(self):
        return f"{self.make.name} {self.name}"
