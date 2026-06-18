from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ScheduledPost

from social.models import SocialAccount

@login_required
def scheduler(request):
    connected_accounts = SocialAccount.objects.filter(user=request.user)
    connected_dict = {acc.platform: acc for acc in connected_accounts}
    
    selected_platform = request.GET.get('platform')
    
    if not selected_platform and connected_accounts.exists():
        selected_platform = connected_accounts.first().platform
        
    if selected_platform:
        posts = ScheduledPost.objects.filter(
            user=request.user, 
            platform=selected_platform
        ).order_by('-scheduled_time')
        
        selected_account = connected_dict.get(selected_platform)
        account_name = selected_account.account_name if selected_account and selected_account.account_name else request.user.username
    else:
        posts = ScheduledPost.objects.filter(user=request.user).order_by('-scheduled_time')
        account_name = request.user.username
        
    context = {
        "connected_dict": connected_dict,
        "selected_platform": selected_platform,
        "posts": posts,
        "account_name": account_name
    }
    
    return render(request, "scheduler.html", context)

def calendar(request):
    return render(request, 'scheduler.html')
    



















