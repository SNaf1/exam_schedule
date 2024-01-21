import os
import django
import pdfplumber
import datetime
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exam.settings")
django.setup()

from exam_schedule.models import ExamSchedule
pdf_path = r'H:\Uni work\Assignment\exam routine\exam\Final Schedule Fall 2023.pdf'

# To store data from all pages
all_extracted_data = []  

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            header = table[0] 
            data = table[1:]   

            if not all_extracted_data:  
                for row in data:
                    if len(row) == len(header):
                        data_dict = {header[i]: row[i] for i in range(len(header))}
                        all_extracted_data.append(data_dict)
            else:
                # Skipping the header row on subsequent pages
                data = data[1:]  
                for row in data:
                    if len(row) == len(header):
                        data_dict = {header[i]: row[i] for i in range(len(header))}
                        all_extracted_data.append(data_dict)



for data in all_extracted_data:
    data_dict = {
        'sl': data['SL.'].strip(),
        'course': data['Course'].strip(),
        'section': data['Section'].strip(),
        'mid_date': datetime.datetime.strptime(data['Final Date'], '%d-%b-%y').date(),
        'start_time': datetime.datetime.strptime(data['Start Time'], '%I:%M %p').time(),
        'end_time': datetime.datetime.strptime(data['End Time'], '%I:%M %p').time(),
        'room': data['Room.'].strip(),
        'mode': data['Mode'].strip(),
    }

    exam_schedule = ExamSchedule(**data_dict)
    exam_schedule.save()
