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

student_user = "STUDENT"
faculty_user = "FACULTY"
dean_user = "DEAN"
vc_user = "VC"
director_user = "DIRECTOR"
non_faculty_user = "NON-FACULTY"
admin_user = "ADMIN"


#Only These Type of User can access Moderator Page (Admin Page)
MODERATOR_USER_LIST = [admin_user,vc_user,director_user,dean_user]

#This User Type will be Stored and shown in DB
USER_TYPE = [
    (student_user, student_user),
    (faculty_user, faculty_user),
    (dean_user,dean_user),
    (vc_user,vc_user),
    (director_user,director_user),
    (non_faculty_user,non_faculty_user),
    (admin_user, admin_user),
]


president_user = "PRESIDENT"
vice_precident_user = "VICE-PRECIDENT"
core_member_user = "CORE-MEMBER"
general_member_user = "GENERAL-MEMBER" 

#Club Members/Core Members
ROLE_CHOICES = [
        (president_user, president_user),
        (vice_precident_user, vice_precident_user),
        (core_member_user, core_member_user),
        (general_member_user,general_member_user)
    ]