
from django.db import models
from django.db.models import Model
from ckeditor.fields import RichTextField




class Stream(models.Model):
    name = models.CharField(max_length=255)
   

    def __str__(self):
        return self.name


class CourseType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.TextField(max_length=255)
    domain = models.CharField(max_length=255,unique= True)




    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField(max_length=300,blank=True, null=True)
    overview = RichTextField(max_length=900, default='course overview here')
    logo = models.ImageField(upload_to='college_logos/')
    address = RichTextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(default='example@gmail.com')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    affiliation = RichTextField(max_length=500,default='Affiliation details here')
    admission=RichTextField(max_length=500, default='admission formalities here')
    is_featured = models.BooleanField(default=False)
    website=models.CharField(max_length=200,default='wwww.example.com')
   
    

    def __str__(self):
        return self.name

class CollegeCourse(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.IntegerField()
    eligibility = RichTextField(default='Eligibilty criteria')
    syllabus = RichTextField(default='Syllabus here')


    class Meta:
        unique_together = ['college', 'course']


    def __str__(self):
        return f"{self.college.name} - {self.course.name}"

class Enquiry(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    price = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country_code = models.CharField(max_length=6,default="+91")
    phone = models.CharField(max_length=15)
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'In Progress'),
        (3, 'Completed'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)
    note = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.college.name} - {self.course.name}"







