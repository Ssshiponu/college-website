from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    department_head = models.ForeignKey(
        'Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_department'
    )
    established = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['slug'])]

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Department name cannot be empty.")
        if not self.code.strip():
            raise ValidationError("Department code cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while Department.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving department: {e}")

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
    education = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = CloudinaryField('image', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "শিক্ষক-শিক্ষিকা"
        ordering = ['designation', 'name']
        indexes = [models.Index(fields=['slug'])]

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Faculty name cannot be empty.")
        if self.email and not self.email.strip():
            raise ValidationError("Email cannot be empty if provided.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            original_slug = self.slug
            counter = 1
            while Faculty.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving faculty: {e}")

    def __str__(self):
        return self.name

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
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publish_date = models.DateTimeField(default=timezone.now)
    document = CloudinaryField('document', blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    is_important = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "নোটিশ"
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_important', '-publish_date']),
            models.Index(fields=['slug']),
        ]

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Notice title cannot be empty.")
        if len(self.title) < 5:
            raise ValidationError("Notice title must be at least 5 characters long.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = slugify(self.title)[:50]
            original_slug = self.slug
            counter = 1
            while Notice.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving notice: {e}")

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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    description = models.TextField()
    duration = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "প্রোগ্রাম"
        indexes = [models.Index(fields=['slug'])]

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Program name cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.level}")[:50]
            original_slug = self.slug
            counter = 1
            while Program.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving program: {e}")

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "ইভেন্ট"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['is_featured', '-date']),
            models.Index(fields=['slug']),
        ]

    def clean(self):
        if not self.title.strip():
            raise ValidationError("Event title cannot be empty.")
        if self.date and self.date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = slugify(self.title)[:50]
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        # Automatically set is_featured to False for past events
        if self.date and self.date < timezone.now().date():
            self.is_featured = False
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving event: {e}")

    def __str__(self):
        return self.title

class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('campus', 'ক্যাম্পাস'),
        ('history', 'ইতিহাস'),
        ('event', 'ইভেন্ট'),
        ('students activity', 'ছাত্র কার্যক্রম'),
        ('other', 'অন্যান্য'),
    ]

    title = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "গ্যালারি"
        ordering = ['-upload_date']
        indexes = [models.Index(fields=['category'])]

    def clean(self):
        if not self.image:
            raise ValidationError("Gallery image is required.")

    def save(self, *args, **kwargs):
        self.full_clean()
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving gallery image: {e}")

    def __str__(self):
        return self.title or f"Image ({self.category})"

class Faq(models.Model):
    FAQ_PAGES = [
        ('admission', 'ভর্তি'),
        ('contact', 'যোগাযোগ'),
    ]
    question = models.CharField(max_length=200)
    ans = models.TextField()
    page = models.CharField(choices=FAQ_PAGES, max_length=20)

    class Meta:
        verbose_name_plural = "প্রশ্ন-উত্তর"
        ordering = ['question']

    def clean(self):
        if not self.question.strip():
            raise ValidationError("FAQ question cannot be empty.")
        if not self.ans.strip():
            raise ValidationError("FAQ answer cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving FAQ: {e}")

    def __str__(self):
        return self.question