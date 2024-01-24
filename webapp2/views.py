from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import properties
from .python_script import keyword_search
from django.contrib.auth import login , authenticate , logout
from collections import Counter
from .forms import CustomUserCreationForm, ProfileForm, PropertyForm

def index(request):
    return render(request , "index.html")


def ranked(request):
    return render(request , "property_details.html")

def Login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, " username does not exists ! ")

        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            messages.success(request, " You are Successfully log in ! ")
            return redirect("home")
        else:
            messages.error(request , "Username or Password is incorrect ! Please try again ")        
    return render(request , 'login_register.html')

def Logout(request):
    logout(request)
    messages.success(request, " You are Successfully log out ! ")
    return redirect('login')

def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # this could save the user but make temporary instance of user
            user.username = user.username.lower()
            user.save()    
            messages.success(request , "User successfully registered!")
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , "An Error Occurred Please Try Again")
    page = 'register'
    context ={
        'page':page,
        'form':form
    }
    return render(request, "login_register.html" , context)

# from django.shortcuts import render
from .models import Review
# from .python_script import keyword_search

from django.shortcuts import render
from django.http import HttpResponse
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from textblob import TextBlob
from .models import Review, properties
from Reviews.models import NewReview  # Make sure to import your models
from django.utils import timezone
from Reviews.models import Profile

def calculate_keyword_weights(review):
    words = word_tokenize(review.text)
    words = [word for word in words if word not in stopwords.words('english')]
    word_freq = Counter(words)
    word_weights = {word: freq / len(words) for word, freq in word_freq.items()}
    return word_weights

def extract_features(review):
    words = word_tokenize(review.text)
    tagged_words = pos_tag(words)
    adjectives = [word for word, pos in tagged_words if pos == 'JJ']
    key_phrases = [' '.join([adjectives[i], adjectives[i + 1]]) for i in range(len(adjectives) - 1)]
    return adjectives, key_phrases

def calculate_tonality(review):
    blob = TextBlob(review.text)
    return blob.sentiment.polarity


def calculate_reasonableness(keyword_weights):
    return sum(keyword_weights.values())

def calculate_comprehensiveness(keyword_weights):
    return len(set(keyword_weights.keys()))

def calculate_relevancy(keyword_weights):
    return sum(keyword_weights.values())


def update_review_model(review):
    keyword_weights = calculate_keyword_weights(review)
    adjectives, key_phrases = extract_features(review)

    review.length = len(review.text)
    review.reasonableness = calculate_reasonableness(keyword_weights)
    review.comprehensiveness = calculate_comprehensiveness(keyword_weights)
    review.relevancy = calculate_relevancy(keyword_weights)
    review.tonality = calculate_tonality(review)

    review.save()


@login_required(login_url='login')
def userUpdate(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print("Form data submitted successfully!")
            messages.success(request, "Profile Updated successfully!")
            return redirect('profile')
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        print("Request method is not POST.")

    context = {
        'form': form,
    }
    return render(request, 'account_update.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = PropertyForm()

    if request.method=='POST':
        form = PropertyForm(request.POST , request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            messages.success(request , "New Project Created successfully!")
            return redirect('account')

    context = {
        'form':form,
        'title':"Create Project",
    }
    return render(request, 'create_property.html', context)


def single_profile(request):
    profile = Profile.objects.get(user=request.user)

    data = {
        'profile':profile
    }

    return render(request, 'user-profile.html', data)


# @login_required(login_url='login')
def review_view(request, property_id):
    try:
        property = properties.objects.get(pk=property_id)
    except properties.DoesNotExist:
        # Handle the case when the property does not exist
        return HttpResponse("Property not found.", status=404)

    keywords = [
        'Impressive','Exceptional','Nice','Efficient', 'Brilliant', 'Excellent', 'Repairs', 'maintenance',
        'Fantastic', 'Great', 'Awesome', 'positive', 'building','Bad',
        'Furnished', 'Fair', 'satisfied', 'quick', 'pleasent',
        'decent', 'Convinient', 'double', 'apartment', 'disturbance'
    ]

    # Process form submission
    if request.method == 'POST':
        text = request.POST.get('review')
        author = request.user.username  # Assuming the user is authenticated
        date = timezone.now()

        # Create a NewReview object and save it to the database
        new_review = NewReview(
            text=text,
            author=author,
            date=date,
            property=property.desc,
            address=property.desc,
            length=len(text),
            reasonableness=0,  # Set to your default value
            comprehensiveness=0,  # Set to your default value
            relevancy=0,  # Set to your default value
            tonality=0.0  # Set to your default value
        )
        new_review.save()

    # Continue with the existing code to fetch and filter reviews
    reviews = NewReview.objects.filter(address=property.desc).order_by('-date')
    total_reviews = NewReview.objects.filter(address=property.desc).count()

    filtered_reviews = []
    for review in reviews:
        keyword_weights = calculate_keyword_weights(review)
        adjectives, key_phrases = extract_features(review)

        review.length = len(review.text)
        review.reasonableness = calculate_reasonableness(keyword_weights)
        review.comprehensiveness = calculate_comprehensiveness(keyword_weights)
        review.relevancy = calculate_relevancy(keyword_weights)
        review.tonality = calculate_tonality(review)
        review.save()

        if any(keyword in keyword_weights for keyword in keywords):
            filtered_reviews.append(review)

    address = property.desc

    data = {
        'id': property,
        'total_count':total_reviews,
        'total_reviews': total_reviews // 2,
        'validated_reviews': len(filtered_reviews),
        'percentage':int((len(filtered_reviews)/total_reviews)*100),
        'top_reviews': filtered_reviews[:5],
        'address': address,
    }
    return render(request, 'property_details.html', data)

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
