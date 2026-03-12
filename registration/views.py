from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hospital, Registration
from .forms import RegistrationForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.utils import timezone
import csv

def landing(request):
    total = Registration.objects.count()
    return render(request,"landing.html",{"total":total})

def dashboard(request):

    total = Registration.objects.count()

    return render(request, "dashboard.html", {"total": total})

def login_page(request):

    return render(request, "login.html")

@login_required
def register(request):

    email = request.session.get("user_email")

    if not email and request.user.is_authenticated:
        email = request.user.email

    # check if already registered
    if Registration.objects.filter(email=email).exists():
        return render(request, "already_registered.html")
    
    districts = Hospital.objects.values_list("district", flat=True).distinct()

    hospital = find_hospital_by_email(email)

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            reg = form.save(commit=False)

            reg.email = email
            if hospital:
                reg.hospital = hospital
            else:
                hospital_id = request.POST.get("hospital")
                reg.hospital = Hospital.objects.get(id=hospital_id)

            reg.save()

            return render(request, "success.html", {
                "name": reg.name,
                "hospital": reg.hospital.hospital_name,
                "time": reg.created_at
            })

    else:
        form = RegistrationForm()

    context = {
        "form": form,
        "hospital": hospital,
        "email": email,
        "districts": districts
    }

    return render(request, "register.html", context)

def get_hospitals_by_district(request):

    district = request.GET.get("district")

    hospitals = Hospital.objects.filter(district=district)

    data = []

    for h in hospitals:
        data.append({
            "id": h.id,
            "name": h.hospital_name,
            "hospital_id": h.hospital_id
        })

    return JsonResponse(data, safe=False)

def find_hospital_by_email(user_email):

    user_email = user_email.lower().strip()

    for h in Hospital.objects.all():

        emails = [e.strip().lower() for e in h.email.split(",")]

        if user_email in emails:
            return h

    return None

def email_login(request):

    if request.method == "POST":

        email = request.POST.get("email")

        request.session["user_email"] = email

        return redirect("/register/")

    return redirect("/login/")

def stats(request):

    total = Registration.objects.count()

    district_stats = Registration.objects.values(
        "hospital__district"
    ).annotate(count=Count("id"))

    hospital_stats = Registration.objects.values(
        "hospital__hospital_name"
    ).annotate(count=Count("id")).order_by("-count")[:10]

    context = {

        "total":total,
        "district_stats":district_stats,
        "hospital_stats":hospital_stats
    }

    return render(request,"stats.html",context)


def export_all_registrations(request):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Email",
        "Name",
        "Designation",
        "Mobile",
        "Hospital",
        "District",
        "Registration Time"
    ])

    registrations = Registration.objects.select_related("hospital").all()

    for r in registrations:

        writer.writerow([
            r.email,
            r.name,
            r.designation,
            r.mobile,
            r.hospital.hospital_name if r.hospital else "",
            r.hospital.district if r.hospital else "",
            r.created_at
        ])

    return response

def live_registrations(request):

    registrations = Registration.objects.select_related("hospital").order_by("-created_at")[:50]

    data = []

    # Convert times to Indian Standard Time (UTC+5:30)
    ist = timezone.get_fixed_timezone(330)

    for r in registrations:

        data.append({
            "name": r.name,
            "email": r.email,
            "hospital": r.hospital.hospital_name if r.hospital else "",
            "hospital_id": r.hospital.hospital_id if r.hospital else "",
            "district": r.hospital.district if r.hospital else "",
            "time": timezone.localtime(r.created_at, ist).strftime("%H:%M:%S")
        })

    return JsonResponse(data, safe=False)

def monitor(request):

    total = Registration.objects.count()

    return render(request, "monitor.html", {"total": total})
