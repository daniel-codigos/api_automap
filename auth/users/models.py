from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=8)
    username = models.CharField(unique=True, max_length=10)
    password = models.CharField(max_length=20)
    email = models.CharField(unique=True,max_length=35)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class show_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()


class Save_bad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   # id = models.IntegerField()
    # Un campo de tipo JSONField para almacenar datos en formato JSON
    json = models.JSONField()

class SaveErrorParte(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.JSONField()
    def __str__(self):
        return {'info':self.info}

class Save_config(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Un campo de tipo JSONField para almacenar datos en formato JSON
    json = models.JSONField()


class Register_new_hour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,unique=True)
    hour_on = models.IntegerField()
    hour_off = models.IntegerField()
    status = models.CharField(max_length=1)
    joint_hour = models.BooleanField(default=True) #para poder tener horario de crecimiento y flora enlazao a 1 solo ;)
    use_hour = models.BooleanField(default=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.name,self.hour_on,self.hour_off,self.status)

class Register_new_enchufe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,unique=True)
    numero = models.IntegerField()
    

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.name,self.hour_on,self.hour_off,self.status)

class SaveUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username_infocol = models.CharField(max_length=10,null=True,unique=True)
    password_infocol = models.CharField(max_length=10,null=True,unique=True)
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.username_infocol,self.password_infocol)
        #return {'username':self.username_infocol,'password':self.password_infocol}


class SaveFinData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   # id = models.IntegerField()
    # Un campo de tipo JSONField para almacenar datos en formato JSON
    json = models.JSONField()