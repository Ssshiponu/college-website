from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
import logging
from .models import Department, Faculty, Notice, Program, Event, Gallery, Faq

# Configure logging
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['notices'] = Notice.objects.select_related().order_by('-publish_date')[:3]
            context['events'] = Event.objects.filter(is_featured=True).order_by('-date')[:3]
            context['principal'] = Faculty.objects.filter(designation='principal').first()
        except Exception as e:
            logger.error(f"Error in HomeView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load homepage content. Please try again later.")
            context['notices'] = []
            context['events'] = []
            context['principal'] = None
        return context

class HistoryView(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['gallery'] = Gallery.objects.filter(category='history').order_by('-upload_date')[:3]
        except Exception as e:
            logger.error(f"Error in HistoryView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load history gallery. Please try again later.")
            context['gallery'] = []
        return context

class FacultyListView(ListView):
    model = Faculty
    template_name = 'faculty.html'
    context_object_name = 'faculty'
    paginate_by = 10  # Added pagination

    def get_queryset(self):
        try:
            queryset = super().get_queryset().select_related('department')
            search_query = self.request.GET.get('search', '').strip()
            department_filter = self.request.GET.get('department', '').strip()

            if search_query:
                if len(search_query) < 2:
                    messages.warning(self.request, "Search term must be at least 2 characters long.")
                else:
                    queryset = queryset.filter(
                        Q(name__icontains=search_query) |
                        Q(department__name__icontains=search_query) |
                        Q(designation__icontains=search_query)
                    )

            if department_filter:
                queryset = queryset.filter(department__name__icontains=department_filter)

            return queryset.order_by('designation', 'name')
        except Exception as e:
            logger.error(f"Error in FacultyListView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load faculty list. Please try again later.")
            return Faculty.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['departments'] = Department.objects.all()
            context['search_query'] = self.request.GET.get('search', '')
            context['department_filter'] = self.request.GET.get('department', '')
            context['get_params'] = self.request.GET.urlencode()
        except Exception as e:
            logger.error(f"Error in FacultyListView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load faculty filters. Please try again later.")
            context['departments'] = []
        return context

class FacultyDetailView(DetailView):
    model = Faculty
    template_name = 'faculty_detail.html'
    context_object_name = 'faculty'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ObjectDoesNotExist:
            logger.error(f"Faculty not found: {self.kwargs.get('slug')}")
            raise Http404("Faculty member not found.")

class DepartmentListView(ListView):
    model = Department
    template_name = "departments.html"
    context_object_name = "departments"
    ordering = ["name"]
    paginate_by = 10  # Added pagination

    def get_queryset(self):
        try:
            return super().get_queryset().select_related('department_head')
        except Exception as e:
            logger.error(f"Error in DepartmentListView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load departments. Please try again later.")
            return Department.objects.none()

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ObjectDoesNotExist:
            logger.error(f"Department not found: {self.kwargs.get('slug')}")
            raise Http404("Department not found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            department = self.get_object()
            context['faculty'] = Faculty.objects.filter(department=department).select_related('department')
            context['programs'] = Program.objects.filter(department=department)
        except Exception as e:
            logger.error(f"Error in DepartmentDetailView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load department details. Please try again later.")
            context['faculty'] = []
            context['programs'] = []
        return context

class NoticeListView(ListView):
    model = Notice
    template_name = 'notice.html'
    context_object_name = 'notices'
    paginate_by = 1

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            category = self.request.GET.get('category', '').strip()
            search = self.request.GET.get('search', '').strip()

            if category:
                if category not in dict(Notice.CATEGORY_CHOICES):
                    messages.warning(self.request, "Invalid category selected.")
                    raise ValueError("Invalid category.")
                queryset = queryset.filter(category=category)

            if search:
                if len(search) < 2:
                    messages.warning(self.request, "Search term must be at least 2 characters long.")
                    raise ValueError("Search term too short.")
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )

            return queryset.order_by('-publish_date')
        except ValueError as e:
            logger.warning(f"Invalid query parameters in NoticeListView: {e}")
            return Notice.objects.none()
        except Exception as e:
            logger.error(f"Error in NoticeListView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load notices. Please try again later.")
            return Notice.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            featured_notice = Notice.objects.filter(is_important=True).order_by('-publish_date').first()
            context['featured_notice'] = featured_notice
            context['notices'] = self.object_list  # Use paginated queryset
            context['categories'] = Notice.CATEGORY_CHOICES
            context['get_params'] = self.request.GET.urlencode()
        except Exception as e:
            logger.error(f"Error in NoticeListView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load notice data. Please try again later.")
            context['featured_notice'] = None
            context['notices'] = Notice.objects.none()
            context['categories'] = []
        return context

class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notice_detail.html'
    context_object_name = 'notice'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ObjectDoesNotExist:
            logger.error(f"Notice not found: {self.kwargs.get('slug')}")
            raise Http404("Notice not found.")

class ProgramListView(ListView):
    model = Program
    template_name = 'programs.html'
    context_object_name = 'programs'
    paginate_by = 10  # Added pagination

    def get_queryset(self):
        try:
            queryset = super().get_queryset().select_related('department')
            level_filter = self.request.GET.get('level', '').strip()
            department_filter = self.request.GET.get('department', '').strip()

            if level_filter:
                if level_filter not in dict(Program.LEVEL_CHOICES):
                    messages.warning(self.request, "Invalid program level selected.")
                    raise ValueError("Invalid level.")
                queryset = queryset.filter(level=level_filter)

            if department_filter:
                queryset = queryset.filter(department__name__icontains=department_filter)

            return queryset.order_by('name')
        except ValueError as e:
            logger.warning(f"Invalid query parameters in ProgramListView: {e}")
            return Program.objects.none()
        except Exception as e:
            logger.error(f"Error in ProgramListView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load programs. Please try again later.")
            return Program.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['levels'] = Program.LEVEL_CHOICES
            context['departments'] = Department.objects.all()
            context['get_params'] = self.request.GET.urlencode()
        except Exception as e:
            logger.error(f"Error in ProgramListView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load program filters. Please try again later.")
            context['levels'] = []
            context['departments'] = []
        return context

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'program_detail.html'
    context_object_name = 'program'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ObjectDoesNotExist:
            logger.error(f"Program not found: {self.kwargs.get('slug')}")
            raise Http404("Program not found.")

class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    paginate_by = 3

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            category = self.request.GET.get('category', '').strip()
            if category:
                if category not in dict(Gallery.CATEGORY_CHOICES):
                    messages.warning(self.request, "Invalid event category selected.")
                    raise ValueError("Invalid category.")
                queryset = queryset.filter(category=category)
            return queryset.order_by('-date')
        except ValueError as e:
            logger.warning(f"Invalid query parameters in EventListView: {e}")
            return Event.objects.none()
        except Exception as e:
            logger.error(f"Error in EventListView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load events. Please try again later.")
            return Event.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            featured_event = Event.objects.filter(is_featured=True).order_by('-date').first()
            context['featured_event'] = featured_event
            context['events'] = self.object_list  # Use paginated queryset
            context['categories'] = Gallery.CATEGORY_CHOICES  # Assuming events use gallery categories
            context['get_params'] = self.request.GET.urlencode()
        except Exception as e:
            logger.error(f"Error in EventListView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load event data. Please try again later.")
            context['featured_event'] = None
            context['events'] = Event.objects.none()
            context['categories'] = []
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ObjectDoesNotExist:
            logger.error(f"Event not found: {self.kwargs.get('slug')}")
            raise Http404("Event not found.")

class GalleryView(ListView):
    model = Gallery
    template_name = 'gallery.html'
    context_object_name = 'images'
    paginate_by = 12

    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            category = self.request.GET.get('category', '').strip()
            if category:
                if category not in dict(Gallery.CATEGORY_CHOICES):
                    messages.warning(self.request, "Invalid gallery category selected.")
                    raise ValueError("Invalid category.")
                queryset = queryset.filter(category=category)
            return queryset.order_by('-upload_date')
        except ValueError as e:
            logger.warning(f"Invalid query parameters in GalleryView: {e}")
            return Gallery.objects.none()
        except Exception as e:
            logger.error(f"Error in GalleryView get_queryset: {e}", exc_info=True)
            messages.error(self.request, "Unable to load gallery. Please try again later.")
            return Gallery.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['categories'] = Gallery.CATEGORY_CHOICES
            context['get_params'] = self.request.GET.urlencode()
        except Exception as e:
            logger.error(f"Error in GalleryView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load gallery filters. Please try again later.")
            context['categories'] = []
        return context

class CalenderView(TemplateView):
    template_name = 'calender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['events'] = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:10]
        except Exception as e:
            logger.error(f"Error in CalenderView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load calendar events. Please try again later.")
            context['events'] = []
        return context

class AlumniView(TemplateView):
    template_name = 'alumni.html'

class ResultView(TemplateView):
    template_name = 'result.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['faqs'] = Faq.objects.filter(page='contact')
        except Exception as e:
            logger.error(f"Error in ContactView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load FAQs. Please try again later.")
            context['faqs'] = []
        return context

class CampusView(TemplateView):
    template_name = 'campus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['campus_images'] = Gallery.objects.filter(category='campus').order_by('-upload_date')[:4]
        except Exception as e:
            logger.error(f"Error in CampusView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load campus images. Please try again later.")
            context['campus_images'] = []
        return context

class AdmissionView(TemplateView):
    template_name = 'admission.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['faqs'] = Faq.objects.filter(page='admission')
            context['notices'] = Notice.objects.filter(category='admission').order_by('-publish_date')[:5]
        except Exception as e:
            logger.error(f"Error in AdmissionView get_context_data: {e}", exc_info=True)
            messages.error(self.request, "Unable to load admission data. Please try again later.")
            context['faqs'] = []
            context['notices'] = []
        return context