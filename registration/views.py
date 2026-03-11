from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Hospital, Registration
from .forms import RegistrationForm
from django.http import JsonResponse


@login_required
def register(request):

    email = request.user.email

    # check if already registered
    if Registration.objects.filter(email=email).exists():
        return render(request, "already_registered.html")
    
    districts = Hospital.objects.values_list("district", flat=True).distinct()

    hospital = Hospital.objects.filter(email=email).first()

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

            return render(request, "success.html")

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