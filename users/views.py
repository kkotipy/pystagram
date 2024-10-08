from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, SignupForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("posts:feeds")
            else:
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다")

        context = {"form": form}
        return render(request, "users/login.html", context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "users/login.html", context)


def logout_view(request):
    logout(request)

    return redirect("users:login")


def signup(request):
    # POST 요청 시, form이 유효하다면 최종적으로 redirect 처리된다
    if request.method == "POST":

        form = SignupForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("posts:feeds")

    # GET 요청 시, 빈 form을 생성한다
    else:
        form = SignupForm()

    # context로 전달되는 form은 두 가지 경우가 존재한다
    # 1. POST 요청에서 생성된 form이 유효하지 않은 경우 -> 에러를 포함한 form이 사용자에게 보여진다
    # 2. GET 요청으로 빈 form이 생성된 경우 -> 빈 form이 사용자에게 보여진다
    context = {"form": form}
    return render(request, "users/signup.html", context)
