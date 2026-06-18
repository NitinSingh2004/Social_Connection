from django.db import models

class SocialAccount(models.Model):
    PLATFORMS = (
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
    )

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="social_accounts" # Good practice for clean reverse lookups
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORMS
    )

    # 1. This will store the User's Long-Lived Access Token
    access_token = models.TextField()

    # 2. This will store the Page Token (Crucial for silent background auto-posting!)
    page_access_token = models.TextField(
        blank=True, 
        null=True, 
        help_text="Required for publishing content to Facebook Pages seamlessly"
    )

    page_id = models.CharField(max_length=200, blank=True, null=True)
    page_name = models.CharField(max_length=200, blank=True, null=True)

    # 3. The unique ID of the target Page or Instagram Account
    account_id = models.CharField(
        max_length=255
    )

    # 4. Optional but helpful: The profile/page name to display in your UI
    account_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Name of the connected page or profile"
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_platform_display()} ({self.account_name or self.account_id})"