from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    
    categoryname = models.CharField(max_length=100)
    categorydetails = models.TextField()
    #userid = models.ManyToManyField(User)
    #eventid = models.ManyToManyField(Event)
    active = models.BooleanField(default=True)

# class User(models.Model):
#     userid = models.CharField(max_length=20, primary_key=True)
#     firstname = models.CharField(max_length=30)
#     lastname = models.CharField(max_length=30)
#     major = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     nation = models.CharField(max_length=20)
#     title = models.CharField(max_length=20)
#     year = models.CharField(max_length=1)   
#     age = models.IntegerField(validators=[MaxValueValidator(100)])
#     active = models.BooleanField(default=True)
#     categoryid = models.ManyToManyField(Category)       #edit
#     userpic = models.TextField() 

class Event(models.Model):
    topic = models.CharField(max_length=200)
    join = models.ManyToManyField(User, default=[])  
    createby = models.CharField(max_length=20)
    #createby = models.ForeignKey(User, on_delete=models.CASCADE)   #edit
    categoryid = models.ManyToManyField(Category , default=[])           #edit
    location = models.CharField(max_length=200, blank=True, null=True )
    approve = models.CharField(max_length=4)
    description = models.CharField(max_length=500 ,blank=True, null=True)
#  commentid = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    line = models.CharField(max_length=20, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)   
    hashtag = models.TextField(blank=True, null=True)
    bcapprove = models.TextField(blank=True, null=True)
    posterpic = models.TextField()
    createdate = models.DateTimeField('Create Date')
    updatedate = models.DateTimeField('Editdate Date' ,blank=True, null=True)
    # startdate = models.DateTimeField('Start Date')
    # enddate = models.DateTimeField('End Date')
    eventstdate = models.DateTimeField('Event Start Date')
    eventenddate = models.DateTimeField('Event End Date')
    active = models.BooleanField(default=True)
    limited = models.IntegerField(validators=[MaxValueValidator(10000)] , blank=True, null=True)


class Comment(models.Model):
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
    createby = models.ForeignKey(User, on_delete=models.CASCADE)
 #   major = models.CharField(max_length=100)
    createdate = models.DateTimeField('Create Date')
    active = models.BooleanField(default=True)
    details = models.TextField()
#   commentid = models.CharField(max_length=200)

class Noti(models.Model):

    types = models.TextField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    active = models.BooleanField(default=True)  
    # editevent = models.CharField(max_length=200)
    # replycm = models.CharField(max_length=200)
    # eventofcate = models.CharField(max_length=200)
      
    # des = models.CharField(max_length=200)
    







# from django.db import models
# from django.core.validators import MaxValueValidator

# # Create your models here.

# class User(models.Model):
#     userid = models.CharField(max_length=20)
#     firstname = models.CharField(max_length=30)
#     lastname = models.CharField(max_length=30)
#     major = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     nation = models.CharField(max_length=20)
#     title = models.CharField(max_length=20)
#     year = models.CharField(max_length=1)   
#     age = models.IntegerField(validators=[MaxValueValidator(100)])
#     active = models.BooleanField(default=True)

# class Event(models.Model):
#     topic = models.CharField(max_length=200)

#     createby = models.ManyToManyField(User) 
#     location = models.CharField(max_length=200)
#     approve = models.CharField(max_length=4)
#     description = models.CharField(max_length=500)
#     commentid = models.CharField(max_length=200)
#     facebook = models.CharField(max_length=200)
#     line = models.CharField(max_length=20)
#     web = models.CharField(max_length=200)
#     phone = models.CharField(max_length=20)   
#     hashtag = models.TextField()
#     bcapprove = models.TextField()
#     posterpic = models.TextField()
#     createdate = models.DateTimeField('Create Date')
#     updatedate = models.DateTimeField('Editdate Date')
#     startdate = models.DateTimeField('Start Date')
#     enddate = models.DateTimeField('End Date')
#     active = models.BooleanField(default=True)
#     limited = models.IntegerField(validators=[MaxValueValidator(100)])

# class Comment(models.Model):
#     eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
#     createby = models.ForeignKey(User, on_delete=models.CASCADE)
#     major = models.CharField(max_length=100)
#     createdate = models.DateTimeField('Create Date')
#     active = models.BooleanField(default=True)
#     details = models.TextField()

# class Category(models.Model):
#     categoryname = models.CharField(max_length=100)
#     categorydetails = models.TextField()
#     createby = models.ManyToManyField(User)
#     eventid = models.ManyToManyField(Event)
#     active = models.BooleanField(default=True)