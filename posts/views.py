from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from posts.forms import CommentForm
from posts.models import Post


def feeds(request):
    if not request.user.is_authenticated:
        return redirect("/users/login/")

    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, "posts/feeds.html", context)


@require_POST
def comment_add(request):
    # request.POST로 전달된 데이터를 사용해 CommentForm 인스턴스를 생성
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # commit=False 옵션으로 메모리상에 Comment 객체 생성
        comment = form.save(commit=False)

        # Comment 생성에 필요한 사용자 정보를 request에서 가져와 할당
        comment.user = request.user

        # DB에 Comment 객체 저장
        comment.save()

        print(comment.id)
        print(comment.content)
        print(comment.user)

        # 생성한 comment에서 연결된 post 정보를 가져와서 id값을 사용
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
