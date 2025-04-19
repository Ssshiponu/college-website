from django.db import models
import os

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from cloudinary.models import CloudinaryField

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    description = models.TextField(null=True)
    department_head = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_department')
    established = models.DateField()
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Faculty(models.Model):
    DESIGNATION_CHOICES = [
        ('principal', 'অধ্যক্ষ'),
        ('vice principal', 'সহযোগী অধ্যক্ষ'),
        ('professor', 'অধ্যাপক'),
        ('associate professor', 'যুগ্ম অধ্যাপক'),
        ('assistant professor', 'সহযোগী অধ্যাপক'),
        ('lecturer', 'প্রভাষক'),
        ('staff', 'কর্মচারী'),
    ]

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    education = models.TextField(null=True)
    bio = models.TextField(null=True)
    photo = CloudinaryField('image', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True)

    
    class Meta:
        verbose_name_plural = "Faculty Members"
        ordering = ['designation', 'name']
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('routine', 'রুটিন'),
        ('academic', 'একাডেমিক'),
        ('admission', 'ভর্তি'),
        ('exam', 'পরীক্ষা'),
        ('event', 'অনুষ্ঠান'),
        ('other', 'অন্যান্য'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publish_date = models.DateTimeField(default=timezone.now)
    document = CloudinaryField('document', null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)
    is_important = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

class Program(models.Model):
    LEVEL_CHOICES = [
        ('hsc', 'Higher Secondary'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
    ]

    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    image = CloudinaryField('image', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('campus', 'ক্যাম্পাস'),
        ('event', 'ইভেন্ট'),
        ('students activity', 'ছাত্র কার্যক্রম'),
        ('other', 'অন্যান্য'),
    ]

    title = models.CharField(max_length=100)
    image = CloudinaryField('image', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Gallery"
        ordering = ['-upload_date']

    def __str__(self):
        return self.title

class Faq(models.Model):
    FAQ_PAGES = [
        ('admission', 'ভর্তি'),
        ('contact', 'যোগাযোগ'),
        ('notice', 'নোটিশ'),
    ]
    question = models.CharField(max_length=200)
    ans = models.TextField()
    page = models.CharField(choices=FAQ_PAGES, max_length=20)

    def __str__(self):
        return self.question