from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=20, primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    major = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    nation = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    year = models.CharField(max_length=1)   
    age = models.IntegerField(validators=[MaxValueValidator(100)])
    active = models.BooleanField(default=True)

class Event(models.Model):
    topic = models.CharField(max_length=200)
    join = models.ManyToManyField(User)
    createby = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    approve = models.CharField(max_length=4)
    description = models.CharField(max_length=500)
#  commentid = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200)
    line = models.CharField(max_length=20)
    web = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)   
    hashtag = models.TextField()
    bcapprove = models.TextField()
    posterpic = models.TextField()
    createdate = models.DateTimeField('Create Date')
    updatedate = models.DateTimeField('Editdate Date')
    startdate = models.DateTimeField('Start Date')
    enddate = models.DateTimeField('End Date')
    eventstdate = models.DateTimeField('Event Start Date')
    eventenddate = models.DateTimeField('Event End Date')
    active = models.BooleanField(default=True)
    limited = models.IntegerField(validators=[MaxValueValidator(100)])

class Comment(models.Model):
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
    createby = models.ForeignKey(User, on_delete=models.CASCADE)
 #   major = models.CharField(max_length=100)
    createdate = models.DateTimeField('Create Date')
    active = models.BooleanField(default=True)
    details = models.TextField()

class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    categorydetails = models.TextField()
    userid = models.ManyToManyField(User)
    eventid = models.ManyToManyField(Event)
    active = models.BooleanField(default=True)








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