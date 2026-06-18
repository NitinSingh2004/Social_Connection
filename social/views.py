from django.shortcuts import get_object_or_404, redirect
from .graph import graph  # Make sure 'graph' is imported from your graph.py file
from django.shortcuts import render, redirect
import uuid
from .models import SocialAccount
from django.http import JsonResponse
import os
from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import requests
import json
from django.contrib import messages
from django.utils import timezone
from accounts.models import User
from django.contrib.auth import login
from scheduler.models import Post, ScheduledPost
from datetime import datetime
def connections(request):
    print("running")
    if request.user.is_authenticated:
        print(request.user)
        connected_accounts = SocialAccount.objects.filter(
            user=request.user
        )
        print(connected_accounts)
    else:
        print(f"Not authenticated! Current user is: {request.user}")
        connected_accounts = []

    return render(
        request,
        "connection.html",
        {
            "connected_accounts": connected_accounts,
        }
    )


def linkedin_webhook(request):
    return render(request, "connection.html")

def instagram_webhook(request):
    return render(request, "connection.html")
def publish_to_facebook_api(content, social_account):
    url = f"https://graph.facebook.com/{social_account.page_id}/feed"
    payload = {
        "message": content,
        "access_token": social_account.page_access_token
    }
    response = requests.post(url, data=payload)
    return response.json()

# ==========================================
# CONFIGURATION
# ==========================================
APP_ID = "1008992491621351"
APP_SECRET = "586e6a2115efe5ad7d8ccc540117f48b"

REDIRECT_URI = (
    "https://nonpreformed-stimulatingly-vania.ngrok-free.dev/"
    "social/facebook_callback/"
)


# ==========================================
# FACEBOOK LOGIN REDIRECT
# ==========================================

@login_required
def facebook_webhook(request):
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "public_profile,email,pages_show_list,pages_read_engagement,pages_manage_posts",
          }

    auth_url = (
        "https://www.facebook.com/v20.0/dialog/oauth?"
        + urlencode(params)
    )

    return redirect(auth_url)

# ==========================================
# FACEBOOK WEBHOOK (SEPARATE ENDPOINT)
# ==========================================


