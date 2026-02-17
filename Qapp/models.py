from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone
from Qapp.common import ROLE_CHOICES, USER_TYPE


courses_name_choices = [
    ('B.TECH', 'B.TECH'),
    ('M.TECH', 'M.TECH'),
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
    ('BSC', 'BSC'),
    ('MSC', 'MSC'),
    ('BBA', 'BBA'),
    ('MBA', 'MBA'),
    ('BA', 'BA'),
    ('MA', 'MA'),
    ("BALLAB", "BALLAB"),
    ("LLB", "LLB"),
]

branch_choices = [
    ('B.TECH CSE', 'B.TECH CSE'),
    ('B.TECH CIVIL', 'B.TECH CIVIL'),
    ('B.TECH MECHANICAL', 'B.TECH MECHANICAL'),
    ('B.TECH ELECTRICAL', 'B.TECH ELECTRICAL'),
    ('M.TECH CSE', 'M.TECH CSE'),
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
    ('BSC', 'BSC'),
    ('MSC', 'MSC'),
    ('BBA', 'BBA'),
    ('MBA', 'MBA'),
    ('BA', 'BA'),
    ('MA', 'MA'),
    ("BALLAB", "BALLAB"),
    ("LLB", "LLB"),
]

section_choices = [
    ('A', 'A'),
    ('B', 'B'), 
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z'),
]

current_year_choices = [
    ('1st', '1st'),
    ('2nd', '2nd'), 
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th')
]

notification_type = [
    ('Marking Attendance', 'Marking Attendance')
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
    qid = models.CharField(max_length=15, default="000000",unique=True, null=False, blank=False)
    face_encoding = models.TextField(null=True, blank=True)
    anonymous = models.BooleanField(default=True,null=True, blank=True)
    user_type = models.CharField(max_length=100,choices=USER_TYPE,default="STUDENT",blank=False,null=False)
    country_code_for_mobile = models.CharField(max_length=10, default="00",null=False, blank=False)
    mobile = models.CharField(max_length=15,default="0000000000", null=False, blank=False)
    program = models.CharField(max_length=50, choices=courses_name_choices, null=True, blank=True)
    branch = models.CharField(max_length=50, choices=branch_choices,null=True, blank=True)
    section = models.CharField(max_length=5, choices=section_choices, null=True, blank=True)
    current_year = models.CharField(max_length=5, null=True, blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True,unique=True)
    approved = models.BooleanField(default=False)
    registered_at = models.DateTimeField(default=timezone.now,blank=False,null=False)
    updated_at = models.DateTimeField(default=None,null=True,blank=True)

    def __str__(self):
        return self.username
    
    def get_full_name(self):   
        return f"{self.first_name} {self.last_name}"
    


class PendingUser(models.Model):
    username = models.CharField(max_length=150, default=None,null=True, blank=True)
    qid = models.CharField(max_length=15, default="000000", unique=True, null=True, blank=True)
    face_encoding = models.TextField(null=True, blank=True)
    user_type = models.CharField(max_length=100,choices=USER_TYPE,default=None,blank=False,null=False)
    country_code_for_mobile = models.CharField(max_length=10, null=False, blank=False)
    mobile = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False)
    approved = models.BooleanField(default=False,null=True,blank=True)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    approved_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None,null=True)
    approved_at = models.DateTimeField(default=None,null=True)
    user_requested_at = models.DateTimeField(default=timezone.now,null=False,blank=False)

    def __str__(self):
        if self.approved:
            return f"{self.registration_number}:- {self.username} request APPROVED for user-type ({self.user_type})"
        elif not self.approved:
            return f"{self.registration_number}:- Pending Request of {self.username} for user-type ({self.user_type})"
        else:
            return "ERROR"



########### Start Club #######################################
class Club(models.Model):
    club_name = models.CharField(default="",max_length=150, unique=True)
    description = models.TextField(default="")
    logo = models.ImageField(default=None,upload_to='club_logos/')
    entry_fees = models.IntegerField(default=0, help_text="0 means FREE")
    members = models.ManyToManyField(CustomUser,blank=True,related_name='clubs_as_member')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    faculty_assigned = models.ManyToManyField(CustomUser,default=None,blank=False,related_name='faculty_assigned_club')

    def __str__(self):
        return self.club_name

class ClubMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None,null=False,blank=False,related_name='user_in_club')
    club = models.ForeignKey(Club,default=None, on_delete=models.CASCADE,null=False,blank=False,related_name='club_membership')
    position = models.CharField(max_length=100, choices=ROLE_CHOICES, default='GENERAL-MEMBER')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user not in self.club.members.all():
            self.club.members.add(self.user)
    
    def delete(self, *args, **kwargs):
        print("TRUEEEE")
        super().delete(*args, **kwargs)
        self.club.members.remove(self.user)

    def __str__(self):
        return f"{self.user.username} - {self.club.club_name} ({self.position})"


class ClubPayment(models.Model):
    club = models.ForeignKey(Club,on_delete=models.CASCADE, null=True, blank=True,related_name='club_payment')
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True,related_name='user_payment_club')
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    member_position = models.CharField(max_length=100,default="GENERAL-MEMBER",choices=ROLE_CHOICES,null=False,blank=False)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == False:
            clb = ClubMembership.objects.filter(user=self.user,club=self.club)
            for clb in clb:
                clb.delete()

        if self.status == True and self.user not in self.club.members.all():
            clb = ClubMembership.objects.filter(user=self.user,club=self.club)
            for clb in clb:
                clb.delete()
            ClubMembership.objects.create(
                user = self.user,
                club = self.club,
                position = self.member_position
            )
    
    def delete(self, *args, **kwargs):
        clb = ClubMembership.objects.filter(user=self.user,club=self.club)
        for clb in clb:
                clb.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.payment_id}"
    

class ClubGallery(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(default=None,upload_to='club_gallery/')
    
########### End Club #######################################

    

######################## Start Event #########################
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

    def __str__(self):
        return f"{self.event} by {self.club} on {self.event_date.strftime('%Y-%m-%d')}"


class StudentEventEnrolled(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    student_enrolled = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='student_enrolled_event', blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now, null=False,blank=False)
    actual_enrolled_time = models.DateField(default=timezone.now, null=True,blank=True)


class EventPayment(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.payment_id}"

######################### End Events Models #########################



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