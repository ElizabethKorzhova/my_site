from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Welcome to the home page")


def about_view(request):
    return HttpResponse("About page")


def contact_view(request):
    return HttpResponse("Contact us")


def post_view(request, post_id):
    return HttpResponse(f"You are viewing the post with ID: {post_id}")


def profile_view(request, username):
    return HttpResponse(f"You are viewing the user profile: {username}")


def event_view(request, year, month, day):
    return HttpResponse(f"Event date: {year}-{month}-{day}")
