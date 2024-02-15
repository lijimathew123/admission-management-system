from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Stream, Course, Location,College,CollegeCourse,Enquiry,CourseType
from django.http import JsonResponse

from django.contrib.staticfiles import finders
import json
from django.db.models import Min, Max





def index(request):
    streams = Stream.objects.all()
    course_types = CourseType.objects.all()
    courses = Course.objects.all()
    locations = Location.objects.all()

    # get current domain
    current_domain = request.get_host()
    print(current_domain)

    try:
        domain_location = Location.objects.get(domain=current_domain)
        domain_location_name = domain_location.name
        remaining_locations = Location.objects.exclude(id=domain_location.id)
    except Location.DoesNotExist:
        # Handle the case where the domain doesn't match any location
        domain_location_name = None
        remaining_locations = Location.objects.all()

    # Get the first 4 featured colleges
    featured_colleges = College.objects.filter(is_featured=True)[:4]
    featured_courses = Course.objects.filter(is_featured=True)[:6]

    return render(request, 'index.html', {
        'streams': streams,
        'course_types': course_types,
        'courses': courses,
        'domain_location_name': domain_location_name,
        'remaining_locations': remaining_locations,
        'featured_colleges': featured_colleges,
        'featured_courses': featured_courses,
    })



# def index(request):
#     streams = Stream.objects.all()
#     course_types = CourseType.objects.all()
#     courses = Course.objects.all()
#     locations = Location.objects.all()

# # get current domain
#     current_domain = request.get_host()
#     print(current_domain)

   

#      try:
#         domain_location = Location.objects.get(domain=current_domain)
#         domain_location_name = domain_location.name
#         remaining_locations = Location.objects.exclude(id=domain_location.id)
#     except Location.DoesNotExist:
#         # Handle the case where the domain doesn't match any location
#         domain_location_name = None
#         remaining_locations = Location.objects.all()


# # Get the first 4 featured colleges
#     featured_colleges = College.objects.filter(is_featured=True)[:4]

#     featured_courses = Course.objects.filter(is_featured=True)[:6]

#     return render(request, 'index.html', {
#         'streams': streams,
#         'course_types': course_types,
#         'courses': courses,
#         'domain_location_name': domain_location_name,
#         'remaining_locations': remaining_locations,
#         'featured_colleges': featured_colleges,
#         'featured_courses': featured_courses,
#     })


def college_list(request):
    if request.method == 'GET':
        stream_id = request.GET.get('stream')
        course_type_id = request.GET.get('type')
        course_id = request.GET.get('course')
        location_id = request.GET.get('location')

        # Start with all colleges
        colleges = College.objects.all()

        # Retrieve the selected course type
        selected_course_type = get_object_or_404(CourseType, id=course_type_id) if course_type_id else None

        # Retrieve the selected stream
        selected_stream = get_object_or_404(Stream, id=stream_id) if stream_id else None

        # Retrieve the selected location
        selected_location = get_object_or_404(Location, id=location_id) if location_id else None

        # Filter colleges based on selected values
        if stream_id:
            colleges = colleges.filter(collegecourse__course__stream_id=stream_id)
        if course_type_id:
            colleges = colleges.filter(collegecourse__course__course_type_id=course_type_id)
        if course_id:
            colleges = colleges.filter(collegecourse__course_id=course_id)
            selected_course = get_object_or_404(Course, id=course_id)
        else:
            selected_course = None

        if location_id:
            colleges = colleges.filter(location_id=location_id)

        # Order colleges by course price in ascending order
        colleges = colleges.order_by('collegecourse__price')

        # Get distinct colleges
        colleges = colleges.distinct()

        # Retrieve price information for each college
        college_prices = []
        for college in colleges:
            if course_id:
                course_price = college.collegecourse_set.filter(course_id=course_id).first()
                if course_price:
                    college_prices.append({
                        'college': college,
                        'price': course_price.price,
                    })
            else:
                # If no course is selected, append basic information without price
                college_prices.append({
                    'college': college,
                    'price': None,
                })

        colleges_count = len(college_prices)

        # Check if no colleges are found
        if colleges_count == 0:
            message = "No colleges found based on the provided criteria."
            return render(request, 'college.html', {'message': message})

        return render(request, 'college.html', {
            'college_prices': college_prices,
            'colleges_count': colleges_count,
            'selected_course': selected_course,
            'selected_course_type': selected_course_type,
            'selected_stream': selected_stream,
            'selected_location': selected_location,
        })




