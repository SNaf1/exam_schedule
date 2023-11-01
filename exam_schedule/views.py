from django.shortcuts import render, redirect
from django.utils import timezone
import datetime
from .models import ExamSchedule
from django.http import HttpResponseRedirect

from django.contrib import messages  # Import the messages framework

def home(request):
    if request.method == 'GET':
        request.session['search_results'] = []

    search_results = request.session.get('search_results', [])

    if request.method == 'POST':
        if 'course' in request.POST:  # Check if 'course' is in the POST data
            course = request.POST.get('course').upper()
            section = request.POST.get('section')
    
            # Check if the course is already in the search results
            if any(result['course'] == course for result in search_results):
                messages.warning(request, f"Course '{course}' is already in the list.")
            else:
                exam_schedule = ExamSchedule.objects.filter(course=course, section=section).first()
    
                if exam_schedule:
                    search_results.append({
                        'course': exam_schedule.course,
                        'section': exam_schedule.section,
                        'mid_date': exam_schedule.mid_date.strftime('%d-%b-%Y'),
                        'start_time': exam_schedule.start_time.strftime('%I:%M %p'),
                        'end_time': exam_schedule.end_time.strftime('%I:%M %p'),
                        'room': exam_schedule.room,
                    })
                    request.session['search_results'] = search_results
                else:
                    messages.warning(request, f"Course '{course}' with section '{section}' was not found.")
        elif 'course_to_remove' in request.POST:  # Check if 'course_to_remove' is in the POST data
            course_to_remove = request.POST.get('course_to_remove')
            search_results = [result for result in search_results if result['course'] != course_to_remove]
            request.session['search_results'] = search_results

    # Sort all search results by date and time
    search_results.sort(key=lambda x: (x['mid_date'], x['start_time']))

    context = {
        'search_results': search_results,
    }
    return render(request, 'home.html', context)

