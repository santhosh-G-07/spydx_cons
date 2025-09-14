from django.db import models
from django.contrib.auth.models import User


# Consultant profile linked to default Django User
class Consultant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant')
    phone = models.CharField(max_length=15, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)  # job role
    location = models.CharField(max_length=100, blank=True, null=True)  # new
    linkedin_id = models.URLField(blank=True, null=True)  # new
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username



from django.db import models
from django.contrib.auth.models import User

class ResumeUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Resume ({self.file.name})"



from django.db import models

class Project(models.Model):
    consultant = models.ForeignKey('Consultant', on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class UserATSResult(models.Model):
    consultant = models.ForeignKey(
        Consultant,
        on_delete=models.CASCADE,
        related_name='ats_results'
    )
    resume_text = models.TextField()
    ats_score = models.FloatField()
    mistakes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.consultant} - Score: {self.ats_score}"
