from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)

    def __str__(self):
        return '%s' % (self.name)

class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(100.00, message='Price must be greater than 100.00 !!'), MaxValueValidator(200.00, message='Price must be less than 200.00 !!')])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    num_reviews = models.PositiveIntegerField(default=0)
    hours = models.IntegerField(default=10, validators=[MinValueValidator(0, message='Hours should not be less than 0')])

    def __str__(self):
        return '%s' % (self.title)
    def get_cost(self):
        return self.price

class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree')
    ]
    CITY_CHOICES = [
        ('WS', 'Windsor'),
        ('CG', 'Calgary'),
        ('MR', 'Montreal'),
        ('VC', 'Vancouver')
    ]
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province = models.CharField(max_length=2, default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='media', blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Order(models.Model):
    courses = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student, related_name='orders', on_delete=models.CASCADE)
    ORDER_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On Hold')
    ]
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def __str__(self):
        return "Order from " + self.Student.first_name + ' ' + self.Student.last_name + ' with total price %s' % self.total_cost()
    def total_cost(self):
        return sum([course.price for course in self.courses.all()])
    def total_items(self):
        return self.courses.all().count()

class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return 'Reviewer: %s\nCourse: %s\nRating: %s' % (self.reviewer, self.course, self.rating)