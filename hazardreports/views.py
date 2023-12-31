from django.shortcuts import render, redirect
from .forms import HazardReportForm
from .models import HazardReport, HazardCategory
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Count
from django.db.models.functions import TruncMonth
# Create your views here.

from geopy.geocoders import Nominatim

def get_address_from_lat_lon(latitude, longitude):
    geolocator = Nominatim(user_agent="reverse_geocoding_app")
    location = f"{latitude}, {longitude}"

    try:
        location_info = geolocator.reverse(location, exactly_one=True)
        address = location_info.address
        return address
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def get_location_from_ip(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = response.json()
        location = data.get('loc', '').split(',')
        print(data)
        print("\n\n\n\n")
        return {'latitude': location[0], 'longitude': location[1]}
    except Exception as e:
        print(f"Error fetching location from IP: {str(e)}")
        return {'latitude':12.80119581748144, 'longitude':80.22476235441839}
    
@login_required(login_url='login')
def add_report(request):
    if request.method == 'POST':
        form = HazardReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            ip = request.META.get('REMOTE_ADDR')
            location_data = get_location_from_ip(ip)
            report.latitude = location_data.get('latitude', None)
            report.longitude = location_data.get('longitude', None)
            print(location_data)
            add = get_address_from_lat_lon(location_data.get('latitude', None),location_data.get('longitude', None))
            report.pin_code = add.split(' ')[-2].replace(",", "")
            report.address=add
            report.save()
            return redirect('home')
    else:
        form = HazardReportForm()
    return render(request, 'form_template.html', {'form': form,"form_heading":"Hazrad Report","button_text":"Report"})

@login_required(login_url='login')
def user_reports(request):
    user=request.user
    try:
        if user.authority:
            reports = HazardReport.objects.filter().order_by("-id")
        else:
            reports = HazardReport.objects.filter(user=user).order_by("-id")
    except:
        reports = HazardReport.objects.filter(user=user).order_by("-id")
    return render(request, "hazards/report_view.html", {"reports":reports, 'heading':'All Reports', "empty_message":'No reports uploaded yet!'})

@login_required(login_url='login')
def location_reports(request):
    ip = request.META.get('REMOTE_ADDR')
    location_data = get_location_from_ip(ip)
    add = get_address_from_lat_lon(location_data.get('latitude', None),location_data.get('longitude', None))
    pin_code = add.split(' ')[-2].replace(",", "")
    reports = HazardReport.objects.filter(pin_code__icontains=pin_code).order_by("-id")
    return render(request, "hazards/report_view.html", {"reports":reports, 'heading':'User Reports', "empty_message":'No Hazards in your Area.'})

@login_required(login_url='login')
def update_status(request, report_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        report = HazardReport.objects.get(pk=report_id)
        report.status = new_status
        report.save()
        return redirect('home')
    else:
        return redirect('home')
    

def generate_pie_chart_data(request):
    # Retrieve all categories
    categories = HazardCategory.objects.all()

    # Count the number of reports for each category
    category_data = []
    category_labels = []
    for category in categories:
        report_count = HazardReport.objects.filter(category=category).count()
        category_data.append(report_count)
        category_labels.append(category.name)

    status_options = ['Pending', 'In Progress', 'Resolved', 'Closed']
    status_data = []
    status_labels = []
    for status in status_options:
        report_count = HazardReport.objects.filter(status=status).count()
        status_data.append(report_count)
        status_labels.append(status)

    monthly_report_counts = HazardReport.objects.annotate(
        month=TruncMonth('timestamp')
    ).values('month').annotate(report_count=Count('id')).order_by('month')

    monthly_report_labels = [entry['month'].strftime('%Y-%m') for entry in monthly_report_counts]
    monthly_report_data = [entry['report_count'] for entry in monthly_report_counts]

    return render(request, 'hazards/visualize_report.html', {'category_data': category_data, 'category_labels': category_labels,
                                                             'status_data':status_data, "status_labels":status_labels,
                                                             'monthly_report_labels':monthly_report_labels,
                                                             'monthly_report_data':monthly_report_data})