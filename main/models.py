from djongo import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import datetime
# Create your models here.
import gridfs
from PIL import Image
import io
import uuid

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("Email is not provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Users(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=128, default=uuid.uuid4)
    email = models.EmailField(unique=True, max_length=30)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:

        db_table ='Users'
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    



   
    

class Fixtures(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    home_team = models.CharField(max_length=120)
    away_team= models.CharField(max_length=60)    
    time=models.TextField(max_length=60)
    home_win=models.TextField(max_length=60)
    away_win=models.TextField(max_length=60)
    date=models.TextField(max_length=50 ,default="today")
    draw=models.TextField(max_length=50 ,default="today")
    
    
    class Meta:

        db_table='fixtures'
        verbose_name = 'fixtures'
        verbose_name_plural ='fixtures'
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Pledges(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    homeTeam = models.CharField(max_length=120)
    awayTeam= models.CharField(max_length=60)    
    date=models.TextField(default="No Id")
    time=models.TextField(max_length=60)
    day=models.TextField(max_length=50 ,default="thursday")
    amount=models.TextField(max_length=50,default=20)
    placed=models.BooleanField(default=False)
    option=models.TextField(max_length=20)
    progress=models.TextField(max_length=50,default=20)
    pledger=models.TextField(max_length=50)
    placer=models.TextField(max_length=50)
    outcome=models.TextField(max_length=50)
    
    
    class Meta:

        db_table ='pledges'
        verbose_name = 'pledges'
        verbose_name_plural = 'pledges'
    def __str__(self):
        return self.homeTeam
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
    
    
class Posts(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=120)
    time= models.CharField(max_length=60)    
    date=models.TextField(default="No Id")
    info=models.TextField(max_length=60)
    likes=models.TextField(max_length=50 ,default="thursday")
    share=models.TextField(max_length=50,default=20)
    comments=models.BooleanField(default=False)
    country=models.TextField(max_length=50,default=20)
    club=models.TextField(max_length=50)
    field_name = models.ImageField(
    upload_to=None, 
    height_field=None, 
    width_field=None, 
    max_length=100, 
    
)
    
    
    
    
    class Meta:

        db_table ='posts'
        verbose_name = 'posts'
        verbose_name_plural = 'posts'
    def __str__(self):
        return self.homeTeam
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
class Pending(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    senderId= models.CharField(max_length=100)
    receiverId= models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    time = models.TextField() 
    class Meta:

        db_table ='Pending'
        verbose_name = 'Pending'
        verbose_name_plural = 'Pending'
    def __str__(self):
        return self.senderId
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
class PostMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    userId= models.CharField(max_length=100)
    fullname= models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    residence = models.TextField() 
    phone = models.TextField() 
    info = models.TextField() 
    education=models.TextField()
    
    class Meta:

        db_table ='Chats'
        verbose_name = 'Chats'
        verbose_name_plural = 'Chats'
    def __str__(self):
        return self.userid
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    
    

    
    
    
    
    
    
    
    








    
        #if not title:
            #raise ValueError("title is not provided")
        #title = self.normalize_email(email)
        #user = self.model(email=email, **extra_field)
        #user.set_password(password)
        #user.save(using=self.db)
        #return user