def facebook_callback(request):
    """
    Facebook OAuth callback
    """

    code = request.GET.get("code")

    if not code:
        messages.error(request, "Facebook login cancelled.")
        return redirect("dashboard")

    # Exchange code for access token
    token_response = requests.get(
        "https://graph.facebook.com/v20.0/oauth/access_token",
        params={
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        timeout=30,
    )

    token_data = token_response.json()

    if "access_token" not in token_data:
        return JsonResponse(token_data, status=400)

    access_token = token_data["access_token"]

    # Get Facebook profile info
    user_response = requests.get(
        "https://graph.facebook.com/me",
        params={
            "access_token": access_token,
            "fields": "id,name",
        },
        timeout=30,
    )

    user_data = user_response.json()

    facebook_id = user_data.get("id")
    facebook_name = user_data.get("name")
    print(facebook_id)
    print(facebook_name)

    if not facebook_id:
        messages.error(request, "Unable to retrieve Facebook account.")
        return redirect("dashboard")
    # Fetch User Pages
    page_id = ""
    page_name = ""
    page_access_token = ""
    
    pages_response = requests.get(
        "https://graph.facebook.com/v20.0/me/accounts",
        params={"access_token": access_token},
        timeout=30
    )
    pages_data = pages_response.json()
    
    if "data" in pages_data and len(pages_data["data"]) > 0:
        first_page = pages_data["data"][0]
        page_id = first_page.get("id", "")
        page_name = first_page.get("name", "")
        page_access_token = first_page.get("access_token", "")

    # Get or fallback user
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(username="pankaj")

    # Save/Update database
    SocialAccount.objects.update_or_create(
        user=user,
        platform="facebook",
        defaults={
            "account_name": facebook_name,
            "account_id": facebook_id,
            "access_token": access_token,
            "page_id": page_id,
            "page_name": page_name,
            "page_access_token": page_access_token
        }
    )

    messages.success(
        request,
        f"Facebook account '{facebook_name}' connected successfully."
    )
    if not request.user.is_authenticated:
        login(request, user)

    return redirect("connections")


#### for Facebook post ####


def publish_facebook(request):
    # Get post
    post = get_object_or_404(Post)

    # Get connected Facebook account
    social = get_object_or_404(
        SocialAccount,
        user=request.user,
        platform="facebook"
    )

    # Facebook Graph API
    url = f"https://graph.facebook.com/{social.page_id}/feed"

    payload = {
        "message": post.caption,
        "access_token": social.page_access_token,
    }

    response = requests.post(url, data=payload, timeout=30)
    result = response.json()

    # Check success
    if "id" in result:
        messages.success(request, "Post published successfully!")

        # Optional: mark the post as published
        # post.status = "published"
        # post.save()

    else:
        error_message = result.get("error", {}).get(
            "message", "Publishing failed."
        )
        messages.error(request, error_message)

    return redirect("dashboard")














def create_post(request):
    # Ensure a consistent session thread ID for LangGraph memory state checkpointing
    if "graph_thread_id" not in request.session:
        request.session["graph_thread_id"] = str(uuid.uuid4())

    thread_id = request.session["graph_thread_id"]
    config = {"configurable": {"thread_id": thread_id}}

    # 1. Fetch connected accounts for the currently authenticated profile
    connected_platforms = list(
        SocialAccount.objects.filter(user=request.user).values_list('platform', flat=True)
    )

    # 2. Build the default baseline context dictionary
    context = {
        "generated_post": None,
        "platform": None,
        "prompt": None,
        "status": "idle",
        "connected_platforms": connected_platforms
    }

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "generate":
            prompt = request.POST.get("prompt")
            platform = request.POST.get("platform")

            # Update context immediately so user input doesn't disappear if graph fails
            context["prompt"] = prompt
            context["platform"] = platform

            initial_input = {
                "prompt": prompt,
                "platform": platform,
                "regenerate": False,
                "generated_post": ""
            }
            print("Starting Graph Generation with input:", initial_input)

            # Stream through the LangGraph agent states
            for event in graph.stream(initial_input, config, stream_mode="values"):
                print(f"the event is {event}")
                pass

        elif action in ["approve", "regenerate", "publish", "draft", "schedule"]:
            if action == "publish":
                platform = request.POST.get("platform", "")
                
                # Fetch generated post from state memory
                state = graph.get_state(config)
                generated_content = state.values.get("generated_post", "") if state and state.values else ""
                
                if not generated_content:
                    messages.error(request, "Failed to publish: No generated content found.")
                    return redirect("create_post")
                
                if platform == "facebook":
                    try:
                        social_account = SocialAccount.objects.get(user=request.user, platform="facebook")
                        
                        if not social_account.page_access_token or not social_account.page_id:
                            messages.error(request, "Facebook Page not connected properly. Please reconnect.")
                            return redirect("create_post")
                            
                        # Call Facebook API using the helper function
                        response_data = publish_to_facebook_api(generated_content, social_account)
                        
                        if "id" in response_data:
                            messages.success(request, "🎉 Your post has been successfully published to your Facebook Page!")
                        else:
                            error_msg = response_data.get("error", {}).get("message", "Unknown error")
                            messages.error(request, f"Facebook API Error: {error_msg}")
                            return redirect("create_post")
                            
                    except SocialAccount.DoesNotExist:
                        messages.error(request, "Facebook account not connected.")
                        return redirect("create_post")
                    except Exception as e:
                        messages.error(request, f"Error publishing to Facebook: {str(e)}")
                        return redirect("create_post")
                else:
                    # Mock success for other platforms for now
                    messages.success(request, f"🎉 Your post has been successfully published to {platform.title()}!")
                
                if "graph_thread_id" in request.session:
                    del request.session["graph_thread_id"]
                return redirect("dashboard")
            elif action == "draft":
                messages.success(request, "📝 Your post has been saved as a draft!")
                if "graph_thread_id" in request.session:
                    del request.session["graph_thread_id"]
                return redirect("dashboard")
            elif action == "schedule":
                dt_str = request.POST.get("schedule_time", "")
                platform = request.POST.get("platform", "None")
                
                # Fetch generated post from state memory
                state = graph.get_state(config)
                generated_content = state.values.get("generated_post", "") if state and state.values else ""
                
                if not generated_content:
                    messages.error(request, "Failed to schedule: No generated content found.")
                    return redirect("create_post")
                    
                if platform == "None":
                    platform = ""
                
                try:
                    # Convert string to aware datetime
                    dt = timezone.make_aware(datetime.strptime(dt_str, "%Y-%m-%dT%H:%M"))
                    
                    # 1. Create Post
                    post_obj = Post.objects.create(
                        user=request.user,
                        content=generated_content
                    )
                    
                    # 2. Create ScheduledPost
                    ScheduledPost.objects.create(
                        user=request.user,
                        content=post_obj,
                        platform=platform,
                        scheduled_time=dt
                    )
                    
                    # Nice readable format for message
                    readable_dt = dt.strftime("%b %d, %Y at %I:%M %p")
                    plat_str = f" on {platform.title()}" if platform else ""
                    messages.success(request, f"📅 Your post has been scheduled for {readable_dt}{plat_str}!")
                except Exception as e:
                    messages.error(request, f"Error scheduling post: {str(e)}")

                if "graph_thread_id" in request.session:
                    del request.session["graph_thread_id"]
                return redirect("create_post")

            print(f"Executing Graph Action: {action}")
            for event in graph.stream({"action": action}, config, stream_mode="values"):
                pass

            if action == "approve":
                # Fetch final state values to show on the success screen
                state = graph.get_state(config)
                context["generated_post"] = state.values.get("generated_post")
                context["platform"] = state.values.get("platform")
                context["prompt"] = state.values.get("prompt")
                context["status"] = "completed"
                
                # Clear thread memory footprint since execution workflow concluded cleanly
                if "graph_thread_id" in request.session:
                    del request.session["graph_thread_id"]
                    
                return render(request, "create_post.html", context)

    # 3. Read the post-execution state directly from LangGraph compilation memory
    state = graph.get_state(config)

    # 4. Correctly extract memory state values to pass down into your HTML layout context
    if state and state.values:
        context["generated_post"] = state.values.get("generated_post")
        context["platform"] = state.values.get("platform")
        
        # Clean up any tone meta tags (e.g., "[Tone: Witty]") from the raw prompt for the input field UI
        raw_prompt = state.values.get("prompt", "")
        if raw_prompt and " [Tone:" in raw_prompt:
            context["prompt"] = raw_prompt.split(" [Tone:")[0]
        else:
            context["prompt"] = raw_prompt

    # 5. Calculate and preserve status states accurately without destructive overwriting
    if state and state.next and state.tasks and state.tasks[0].interrupts:
        context["status"] = "reviewing"
    else:
        # If a generated post exists and we haven't explicit-returned via 'approve',
        # mark it as reviewing/ready rather than force-killing the session ID
        if context["generated_post"]:
            context["status"] = "reviewing"  # Allows users to read, edit, or regenerate it

    return render(request, "create_post.html", context)