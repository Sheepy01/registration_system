from django.db import models

class Hospital(models.Model):

    hospital_id = models.CharField(max_length=50)
    hospital_name = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    email = models.TextField()

    def __str__(self):
        return f"{self.hospital_name} ({self.district})"


class Registration(models.Model):

    email = models.EmailField()
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)