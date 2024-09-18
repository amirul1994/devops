#from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
#from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# define what a user and a superuser is
class CustomUserManager(BaseUserManager):
    def create_user(self, name, age, profession, address, password):
        if not name: 
            raise ValueError('Users must have a name')
        
        user = self.model(name=name, age=age, profession=profession, 
                          address=address, password=make_password(password),)
        #user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    """
    def create_superuser(self, name, age, profession, address, password=None):
        user = self.create_user(name=name, age=age, profession=profession, 
                                address=address, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    """

class CustomUser(models.Model):
    name = models.TextField(max_length=50, unique=True)
    age = models.TextField(max_length=4)
    profession = models.TextField(max_length=50)
    address = models.TextField(max_length=100)
    password = models.CharField(max_length=128) # Django uses the PBKDF2 password hasher by default, which generates a 64-character hash. 
    last_login = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['age', 'profession', 'address', 'password']

    class Meta:
        db_table = 'userinfo'
        managed = False
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    

