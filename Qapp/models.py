from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

courses_name_choices = [
    ('B.tech CSE', 'B.tech CSE'),
    ('B.tech Civil', 'B.tech Civil'),
    ('B.tech AI/ML', 'B.tech AI/ML'),
    ('B.tech Mechanical', 'B.tech Mechanical'),
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
]


class Course(models.Model):
    course_name = models.CharField(max_length=100, choices=courses_name_choices,default="",null=True, blank=True)

    def __str__(self):  
        return self.course_name
    

class Subjects(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(default="",null=True,blank=True,max_length=100)
    subject_code = models.CharField(default="",null=True,blank=True,max_length=100)

    def __str__(self):
        return f"{self.subject_name} - {self.subject_code}"
    


class Section(models.Model):
    section_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['section_name', 'course'], 
                name='unique_section_per_course'
            )
        ]

    def __str__(self):
        return f"{self.section_name} - {self.course}"

class CustomUser(AbstractUser):
    qid = models.CharField(max_length=15, unique=True, null=True, blank=True)
    anonymous = models.BooleanField(default=True,null=True, blank=True)
    section = models.ForeignKey(Section,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
    
    def get_full_name(self):   
        return f"{self.first_name} {self.last_name}"
