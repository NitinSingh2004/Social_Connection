from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from social.models import SocialAccount
from scheduler.models import ScheduledPost, Post
from social.models import SocialAccount

User = get_user_model()


def check_email(request):
    """Asynchronously checks if an email already exists in the database."""
    email = request.GET.get("email", "").strip()
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})


def check_username(request):
    """Asynchronously checks if a username already exists in the database."""
    username = request.GET.get("username", "").strip()
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({"exists": exists})


def signup_view(request):
    """Handles new user registration."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
        }

        if not all([first_name, last_name, username, email, password1, password2]):
            context["error"] = "All fields are required."
            return render(request, "signup.html", context)

        if password1 != password2:
            context["error"] = "Passwords do not match."
            return render(request, "signup.html", context)

        if User.objects.filter(username=username).exists():
            context["error"] = "This username is already taken."
            return render(request, "signup.html", context)

        if User.objects.filter(email=email).exists():
            context["error"] = "A user with this email already exists."
            return render(request, "signup.html", context)

        # Create user safely via the custom UserManager
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Log the user in directly
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("dashboard")  # Redirect straight to dashboard

    return render(request, "signup.html")


def login_view(request):
    """Handles user login authentication using Email."""
    print("running")
    if request.user.is_authenticated:
        return redirect("dashboard")
    print("working")
    if request.method == "POST":
        # Using email because USERNAME_FIELD = "email" in your model
        email = request.POST.get("username", "").strip()
        password = request.POST.get("password")
        print(email)
        # Pass the email string into the 'username' parameter of authenticate
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            print("Login successful:", user)
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            print("Authenticated:", request.user.is_authenticated)

            return redirect("dashboard")
        else:
            context = {
                "email": email,
                "error": "Invalid email or password."
            }
            # Re-render login, NOT dashboard
            return render(request, "login.html", context) 

    return render(request, "login.html")


def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("login")


ALL_PLATFORMS = [
    {"key": "instagram", "label": "Instagram"},
    {"key": "facebook",  "label": "Facebook"},
    {"key": "twitter",   "label": "X (Twitter)"},
    {"key": "linkedin",  "label": "LinkedIn"},
    {"key": "tiktok",    "label": "TikTok"},
    {"key": "pinterest", "label": "Pinterest"},
    {"key": "youtube",   "label": "YouTube"},
]


def dashboard_view(request):
    # Connected social accounts
    connected_accounts = SocialAccount.objects.filter(user=request.user)

    # Connected platform keys
    connected_keys = set(
        connected_accounts.values_list("platform", flat=True)
    )

    # Platforms not yet connected
    unconnected_platforms = [
        p for p in ALL_PLATFORMS
        if p["key"] not in connected_keys
    ]

    # Dashboard statistics
    total_posts = Post.objects.filter(
        user=request.user
    ).count()

    published_count = ScheduledPost.objects.filter(
        user=request.user,
        status="published"
    ).count()

    scheduled_count = ScheduledPost.objects.filter(
        user=request.user,
        status="scheduled"
    ).count()

    connected_accounts_count = connected_accounts.count()

    # Upcoming scheduled posts
    scheduled_posts = (
        ScheduledPost.objects.filter(
            user=request.user,
            status="scheduled"
        )
        .select_related("content")
        .order_by("scheduled_time")[:10]
    )

    context = {
        "connected_accounts": connected_accounts,
        "connected_accounts_count": connected_accounts_count,
        "unconnected_platforms": unconnected_platforms,

        "scheduled_posts": scheduled_posts,

        "total_posts": total_posts,
        "published_count": published_count,
        "scheduled_count": scheduled_count,
    }

    return render(request, "dashboard.html", context)


def password_reset(request):
    # Place holder layout or logic
    return render(request, "login.html")