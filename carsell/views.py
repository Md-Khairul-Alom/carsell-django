from django.shortcuts import render, get_object_or_404, redirect
from pages.models import Team
from cars.models import Car
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def home(request):
    teams=Team.objects.all()
    featured_cars=Car.objects.filter(is_featured=True).order_by('created_date')
    all_cars=Car.objects.order_by('created_date')
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()

    context={
        'teams':teams,
        'featured_cars':featured_cars,
        'all_cars':all_cars,
        'model_search':model_search,
        'city_search':city_search,
        'year_search':year_search,
        'body_style_search': body_style_search,

    }
    return render(request, 'pages/home.html', context)


def about(request):
    teams=Team.objects.all()
    context={
        'teams':teams,
    }
    return render(request, 'pages/about.html', context)

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        phone=request.POST['phone']
        message=request.POST['message']

        email_subject = 'You have a new mail from Carzone Website regarding' + subject
        message_body= 'Name: ' + name + '. Email: ' + email + '. Phone: ' + phone + '. Message: ' + message
        admin_info = User.objects.get(is_superuser=True)
        admin_email=admin_info.email

        send_mail(
            email_subject,
            message_body,
            'khairul9215@gmail.com',
            [admin_email],
            fail_silently=False,
        )
        messages.success(request, 'We will get back to you shortly')
        return redirect('contact')
    return render(request, 'pages/contact.html')

def cars(request):
    cars=Car.objects.order_by('created_date')
    paginator=Paginator(cars, 3)
    page=request.GET.get('page')
    paged_cars=paginator.get_page(page)

    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()

    context={
    'cars':paged_cars,
    'model_search':model_search,
    'city_search':city_search,
    'year_search':year_search,
    'body_style_search': body_style_search,
    }
    return render(request, 'pages/cars.html', context)

def car_detail(request, id):
    single_car=get_object_or_404(Car, pk=id)
    context={
    'single_car':single_car,
    }
    return render(request, 'pages/car_detail.html', context)

def search(request):
    cars=Car.objects.order_by('created_date')
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search=Car.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars=cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars=cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            cars=cars.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars=cars.filter(year__iexact=year)

    if 'min_price' in request.GET:
        min_price=request.GET['min_price']
        max_price=request.GET['max_price']

        if max_price:
            cars=cars.filter(price__gte=min_price, price__lte=max_price)

    context={
    'cars':cars,
    'model_search':model_search,
    'city_search':city_search,
    'year_search':year_search,
    'body_style_search': body_style_search,
    'transmission_search': transmission_search,
    }
    return render(request, 'pages/search.html', context)
