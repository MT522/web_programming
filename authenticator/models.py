from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Contestant(models.Model):
    
    class Gender(models.IntegerChoices):
        MALE = 1,"Male"
        FEMALE = 2,"Female"
        OTHER = 3,"Other"
    """
    class ParticipationType(models.IntegerChoices):
        IN_PERSON = 1, "In Person"
        ONLINE = 2, "Online"
    """ 
        
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        APPROVED = 2, "Approved"

    class Resume_Approve(models.IntegerChoices):
        SHARE = 1, "Share"
        NOT_SHARE = 2, "Do not Share"
    
    class League(models.IntegerChoices):
        UNDERGRAD = 1, "Undergrad"
        GRAD = 2, "Grad"
    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    gender = models.PositiveSmallIntegerField(default=Gender.MALE, choices=Gender.choices)
    
    
    phone = models.CharField(max_length = 14)
    telegram_id = models.CharField(max_length=127)
    national_id = models.CharField(max_length=127)
    affiliation = models.CharField(max_length=127)
    major = models.CharField(max_length=127)

    prof_name = models.CharField(max_length=63)
    prof_email = models.EmailField(max_length=127)

    resume = models.FileField(upload_to='resumes', null=True)
    resume_share_consent = models.PositiveSmallIntegerField(default=Resume_Approve.SHARE, choices=Resume_Approve.choices)
    content = models.FileField(upload_to='content', null=True)

    league = models.PositiveSmallIntegerField(default=League.UNDERGRAD, choices=League.choices)
    judge1 = models.ForeignKey("Judge", null=True, on_delete=models.SET_NULL, related_name="judge1")
    judge2 = models.ForeignKey("Judge", null=True, on_delete=models.SET_NULL, related_name="judge2")
    judge3 = models.ForeignKey("Judge", null=True, on_delete=models.SET_NULL, related_name="judge3")

    exceeded_time = models.BooleanField(null=True, default=False)
    
    def __str__(self):
        return str(self.user)

class Judge(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Score(models.Model):
    user = models.ForeignKey("Contestant", null=True, on_delete=models.CASCADE)
    judge = models.ForeignKey("Judge", null=True, on_delete=models.CASCADE)

    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    comment = models.CharField(null=True, blank=True, max_length=511)

    def __str__(self):
        return str(self.user + " | " + self.judge + " | " + f"{self.score}")
