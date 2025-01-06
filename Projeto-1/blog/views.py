from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment, Category, User
from .forms import PostForm, CommentForm, UserForm, PhoneForm, LoginForm

def home(request):
    posts = Post.objects.order_by('-created_at')
    categories = Category.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj, 'categories': categories})

def news(request):
    posts = Post.objects.order_by('-created_at')
    categories = Category.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj, 'categories': categories})

def new_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.name = request.user.name  # Pega o nome completo ou o username
            comment.user = request.user  # Associa o comentário ao usuário
            comment.save()
            messages.success(request, 'Comentário adicionado com sucesso.')
            return redirect('new_details', post_id=post_id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'new_details.html', {
        'post': post,
        'comment_form': comment_form,
        'comments': comments
    })
    
def new_details_by_category(request, category_id, post_id):
    category = get_object_or_404(Category, id=category_id)
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('new_details_by_category', category_id=category_id, post_id=post_id)
    else:
        comment_form = CommentForm()
    return render(request, 'new_details.html', {
        'category': category,
        'post': post,
        'comment_form': comment_form,
        'comments': comments
    })

@login_required
def add_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Remover dislike se existir
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    
    # Adicionar like apenas se ainda não existir
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    
    return redirect('new_details', post_id=post_id)

@login_required
def remove_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Remover like se existir
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    
    return redirect('new_details', post_id=post_id)

@login_required
def add_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Remover like se existir
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    
    # Adicionar dislike apenas se ainda não existir
    if request.user not in post.dislikes.all():
        post.dislikes.add(request.user)
    
    return redirect('new_details', post_id=post_id)

@login_required
def remove_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Remover dislike se existir
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    
    return redirect('new_details', post_id=post_id)


def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})   

def new_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'new_by_category.html', {
        'category': category,
        'posts': posts,
        'page_obj': page_obj,
    })

def faq(request):
    return render(request, 'FAQ.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        phone_form = PhoneForm(request.POST)
        if user_form.is_valid() and phone_form.is_valid():
            try:
                user = user_form.save()
                phone = phone_form.save(commit=False)
                phone.user = user
                phone.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error saving data: {str(e)}')
                return redirect('register')
    else:
        user_form = UserForm()
        phone_form = PhoneForm()
    return render(request, 'register.html', {'user_form': user_form, 'phone_form': phone_form})

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not email or not new_password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'password_reset.html')
            
        try:
            user = User.objects.get(email=email)
            if new_password == confirm_password:
                if len(new_password) >= 8:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('login')
                else:
                    messages.error(request, 'Password must be at least 8 characters long.')
            else:
                messages.error(request, 'Passwords do not match.')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            
    return render(request, 'password_reset.html')