from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def post_index(request):
    post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        #filter sorgulama yaparak liste döndürür
        # icontains aldığı parametreye göre küçük büyük duyarlılığı olmadan arama yapar
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 3) # Show 25 contacts per page

    page = request.GET.get('sayfa')
    post_list = paginator.get_page(page)
    
    return render(request, 'post/index.html', {'posts': post_list})
    #return HttpResponse('Burası Post index sayfası')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False) # commit=False
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)

def post_create(request):    
    
    #if request.method == "POST":
    #    print(request.POST)

    #title = request.POST.get('title')
    #content = request.POST.get('content')
    #Post.objects.create(title=title, content=content)

    """if request.method == "POST":
        # Formdan gelen bilgileri kaydet
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        # Formu kullanıcıya göster
        form = PostForm()"""   
        
    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()   

    # Formdan gelen bilgileri kaydet
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False) # commit=False
        post.user = request.user
        post.save()
        #post.slug = slugify(post.title.replace('ı','i'))
        #post.save()
        messages.success(request, 'Başarılı bir şekilde oluşturuldu')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)

def post_update(request, slug):

    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()  

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
            form.save()
            messages.success(request, 'Başarılı bir şekilde güncellendi', extra_tags='mesaj-basarili')
            return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_delete(request, slug):

    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()  
        
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')