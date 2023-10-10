from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.db.models import Q
from .models import Post
from .forms import CommentForm, TipForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-posted_on")
    template_name = 'index.html'
    paginate_by = 6


class ViewRecipe(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('posted_on')
        tips = post.tips.order_by('posted_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "view_recipe.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,  # change to false if have approval
                "tips": tips,
                "tipped": True,
                "liked": liked,
                "comment_form": CommentForm(),
                "tip_form": TipForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('posted_on')
        tips = post.tips.order_by('posted_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        tip_form = TipForm(data=request.POST)
        if tip_form.is_valid():
            tip_form.instance.email = request.user.email
            tip_form.instance.name = request.user.username
            tip = tip_form.save(commit=False)
            tip.post = post
            tip.save()
        else:
            tip_form = TipForm()

        return render(
            request,
            "view_recipe.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "tips": tips,
                "tipped": True,
                "liked": liked,
                "comment_form": CommentForm(),
                "tip_form": TipForm()
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('view_recipe', args=[slug]))


def contact_page(request):
    return render(request, 'contact_form.html')


def add_recipe(request):
    return HttpResponseRedirect(reverse('add_recipe'))


class SearchRecipes(generic.ListView):
    model = Post
    template_name = 'search_recipes.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        post_list = Post.objects.filter(
            Q(recipe_name__icontains=query) | Q(ingredients__icontains=query)
        )
        return post_list
