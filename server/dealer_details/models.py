from django.db import models


class Dealership(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, db_index=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    zip = models.CharField(max_length=10, blank=True, default="")
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    short_name = models.CharField(max_length=160, blank=True, default="")
    full_name = models.CharField(max_length=160, blank=True, default="")

    class Meta:
        ordering = ["state", "city", "name"]

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.name
        if not self.short_name:
            self.short_name = self.name
            for suffix in (
                " Motors",
                " Auto Center",
                " Automotive",
                " Auto Group",
                " Auto Gallery",
                " Auto House",
                " Auto Mall",
                " Auto Plaza",
                " Auto Works",
                " Auto Exchange",
                " Auto",
                " Cars",
            ):
                if self.name.endswith(suffix):
                    self.short_name = self.name[: -len(suffix)]
                    break
        if kwargs.get("update_fields") is not None:
            kwargs["update_fields"] = set(kwargs["update_fields"]) | {
                "short_name",
                "full_name",
            }
        super().save(*args, **kwargs)

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
