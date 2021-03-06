import uuid
import string
import random
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import os
# ---------------------------------------------------
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import random
import string
import datetime
# ---------------------------------------------------

User = get_user_model()

# PROJECT_WORKED_CHOICE = [
#     ('irsc','IRSC'),
#     ('intellify','Intellify'),
#     ('isafe','iSAFE Assisst'),
#     ('solve','Solve(Multiple Projects)'),
# ]
# PROFILE_CHOICE = [
#     ('FR', 'Freshman'),
#     ('SO', 'Sophomore'),
#     ('JR', 'Junior'),
#     ('SR', 'Senior'),
#     ('GR', 'Graduate'),
# ]
# TYPE_OF_INTERNSHIP = [
#     ('wfh', 'work from home'),
#     ('wfo', 'wrok from office')
# ]

# STATUS = [
#     ('V', 'Volunteer'),
#     ('I', 'Intern')
# ]
# TENURE_CHOICE = [(f'{i} Month', f'{i} month') for i in range(1,13)]

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=225,editable=False,unique=True)

    def save(self, *args, **kwargs):
        self.registration_number = "".join(random.choices(string.digits,k=8))
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    def get_full_name(self):
        return "{} {}".format(self.first_name,self.last_name)

    @property
    def is_staff(self):
        return self.user.is_staff

    @property
    def is_superuser(self):
        return self.user.is_superuser


class Profile(models.Model):
    intern = models.OneToOneField(UserProfile, related_name='profile', on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    forgot_password_timestamp = models.DateTimeField(auto_now=True)



class ProjectWorkedChoice(models.Model):
    project_worked = models.CharField(max_length=225)

    def __str__(self):
        return "{}".format(self.project_worked)

class ProfileChoice(models.Model):
    profile = models.CharField(max_length=225)

    def __str__(self):
        return "{}".format(self.profile)

class StatusChoice(models.Model):
    status = models.CharField(max_length=225)

    def __str__(self):
        return "{}".format(self.status)

class TypeOfInternChoice(models.Model):
    type_of_intern = models.CharField(max_length=225)

    def __str__(self):
        return "{}".format(self.type_of_intern)

class TenureChoice(models.Model):
    tenure = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.tenure)


class Certificate(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userprofile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    certificate_number = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    certificate_pdf = models.FileField(upload_to='certificates/pdf',default='default.pdf')
    certificate_png = models.FileField(upload_to='certificates/png',default='default.png')

    def save(self, *args, **kwargs):
        self.userprofile = self.user.userprofile
        super(Certificate, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.userprofile.get_full_name(),self.certificate_number)


REPORT_STATUS = [
    ('A', 'Approved'),
    ('P', 'Pending'),
    ('R', 'Rejected')
]

class PersonalDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    ph_contact_no = models.CharField(max_length=15)
    whatsapp_no = models.CharField(max_length=15)
    project = models.ForeignKey(ProjectWorkedChoice,on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileChoice,on_delete=models.CASCADE)
    type_of_internship = models.ForeignKey(TypeOfInternChoice,on_delete=models.CASCADE)
    joining_date = models.DateField(auto_now_add=True)
    pan_number = models.CharField(max_length=20)
    aadhaar = models.CharField(max_length=20)
    emergency_contact_no = models.CharField(max_length=15)
    bank_account_no = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=15)
    dob = models.DateField()
    permanent_address = models.TextField()
    current_address = models.TextField()
    biometric_id_number = models.CharField(max_length=225)
    internship_tenure = models.ForeignKey(TenureChoice,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume')
    request_edit = models.BooleanField(default=False)
    is_editable = models.CharField(choices=REPORT_STATUS,default='P',max_length=10)
    edit_reason = models.TextField()

    def save(self, *args, **kwargs):
        self.userprofile = self.user.userprofile
        super(PersonalDetail, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.userprofile.get_full_name())

class Project(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userprofile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileChoice,on_delete=models.CASCADE)
    project_worked_on = models.ForeignKey(ProjectWorkedChoice,on_delete=models.CASCADE)
    status = models.ForeignKey(StatusChoice,on_delete=models.CASCADE)
    tenure = models.ForeignKey(TenureChoice,on_delete=models.CASCADE)
    joining_date = models.DateField()
    end_date = models.DateField()
    upload_traker_link = models.URLField()
    detail_of_work = models.TextField()
    mentor_or_leader = models.TextField()
    request_edit = models.BooleanField(default=False)
    is_editable = models.CharField(choices=REPORT_STATUS,default='P',max_length=10)
    edit_reason = models.TextField()

    def save(self, *args, **kwargs):
        self.userprofile = self.user.userprofile
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.userprofile.first_name,self.project_worked_on)


