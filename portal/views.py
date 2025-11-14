# portal/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from accounts.models import AlumniUser
from django.utils import timezone
from .forms import PostForm
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required # <-- MODERATION IMPORT

@login_required
def dashboard_view(request):
    # This is the dashboard, it only DISPLAYS posts
    all_posts = Post.objects.filter(is_approved=True) # <-- MODERATION FILTER
    upcoming_meetups = Post.objects.filter(
        is_approved=True, # <-- MODERATION FILTER
        post_type='Meetup', 
        meetup_time__gte=timezone.now()
    ).order_by('meetup_time')
    
    open_roles = Post.objects.filter(is_approved=True, post_type='Hiring') # <-- MODERATION FILTER
    
    stats = {
        'total_alumni': AlumniUser.objects.count(),
        'open_roles': open_roles.count(),
        'upcoming_meetups': upcoming_meetups.count(),
    }

    context = {
        'user': request.user,
        'posts': all_posts,
        'stats': stats,
        'upcoming_meetups': upcoming_meetups,
        'jobs_announcements': open_roles,
    }
    return render(request, 'portal/dashboard.html', context)

# --- THIS IS THE VIEW FOR THE "+ NEW POST" BUTTON ---
@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # --- !! ADDED MODERATION LOGIC !! ---
            if request.user.is_staff:
                post.is_approved = True  # Auto-approve posts from staff
            else:
                post.is_approved = False # Posts from others need approval
            
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
        
    context = {
        'form': form
    }
    return render(request, 'portal/create_post.html', context)

# --- THESE ARE YOUR SIDEBAR PAGE VIEWS ---
@login_required
def hiring_posts_view(request):
    # Get all posts that are 'Hiring'
    hiring_posts = Post.objects.filter(is_approved=True, post_type='Hiring').order_by('-created_at') # <-- MODERATION FILTER
    
    context = {
        'posts': hiring_posts,
    }
    return render(request, 'portal/hiring.html', context)

@login_required
def meetup_posts_view(request):
    # Get all posts that are 'Meetup'
    meetup_posts = Post.objects.filter(is_approved=True, post_type='Meetup').order_by('-created_at') # <-- MODERATION FILTER
    
    context = {
        'posts': meetup_posts,
    }
    return render(request, 'portal/meetups.html', context)

@login_required
def alumni_list_view(request):
    # We filter this to ONLY show 'Alumni'
    all_alumni = AlumniUser.objects.filter(user_type='Alumni').order_by('-batch_year', 'full_name')
    
    context = {
        'alumni': all_alumni,
    }
    return render(request, 'portal/alumni_list.html', context)

@login_required
def student_list_view(request):
    # This is just like the alumni list, but filtered for 'Student'
    all_students = AlumniUser.objects.filter(user_type='Student').order_by('batch_year', 'full_name')
    
    context = {
        'students': all_students,
    }
    return render(request, 'portal/student_list.html', context)

# --- !! THIS IS THE VIEW FOR THE SEARCH BAR !! ---
@login_required
def search_results_view(request):
    query = request.GET.get('q', '') 
    
    if query:
        # Search for posts where the content CONTAINS the query
        post_results = Post.objects.filter(is_approved=True, content__icontains=query) # <-- MODERATION FILTER
        user_results = AlumniUser.objects.filter(full_name__icontains=query)
    else:
        post_results = Post.objects.none()
        user_results = AlumniUser.objects.none()

    context = {
        'query': query,
        'post_results': post_results,
        'user_results': user_results,
    }
    return render(request, 'portal/search_results.html', context)

# --- !! THIS IS THE VIEW FOR ANNOUNCEMENTS !! ---
@login_required
def announcements_view(request):
    # Get all posts that are 'Announcement'
    announcement_posts = Post.objects.filter(is_approved=True, post_type='Announcement').order_by('-created_at') # <-- MODERATION FILTER
    
    context = {
        'posts': announcement_posts,
    }
    return render(request, 'portal/announcements.html', context)

# --- !! THIS IS THE VIEW FOR INVITES !! ---
@login_required
def invites_view(request):
    # Get all posts that are 'Invite'
    invite_posts = Post.objects.filter(is_approved=True, post_type='Invite').order_by('-created_at') # <-- MODERATION FILTER
    
    context = {
        'posts': invite_posts,
    }
    return render(request, 'portal/invites.html', context)

# --- !! ADD THESE 3 NEW VIEWS FOR MODERATION !! ---

@staff_member_required
def content_moderation_view(request):
    # Get all posts that are not yet approved
    unapproved_posts = Post.objects.filter(is_approved=False).order_by('-created_at')
    
    context = {
        'posts': unapproved_posts,
    }
    return render(request, 'portal/content_moderation.html', context)

@staff_member_required
def approve_post_view(request, pk):
    post = Post.objects.get(pk=pk)
    post.is_approved = True
    post.save()
    return redirect('content_moderation')

@staff_member_required
def delete_post_view(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('content_moderation')