from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # About URLs
    path('about/history/', views.HistoryView.as_view(), name='history'),
    
    # Faculty URLs
    path('about/faculty/', views.FacultyListView.as_view(), name='faculty'),
    path('faculty/<slug:slug>/', views.FacultyDetailView.as_view(), name='faculty_detail'),
    
    # Department URLs
    path('about/departments/', views.DepartmentListView.as_view(), name='departments'),
    path('department/<slug:slug>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    
    # Notice URLs
    path('notices/', views.NoticeListView.as_view(), name='notices'),
    path('notices/<slug:slug>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    
    # Program URLs
    path('programs/', views.ProgramListView.as_view(), name='programs'),
    path('programs/<slug:slug>/', views.ProgramDetailView.as_view(), name='program_detail'),
    
    # Event URLs
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),

    path("campus/", views.CampusView.as_view(), name="campus"),
    
    # Gallery URL
    path('gallery/', views.GalleryView.as_view(), name='gallery'),

    # Alumni URL
    path('alumni/', views.AlumniView.as_view(), name='alumni'),

    # Result URL
    path('result/', views.ResultView.as_view(), name='result'),

    # calendars URL
    path("calender/", views.CalenderView.as_view(), name="calender"),
    
    # Admission URL
    path('admission/', views.AdmissionView.as_view(), name='admission'),
    path('admission#admission-programs', views.AdmissionView.as_view(), name="programs"),
    
    # Contact URL
    path('contact/', views.ContactView.as_view(), name='contact'),
    
] 