from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post


def index(request, tag_slug=None):

    object_list = Post.published.all()
    tag = None


# ЗАСУНУТЬ В МИКСИН
    search_form = SearchForm()
    tags = Tag.objects.all()
    if 'query' in request.GET:
        # form = SearchForm(request.GET)
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.object.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                    'tags': tags, 'search_form':search_form})
# СТОП

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'page':page, 'posts':posts, 'tag':tag,
                                                   'tags' : tags, 'search_form':search_form})

# class index(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 2
#     template_name = 'blog/post_list.html'


def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug, status=True)
    comments = post.comments.filter(active=True)
    new_comment = None
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]



    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


# ЗАСУНУТЬ В МИКСИН
    search_form = SearchForm()
    tags = Tag.objects.all()
    if 'query' in request.GET:
        form = SearchForm()
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.object.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                    'tags': tags, 'search_form':search_form})
# СТОП

    return render(request, 'blog/detail.html', {'post':post, 'comments':comments, 'new_comment':new_comment,
                                                'comment_form':comment_form,
                                                'similar_posts':similar_posts,
                                                'search_form':search_form})

# def post_share(request, post_id):
#     post = get_object_or_404(Post, id=post_id, status=True)
#     sent = False
#     form = EmailPostForm()
#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             # отправка почты
#             # post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = 'Моя рекомендация'
#             message = f'Прочитай вот это - '
#             send_mail(subject, message, 'inventor959@gmail.com', [cd['to']])
#             sent = True
#         else:
#             form = EmailPostForm()
#             return render(request, 'blog/share.html', {'post' : post, 'form':form, 'sent':sent})
#     else:
#         return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent
#                                                    })

def about(request):

# ЗАСУНУТЬ В МИКСИН
    tags = Tag.objects.all()
    search_form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm()
        query = None
        results = []
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.object.annotate(
                search=SearchVector('title', 'body')).filter(search=query)
            return render(request, 'blog/search.html', {'form': search_form, 'query': query, 'results': results,
                                                    'tags': tags, 'search_form':search_form})
# СТОП

    return render(request, 'blog/about.html', {'search_form':search_form})



def post_search(request, query=None):

    form = SearchForm()
    query = None
    results = []
    tags = Tag.objects.all()
    search_form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Post.object.annotate(
            search=SearchVector('title', 'body')).filter(search=query)



    return render(request, 'blog/search.html', {'form':form, 'query':query, 'results':results,
                                                'tags' : tags, 'search_form':search_form})
