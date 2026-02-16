from django.shortcuts import render


def home_view(request):
    return render(request, "home/index.html",
                  {"title": "home", "data": "Welcome to the home page"})


def about_view(request):
    return render(request, "home/index.html",
                  {"title": "about", "data": "About page"})


def contact_view(request):
    return render(request, "home/index.html",
                  {"title": "contact", "data": "Contact us"})


def post_view(request, post_id):
    return render(request, "home/index.html",
                  {"title": f"post {post_id}", "data": f"You are viewing the post with ID: {post_id}"})


def profile_view(request, username):
    return render(request, "home/index.html",
                  {"title": username, "data": f"You are viewing the user profile: {username}"})


def event_view(request, year, month, day):
    return render(request, "home/index.html",
                  {"title": f"{year}/{month}/{day}", "data": f"Event date: {year}-{month}-{day}"})
