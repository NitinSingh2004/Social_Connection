from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
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
from django.views.decorators.csrf import csrf_exempt
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




APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

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
        "scope": "public_profile,email,pages_show_list,pages_read_engagement,pages_manage_posts,read_insights",
          }

    auth_url = (
        "https://www.facebook.com/v20.0/dialog/oauth?"
        + urlencode(params)
    )

    return redirect(auth_url)


### facebook Endpoint ###
def facebook_callback(request):
    """
    Facebook OAuth callback
    """

    code = request.GET.get("code")

    if not code:
        messages.error(request, "Facebook login cancelled.")
        return redirect("dashboard")
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
    print("Token Response:", token_data)

    if "access_token" not in token_data:
        return JsonResponse(token_data, status=400)

    access_token = token_data["access_token"]

    user_response = requests.get(
        "https://graph.facebook.com/v20.0/me",
        params={
            "access_token": access_token,
            "fields": "id,name",
        },
        timeout=30,
    )

    user_data = user_response.json()
    print("User Response:", user_data)

    facebook_id = user_data.get("id")
    facebook_name = user_data.get("name")

    if not facebook_id:
        messages.error(request, "Unable to retrieve Facebook account.")
        return redirect("dashboard")
    page_id = ""
    page_name = ""
    page_access_token = ""

    page_stats = {
        "total_likes": 0,
        "total_followers": 0,
    }
    permissions = requests.get(
        "https://graph.facebook.com/v20.0/me/permissions",
        params={
            "access_token": access_token
        }
    )
    print(permissions.json())
    pages_response = requests.get(
        "https://graph.facebook.com/v20.0/me/accounts",
        params={
            "access_token": access_token
        },
        timeout=30
    )

    print("Pages Status:", pages_response.status_code)

    pages_data = pages_response.json()

    print("Pages Response:", pages_data)

    if "error" in pages_data:
        print("Facebook Error:", pages_data["error"])

    elif pages_data.get("data"):

        first_page = pages_data["data"][0]

        print("First Page:", first_page)

        page_id = first_page.get("id", "")
        page_name = first_page.get("name", "")
        page_access_token = first_page.get("access_token", "")

        print("Page ID:", page_id)
        print("Page Name:", page_name)
        print("Page Token:", page_access_token[:25] + "...")
        page_stats = get_page_stats(
            page_id,
            page_access_token
        )

        print("Page Stats:", page_stats)

    else:
        print("No Facebook Pages found for this account.")

    if request.user.is_authenticated:
        user = request.user
    else:
        return render(request, "login.html")
    SocialAccount.objects.update_or_create(
        user=user,
        platform="facebook",
        defaults={
            "account_name": facebook_name,
            "account_id": facebook_id,
            "access_token": access_token,
            "page_id": page_id,
            "page_name": page_name,
            "page_access_token": page_access_token,
            "facebook_likes": page_stats.get("total_likes", 0),
            "facebook_followers": page_stats.get("total_followers", 0),
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
    post = get_object_or_404(Post)
    social = get_object_or_404(
        SocialAccount,
        user=request.user,
        platform="facebook"
    )
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

    else:
        error_message = result.get("error", {}).get(
            "message", "Publishing failed."
        )
        messages.error(request, error_message)

    return redirect("dashboard")


### also for facebook ###
def get_page_stats(page_id, page_access_token):
    url = f"https://graph.facebook.com/v20.0/{page_id}"

    params = {
        "fields": "id,name,fan_count,followers_count",
        "access_token": page_access_token,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            return {
                "total_likes": 0,
                "total_followers": 0,
            }

        return {
            "total_likes": data.get("fan_count", 0),
            "total_followers": data.get("followers_count", 0),
        }

    except requests.exceptions.RequestException:
        return {
            "total_likes": 0,
            "total_followers": 0,
        }



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




### for instagram ###


CLIENT_ID2=os.getenv("CLIENT_ID2")
CLIENT_SECRET2 = os.getenv("CLIENT_SECRET2")

REDIRECT_URI2 = "https://nonpreformed-stimulatingly-vania.ngrok-free.dev/social/instagram_callback/"

SCOPES = [
    "instagram_business_basic",
    "instagram_business_content_publish"
]


def instagram_login(request):
    """
    Step 1: Redirect the user to the Instagram Login window.
    """
    scope_param = ",".join(SCOPES)
    authorization_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={CLIENT_ID2}"
        f"&redirect_uri={REDIRECT_URI2}"
        f"&scope={scope_param}"
        f"&response_type=code"
    )
    return redirect(authorization_url)


# The exact string you type into the "Verify Token" field in your Meta Dashboard
MY_VERIFY_TOKEN = "your_chosen_secure_verify_token_here"

CLIENT_ID = "1552124069826752"
CLIENT_SECRET = "524fda10056f2df33af7ce5a5a1b5bf4"


def instagram_callback(request):
    """
    Step 2 & 3: Handle the authentication callback from Instagram.
    Also handles Meta's webhook validation challenge.
    """
    if request.method == "GET" and "hub.mode" in request.GET:
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == MY_VERIFY_TOKEN:
            return HttpResponse(challenge, content_type="text/plain")
        else:
            return HttpResponse("Verification token mismatch", status=403)

    error = request.GET.get('error')
    code = request.GET.get('code')

    if error:
        return HttpResponseBadRequest(f"User denied authorization: {error}")

    if not code:
        return HttpResponseBadRequest("Authorization code missing from callback.")

    # STEP A: Exchange Authorization Code for a Short-Lived User Token (Valid ~1 hour)
    short_token_url = "https://api.instagram.com/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID2,
        "client_secret": CLIENT_SECRET2,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI2,
        "code": code
    }

    response = requests.post(short_token_url, data=payload)
    if response.status_code != 200:
        return JsonResponse(response.json(), status=response.status_code)

    token_data = response.json()
    short_lived_token = token_data.get("access_token")
    instagram_user_id = token_data.get("user_id")

    # STEP B: Exchange Short-Lived Token for a Long-Lived Token (Valid 60 Days)
    long_token_url = "https://graph.instagram.com/access_token"
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": CLIENT_SECRET2,
        "access_token": short_lived_token
    }

    long_response = requests.get(long_token_url, params=params)
    if long_response.status_code != 200:
        return JsonResponse(long_response.json(), status=long_response.status_code)

    long_token_data = long_response.json()
    long_lived_token = long_token_data.get("access_token")
    return JsonResponse({
        "status": "Success",
        "message": "Account connected successfully!",
        "instagram_user_id": instagram_user_id,
        "long_lived_token_preview": f"{long_lived_token[:10]}..."
    })



