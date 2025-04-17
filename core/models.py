from django.db import models
import os


# Create your models here.

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string

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
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Lecturer', 'Lecturer'),
        ('Staff', 'Staff'),
    ]

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    education = models.TextField(null=True)
    bio = models.TextField(null=True)
    photo = models.ImageField(upload_to='faculty/', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    
    class Meta:
        verbose_name_plural = "Faculty Members"
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

        # save a 96px width copy of the image with width auto as per aspect ratio
        if self.photo:
            try:
                from PIL import Image
                from io import BytesIO
                from django.core.files.base import ContentFile

                img = Image.open(self.photo)
                aspect_ratio =img.height / img.width 
                new_height = int(96 * aspect_ratio)
                img = img.resize((96, new_height), Image.Resampling.LANCZOS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_file = ContentFile(img_io.getvalue(), name=self.photo.name)
                self.photo.save(f"96_{self.photo.name}", img_file, save=False)
            except Exception as e:
                # Log the error or handle it as needed
                print(f"Error processing image: {e}")

    def delete(self, *args, **kwargs):
        if self.photo:
            os.remove(self.photo.path)
            os.remove(self.photo.path.replace("faculty/", "faculty/96_faculty/"))
        super().delete(*args, **kwargs)

    # get 96 px height image url
    @property
    def photo_96(self):
        try:
            return self.photo.url.replace("faculty/", "faculty/96_faculty/")
        except:
            return None

    def __str__(self):
        return f"{self.name}"

class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('routin', 'রুটিন'),
        ('academic', 'একাডেমিক'),
        ('admission', 'ভর্তি'),
        ('examination', 'পরীক্ষা'),
        ('event', 'অনুষ্ঠান'),
        ('other', 'অন্যান্য'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publish_date = models.DateTimeField(default=timezone.now)
    document = models.FileField(upload_to='notices/', null=True, blank=True)
    is_important = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    @property
    def is_image(self):
        if self.document.url.endswith("jpg"):
            return True
        return False
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    def remove(self, *args, **kwargs):
        if self.document:
            self.document.delete()
        super().remove(*args, **kwargs)

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

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = get_random_string(length=16)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('campus', 'Campus'),
        ('event', 'Event'),
        ('student', 'Student Activities'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Gallery"
        ordering = ['-upload_date']

    def remove(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().remove(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Faq(models.Model):
    FAQ_PAGES = [
        ('Admission', 'Admission'),
        ('Contact', 'Contact'),
        ('Notice', 'Notice'),
    ]
    question = models.CharField(max_length=200)
    ans = models.TextField()
    page = models.CharField(choices=FAQ_PAGES)

    def __str__(self):
        return self.question