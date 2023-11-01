import os
import django
import pdfplumber
import datetime
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exam.settings")
django.setup()

from exam_schedule.models import ExamSchedule
pdf_path = r'H:\Uni work\Assignment\exam routine\exam\Mid Schedule Fall 2023.pdf'

all_extracted_data = []  # To store data from all pages

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            header = table[0]  # Assuming the first row contains column headers
            data = table[1:]   # Remaining rows contain the data

            if not all_extracted_data:  # If it's the first page, just append all the data
                for row in data:
                    if len(row) == len(header):
                        data_dict = {header[i]: row[i] for i in range(len(header))}
                        all_extracted_data.append(data_dict)
            else:
                data = data[1:]  # Skip the header row on subsequent pages
                for row in data:
                    if len(row) == len(header):
                        data_dict = {header[i]: row[i] for i in range(len(header))}
                        all_extracted_data.append(data_dict)



# Now you have a list of dictionaries containing the extracted data from all pages
# You can process and populate your Django database with this combined data
# for data in all_extracted_data:
#     print(data)  # This will print each row as a dictionary

for data in all_extracted_data:
    data_dict = {
        'sl': data['SL.'].strip(),        # Use lowercase field names
        'course': data['Course'].strip(),
        'section': data['Section'].strip(),
        'mid_date': datetime.datetime.strptime(data['Mid Date'], '%d-%b-%y').date(),
        'start_time': datetime.datetime.strptime(data['Start Time'], '%I:%M %p').time(),
        'end_time': datetime.datetime.strptime(data['End Time'], '%I:%M %p').time(),
        'room': data['Room.'].strip()
    }

    exam_schedule = ExamSchedule(**data_dict)
    exam_schedule.save()
