from django.db import models

class Hospital(models.Model):

    hospital_id = models.CharField(max_length=50)
    hospital_name = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    email = models.TextField()

    def __str__(self):
        return f"{self.hospital_name} ({self.district})"


class Registration(models.Model):

    email = models.EmailField(unique=True)

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20, blank=True)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email