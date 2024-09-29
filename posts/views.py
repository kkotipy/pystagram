from django.shortcuts import render, redirect


def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    return render(request, "posts/feeds.html")
