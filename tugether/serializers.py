from rest_framework import serializers
from tugether.models import User, Event, Comment, Category
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'userid', 'firstname', 'lastname', 'major','department','nation','title','year','age','active')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id','topic', 'join', 'createby', 'location', 'approve','description',
        'facebook','line','web','phone','hashtag','bcapprove','posterpic','createdate',
        'updatedate','startdate','enddate','eventstdate','eventenddate','active','limited')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = ('eventid','createby','createdate','active','details')

class CategorySerializable(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = ('categoryname','categorydetails','userid','eventid','active')

# class Category(models.Model):
#     categoryname = models.CharField(max_length=100)
#     categorydetails = models.TextField()
#     userid = models.ManyToManyField(User)
#     eventid = models.ManyToManyField(Event)
#     active = models.BooleanField(default=True)


# class Comment(models.Model):
#     eventid = models.ForeignKey(Event, on_delete=models.CASCADE)
#     createby = models.ForeignKey(User, on_delete=models.CASCADE)
#     major = models.CharField(max_length=100)
#     createdate = models.DateTimeField('Create Date')
#     active = models.BooleanField(default=True)
#     details = models.TextField()


# topic = models.CharField(max_length=200)approve
#     join = models.ManyToManyField(User)
#     createby = models.IntegerField(default=0)
#     location = models.CharField(max_length=200)
#      = models.CharField(max_length=4)
#     description = models.CharField(max_length=500)
# #  commentid = models.CharField(max_length=200)
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
#     eventstdate = models.DateTimeField('Event Start Date')
#     eventenddate = models.DateTimeField('Event End Date')
#     active = models.BooleanField(default=True)
#     limited = models.IntegerField(validators=[MaxValueValidator(100)])

# class TugetherSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     # code = serializers.CharField(style={'base_template': 'textarea.html'})
#     # linenos = serializers.BooleanField(required=False)
#     # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     userid = serializers.CharField(max_length=20)
#     firstname = serializers.CharField(max_length=30)
#     lastname = serializers.CharField(max_length=30)
#     major = serializers.CharField(max_length=100)
#     department = serializers.CharField(max_length=100)
#     nation = serializers.CharField(max_length=20)
#     title = serializers.CharField(max_length=20)
#     year = serializers.CharField(max_length=1)   
#     age = serializers.IntegerField(validators=[MaxValueValidator(100)])
#     active = serializers.BooleanField(default=True)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return User.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """

#         instance.userid = validated_data.get('userid', instance.userid)
#         instance.firstname = validated_data.get('firstname', instance.firstname)
#         instance.lastname = validated_data.get('lastname', instance.lastname)
#         instance.major = validated_data.get('major', instance.major)
#         instance.department = validated_data.get('department', instance.department)
#         instance.nation = validated_data.get('nation', instance.nation)
#         instance.title = validated_data.get('title', instance.title)
#         instance.year = validated_data.get('year', instance.year)
#         instance.age = validated_data.get('age', instance.age)
#         instance.active = validated_data.get('active', instance.active)

#         # instance.title = validated_data.get('title', instance.title)
#         # instance.code = validated_data.get('code', instance.code)
#         # instance.linenos = validated_data.get('linenos', instance.linenos)
#         # instance.language = validated_data.get('language', instance.language)
#         # instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance