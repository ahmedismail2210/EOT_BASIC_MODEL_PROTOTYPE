from django.shortcuts import render
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import properties
from .python_script import keyword_search
from collections import Counter

def index(request):
    return render(request , "index.html")


def ranked(request):
    return render(request , "property_page.html")



# from django.shortcuts import render
from .models import Review
# from .python_script import keyword_search

def review_view(request, property_id ):
    try:
        property = properties.objects.get(pk=property_id)
    except properties.DoesNotExist:
        # Handle the case when the property does not exist
        return HttpResponse("Property not found.", status=404)

    keywords = [
        'Impressive', 'Efficient', 'Brilliant', 'Excellent', 'Repairs', 'maintenance',
        'Fantastic', 'Great', 'Awesome', 'positive', 'building',
        'Furnished', 'Fair', 'satisfied', 'quick', 'pleasent',
        'decent', 'Convinient' , 'double' , 'apartment' , 'disturbance' 
    ]

    reviews = Review.objects.filter(address=property.desc)
    total_reviews = Review.objects.all().count()
        
        
        
    filtered_reviews = []
    for review in reviews:
        text = review.text
        count = Counter(text.split())
        if any(keyword in count for keyword in keywords):
            filtered_reviews.append(review)    
        
        
        # Assuming 'address' is a field in the 'properties' model, retrieve the address
    address = properties.desc


    return render(request, 'property_page.html', {
        
        'id':property,
        'total_reviews': total_reviews // 2 ,
        'validated_reviews': len(filtered_reviews),
        'top_reviews': filtered_reviews,
        'address': address,
    })


def dashboard(request):
    return render(request , "dash.html")

def contact(request):
    return render(request , "contact.html")


def projects(request):
    proj = properties.objects.all()
    data = {
        'proj':proj,
    }
    return render(request , "projects.html" , data)


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Assuming the CSV file has headers: "title", "review", and "rating"
        
        csv_text = csv_file.read().decode('utf-8')
        csv_reader = csv.DictReader(csv_text.splitlines())
        
        for row in csv_reader:
            property.objects.create(
                text=row['text'],
                author=row['author'],
                date=row['date'],
                property=row['property'],
                address=row['address']
            )
        
    return render(request, 'upload_csv.html')


def read_reviews_from_csv():
    reviews = []
    with open('/reviews.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reviews.append(row)
    return reviews
