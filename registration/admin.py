from django.contrib import admin
from .models import Hospital, Registration
import csv
from django.http import HttpResponse

def export_csv(modeladmin,request,queryset):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition']='attachment; filename=registrations.csv'

    writer = csv.writer(response)

    writer.writerow(['Email','Name','Designation','Mobile','Hospital','District'])

    for obj in queryset:

        writer.writerow([
            obj.email,
            obj.name,
            obj.designation,
            obj.mobile,
            obj.hospital.hospital_name,
            obj.hospital.district
        ])

    return response

export_csv.short_description="Export Selected"

class RegistrationAdmin(admin.ModelAdmin):

    list_display=("email","name","hospital","created_at")

    actions=[export_csv]

admin.site.register(Hospital)
admin.site.register(Registration)