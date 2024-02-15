
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [

  path('', views.index, name='index'),
  path('colleges/', views.college_list, name='college_list'),
  path('college_details/<int:college_id>/<int:selected_course_id>/',views.college_details,name='college_details'),
  path('college_detail/<int:college_id>/',views.college_detail,name='college_detail'),
  path('contact/<int:college_id>/<int:college_course_details_id>/',views.contact, name='contact'),
  path('submit_enquiry/', views.submit_enquiry, name='submit_enquiry'),
  path('thank_you_page/', views.thank_you_page, name='thank_you_page'),
  path('error_page/', views.error_page, name='error_page'),
  path('about/',views.about, name='about'),
  path('address/',views.address,name='address'),


  path('get_suggestions/', views.get_suggestions, name='get_suggestions'),



  path('stream_list/<int:stream_id>/', views.stream_list, name='stream_list'),
  path('course_list/<int:course_id>/', views.course_list, name='course_list'),
  path('location_college_list/<int:location_id>/', views.location_college_list, name='location_college_list'),


]
  


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)