class Report(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    userprofile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=500)
    upload_report = models.FileField(upload_to='reports')
    status = models.CharField(choices=REPORT_STATUS, max_length=2,default='P')

    def save(self, *args, **kwargs):
        self.userprofile = self.user.userprofile
        super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - Project: {}, status: {}".format(self.userprofile.first_name,self.project_name,self.status)


class CertificateConfig(models.Model):
    namex = models.CharField(default='0', max_length=50)
    namey = models.CharField(default='0', max_length=50)

    profilex = models.CharField(default='0', max_length=50)
    profiley = models.CharField(default='0', max_length=50)

    typex = models.CharField(default='0', max_length=50)
    typey = models.CharField(default='0', max_length=50)

    d1x = models.CharField(default='0', max_length=50)
    d1y = models.CharField(default='0', max_length=50)

    d2x = models.CharField(default='0', max_length=50)
    d2y = models.CharField(default='0', max_length=50)

    datex = models.CharField(default='0', max_length=50)
    datey = models.CharField(default='0', max_length=50)

    renox = models.CharField(default='0', max_length=50)
    renoy = models.CharField(default='0', max_length=50)

    logox = models.CharField(default='0', max_length=50)
    logoy = models.CharField(default='0', max_length=50)

    signx = models.CharField(default='0', max_length=50)
    signy = models.CharField(default='0', max_length=50)

    namesize = models.CharField(default='0', max_length=50)
    typesize = models.CharField(default='0', max_length=50)
    profilesize = models.CharField(default='0', max_length=50)
    datesize = models.CharField(default='0', max_length=50)
    dsize = models.CharField(default='0', max_length=50)

    def filerename(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4(), ext)
        return os.path.join('certificate_files', filename)

    certificate_img = models.ImageField(
        upload_to=filerename, default='certificate.jpg')
    certificate_pdf = models.FileField(
        upload_to=filerename, default='certificate.pdf')
    logo_img = models.ImageField(upload_to=filerename, default='logo.png')
    sign_img = models.ImageField(upload_to=filerename, default='signature.png')

    namefont = models.FileField(
        upload_to='certificate_file/fonts', default='default.ttf')
    otherfont = models.FileField(
        upload_to='certificate_file/fonts', default='default.ttf')

    cktl = models.CharField(default="1200", max_length=50)
    cktw = models.CharField(default="1600", max_length=50)
    logol = models.CharField(default='165', max_length=50)
    logow = models.CharField(default='165', max_length=50)
    signl = models.CharField(default='78', max_length=50)
    signw = models.CharField(default='224', max_length=50)


# signal settings


from .functions import generate_token, send_email, delete_user_inactive, delete_inactive

@receiver(post_save, sender=UserProfile)
def save_profile(sender, instance,created, **kwargs):
    # delete_inactive(instance.email)
    if created:
        Profile.objects.create(intern=instance, activation_key=generate_token())
        id = instance.user.id
        full_name = instance.first_name + ' ' + instance.last_name
        send_email(full_name, id, instance.user.email)
    pass

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_profile(sender, instance,created, **kwargs):
#     # delete_inactive(instance.email)
#     if created:
#         if instance.is_superuser:
#             UserProfile.objects.create(user=instance, first_name='super', last_name='user')
#             intern = UserProfile.objects.all().filter(user=instance).first()
#             Profile.objects.create(intern=intern, activation_key=generate_token())
#             id = intern.user.id
#             full_name = intern.first_name + ' ' + intern.last_name
#             send_email(full_name, id, intern.user.email)
#             print('Please check your mail to verify email')
    # pass

