from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from posts.forms import CommentForm, PostForm
from posts.models import Post, Comment, PostImage


def feeds(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

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

        # redirect() 함수가 아닌 HttpResponseRedirect는 URL pattern name을 사용할 수 없다
        # 이 경우, reverse()로 URL을 만든 후, 뒤에 추가로 붙일 주소를 직접 입력해야 한다
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)


@require_POST
def comment_delete(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            url = reverse("posts:feeds") + f"#post-{comment.post.id}"
            return HttpResponseRedirect(url)
        else:
            return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")


def post_add(request):
    if request.method == "POST":
        # request.POST로 온 데이터 ("content")는 PostForm으로 처리
        form = PostForm(request.POST)

        if form.is_valid():
            # Post의 "user" 값은 request에서 가져와 자동 할당한다
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Post를 생성한 후
            # request.FILES.getlist("images")로 전송된 이미지들을 순회하며 PostImage 객체를 생성한다
            for image_file in request.FILES.getlist("images"):
                # request.FILES 또는 request.FILES.getlist()로 가져온 파일은
                # Model의 ImageField 부분에 곧바로 할당한다
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            # 모든 PostImage와 Post의 생성이 완료되면
            # 피드 페이지로 이동하여 생성된 Post의 위치로 스크롤되도록 한다
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)

    # GET 요청일 때는 빈 form을 보요주도록 한다
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "posts/post_add.html", context)