def college_details(request, college_id, selected_course_id):
    college = get_object_or_404(College, id=college_id)
    selected_course = None
    college_course_details = None
    course_type = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        college_course_details = get_object_or_404(CollegeCourse, college=college, course=selected_course)
        course_type = selected_course.course_type

    context = {
        'college': college,
        'selected_course': selected_course,
        'college_course_details': college_course_details,
        'course_type': course_type,
        
    }
    return render(request, 'college_details.html', context)




def college_detail(request, college_id):
    college = get_object_or_404(College, id=college_id)
    college_courses = CollegeCourse.objects.filter(college=college)

    context = {
        'college': college,
        'college_courses': college_courses,
    }

    return render(request, 'college_description.html', context)





def contact(request, college_id, college_course_details_id):

   

    with open("static/countrycodes.json") as json_file:
            country_codes = json.load(json_file)


    college = get_object_or_404(College, id=college_id)
    college_course_details = get_object_or_404(CollegeCourse, id=college_course_details_id)

    context = {
        'college': college,
        'college_course_details': college_course_details,
        'country_codes': country_codes,
    }
    return render(request, 'contact.html', context)




def submit_enquiry(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id')
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country')

        college = get_object_or_404(College, id=college_id)
        course = get_object_or_404(Course, id=course_id)

        # Fetch the CollegeCourse details based on college and course
        college_course_details = get_object_or_404(CollegeCourse, college=college, course=course)

        # Create an Enquiry instance and save it to the database
        enquiry = Enquiry(
            course=course,
            college=college,
            location=college.location,
            price=college_course_details.price,
            name=name,
            email=email,
            country_code=country_code,
            phone=phone,
            status=1,  # Set default status to 'Pending'
            note='',  
        )
        enquiry.save()

        # Redirect to a thank you page or another appropriate page
        return redirect('thank_you_page')

    # Handle invalid request method (GET or other)
    return redirect('error_page')


def thank_you_page(request):
    return render(request, 'thank_you.html')


def error_page(request):
    return render(request, 'error.html')


def about(request):
    return render(request,'about.html')


def address(request):
    return render(request,'address.html')








def get_suggestions(request):
    query = request.GET.get('query', '')

    # Query the database for suggestions
    colleges = College.objects.filter(name__icontains=query)
    streams = Stream.objects.filter(name__icontains=query)
    courses = Course.objects.filter(name__icontains=query)
    locations = Location.objects.filter(name__icontains=query)

    suggestions = []

    # Add college suggestions
    for college in colleges:
        suggestions.append({
            'name': college.name,
            'type': 'College',
            'url': f'/college_detail/{college.id}',
        })

    # Add stream suggestions
    for stream in streams:
        suggestions.append({
            'name': stream.name,
            'type': 'Stream',
            'url': f'/stream_list/{stream.id}',
        })

    # Add course suggestions
    for course in courses:
        suggestions.append({
            'name': course.name,
            'type': 'Course',
            'url': f'/course_list/{course.id}',
        })

    # Add location suggestions
    for location in locations:
        suggestions.append({
            'name': location.name,
            'type': 'Location',
            'url': f'/location_college_list/{location.id}/',
        })



    print(suggestions)

    return JsonResponse(suggestions, safe=False)




def stream_list(request, stream_id):
    stream = get_object_or_404(Stream, pk=stream_id)
    colleges = College.objects.filter(collegecourse__course__stream=stream).distinct()

    # Fetch college courses related to the stream
    college_courses = CollegeCourse.objects.filter(course__stream=stream)

    context = {
        'colleges': colleges,
        'stream': stream,
        'college_courses': college_courses,
    }

    return render(request, 'stream_college.html', context)


def location_college_list(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    colleges = College.objects.filter(location=location)
    return render(request, 'location_college.html', {'location': location, 'colleges': colleges})



def course_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Assuming Course model has a foreign key relationship with Stream model
    stream_name = course.stream.name if course.stream else None

    colleges = College.objects.filter(collegecourse__course=course).distinct()

    

    context = {
        'course': course,
        'colleges': colleges,
        'stream_name': stream_name,
    }

    return render(request, 'course_college.html', context)


