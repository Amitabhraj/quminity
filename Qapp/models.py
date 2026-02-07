from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone


courses_name_choices = [
    ('B.tech CSE', 'B.tech CSE'),
    ('B.tech Civil', 'B.tech Civil'),
    ('B.tech AI/ML', 'B.tech AI/ML'),
    ('B.tech Mechanical', 'B.tech Mechanical'),
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
]

notification_type = [
    ('Marking Attendance', 'Marking Attendance')
]

USER_TYPE = [
    ('Admin', 'Admin'),
    ('Faculty', 'Faculty'),
    ('Student', 'Student'),
    ("N_FACULTY","N_FACULTY"),
    ("DEAN","DEAN"),
]


class Course(models.Model):
    course_name = models.CharField(max_length=100, choices=courses_name_choices,default="",null=True, blank=True)

    def __str__(self):  
        return self.course_name
    


class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(default="",null=True,blank=True,max_length=100)
    subject_code = models.CharField(default="",null=True,blank=True,max_length=100)
    faculty_name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} - {self.subject_code}"
    


class Section(models.Model):
    section_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ManyToManyField(Subject)
    
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
    face_encoding = models.BinaryField(null=True, blank=True, editable=True)
    anonymous = models.BooleanField(default=True,null=True, blank=True)
    user_type = models.CharField(max_length=100,choices=USER_TYPE,default=None,blank=True,null=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    program = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=5, null=True, blank=True)
    year = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.username
    
    def get_full_name(self):   
        return f"{self.first_name} {self.last_name}"



######################### Start Club/Events Models #########################

class Club(models.Model):
    club_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    members_detail = models.JSONField(default=dict,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    entry_fees = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    club_video = models.FileField(upload_to='event_videos/', null=True, blank=True)
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    core_members = models.ManyToManyField(CustomUser, related_name='core_members_club', blank=True)
    student_enrolled = models.ManyToManyField(CustomUser, related_name='student_enrolled_club', blank=True)
    blocked_student = models.ManyToManyField(CustomUser, related_name='blocked_students_club', blank=True)

    def __str__(self):
        return f"{self.club_name}"
    
class Event(models.Model):
    event = models.CharField(max_length=100, unique=True, null=True, blank=True)
    club = models.ForeignKey(Club,on_delete=models.CASCADE, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    entry_fees = models.IntegerField(default=0,null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    faculty_assigned = models.ManyToManyField(CustomUser, related_name='faculty_assigned_event', blank=True)
    event_coordinator = models.ManyToManyField(CustomUser, related_name='event_coordinator_event', blank=True)
    is_free = models.BooleanField(default=False)
    event_video = models.FileField(upload_to='event_videos/', null=True, blank=True)
    banner = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    student_enrolled = models.ManyToManyField(CustomUser, related_name='student_enrolled_event', blank=True)
    blocked_student = models.ManyToManyField(CustomUser, related_name='blocked_students_event', blank=True)

    def __str__(self):
        return f"{self.event} by {self.club} on {self.event_date.strftime('%Y-%m-%d')}"


class ClubPayment(models.Model):
    club = models.ForeignKey(Club,on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.payment_id}"
    

class EventPayment(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.payment_id}"

######################### End Club/Events Models #########################



class ActiveToken(models.Model):
    current_token = models.CharField(max_length=200,null=True, blank=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now,null=True, blank=True)



class Attendance(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    is_present = models.BooleanField(default=False)
    attendance_marked_at = models.DateTimeField(default=timezone.now)
    attendance_marked_by_cordinator = models.BooleanField(default=False)

    def __str__(self):
        if self.is_present:
            return f"{self.student_id} - Present in {self.event.event} on {self.event.event_date.strftime('%Y-%m-%d')}"
        else:
            return f"{self.student_id} - Absent in {self.event.event} on {self.event.event_date.strftime('%Y-%m-%d')}"



class Certificate(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    certificate_pushed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificate Pushed to {self.student.username} for event - {self.event.event} at {self.certificate_pushed_at}"




class Notification(models.Model):
    push_to = models.ForeignKey(CustomUser,related_name="push_to_notification" ,on_delete=models.CASCADE, null=True, blank=True)
    push_by = models.ForeignKey(CustomUser,related_name="push_by_notification", on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='notification_file/', null=True, blank=True)
    notificatio_type = models.CharField(max_length=100,choices=notification_type,default=None,blank=True,null=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100,default="",null=True,blank=True)
    message = models.TextField(default="",null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Push to {self.push_to.username} by-{self.push_by.username} , subject-{self.subject}"



class ClassRoom(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    present = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.present:
            return f"{self.student.username} Present in subject-{self.subject.subject_name} on date-{self.date.strftime('%Y-%m-%d')}"
        else:
            return f"{self.student.username} Absent in subject-{self.subject.subject_name} on date-{self.date.strftime('%Y-%m-%d')}"