#### For Linkdin ####

CLIENT_ID3 = os.getenv("CLIENT_ID3")
CLIENT_SECRET3 = os.getenv("CLIENT_SECRET3")


REDIRECT_URI3 = "https://nonpreformed-stimulatingly-vania.ngrok-free.dev/social/linkedin_callback/"

SCOPES = [
    "openid",
    "profile",
    "email",
    "w_member_social"
]


def linkedin_login(request):

    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID3}"
        f"&redirect_uri={REDIRECT_URI3}"
        f"&scope={' '.join(SCOPES)}"
    )

    return redirect(auth_url)


def linkedin_callback(request):

    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "Authorization code missing."})

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI3,
        "client_id": CLIENT_ID3,
        "client_secret": CLIENT_SECRET3,
    }

    token_response = requests.post(token_url, data=payload)

    if token_response.status_code != 200:
        return JsonResponse(token_response.json(), status=token_response.status_code)

    token_data = token_response.json()

    access_token = token_data["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile_response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers=headers
    )

    if profile_response.status_code != 200:
        return JsonResponse(profile_response.json(), status=profile_response.status_code)

    profile = profile_response.json()

    linkedin_id = profile.get("sub")
    linkedin_name = profile.get("name")

    if request.user.is_authenticated:
        user = request.user
    else:
        return render(request, "login.html")

    SocialAccount.objects.update_or_create(
        user=user,
        platform="linkedin",
        defaults={
            "account_name": linkedin_name,
            "account_id": linkedin_id,
            "access_token": access_token,
        }
    )

    return render(request,"connection.html")