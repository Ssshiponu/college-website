from django.views.generic import ListView, DetailView, TemplateView
from .models import Department, Faculty, Notice, Program, Event, Gallery, Faq
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notices'] = Notice.objects.all()[:3]
        context['events'] = Event.objects.filter(is_featured=True)[:3]
        context['principal'] = Faculty.objects.filter(designation='principal').first()
        return context

class HistoryView(TemplateView):
    template_name = 'history.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['principal'] = Faculty.objects.filter(designation='principal').first()
        return context

class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculty.html'
    context_object_name = 'faculty'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        department_filter = self.request.GET.get('department', '')
        
        if search_query:    
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(department__name__icontains=search_query) | Q(designation__icontains=search_query)
            )
        
        if department_filter:
            queryset = queryset.filter(department__name__icontains=department_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['department_filter'] = self.request.GET.get('department', '')
        return context

class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'faculty_detail.html'
    context_object_name = 'faculty'

class DepartmentListView(ListView):
    model = Department
    template_name = "departments.html" 
    context_object_name = "departments"  
    ordering = ["name"]  
    
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['faculty'] = Faculty.objects.filter(department=department)
        context['programs'] = Program.objects.filter(department=department)
        return context

class NoticeListView(ListView):
    model = Notice
    template_name = 'notice.html'
    context_object_name = 'notices'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_notice'] = Notice.objects.filter(is_important=True).order_by('-publish_date').first()
        context['notices'] = Notice.objects.exclude(id=context['featured_notice'].id)
        context['categories'] = Notice.CATEGORY_CHOICES
        return context

class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notice_detail.html'
    context_object_name = 'notice'

class ProgramListView(ListView):
    model = Program
    template_name = 'programs.html'
    context_object_name = 'programs'

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'program_detail.html'
    context_object_name = 'program'

class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_event'] = Event.objects.filter(is_featured=True).order_by('-time').first()
        context['events'] = Event.objects.all().exclude(id=context['featured_event'].id)
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

class GalleryView(ListView):
    model = Gallery
    template_name = 'gallery.html'
    context_object_name = 'images'
    paginate_by = 12

class CalenderView(TemplateView):
    template_name = 'calender.html'

class AlumniView(TemplateView):
    template_name = 'alumni.html'

class ResultView(TemplateView):
    template_name = 'result.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Faq.objects.filter(page='Contact')
        return context

class CampusView(TemplateView):
    model = Gallery
    context_object_name = 'campus_images'
    template_name = 'campus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campus_images'] = Gallery.objects.filter(category='campus')[:4]
        return context

class AdmissionView(TemplateView):
    template_name = 'admission.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = Faq.objects.filter(page='Admission')
        return context