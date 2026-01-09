from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.timezone import now

def send_verification_email(user, token):
    verify_url = f"http://localhost:3000/verify-email/{token}"

    subject = "Verify your email"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    html_content = render_to_string(
        "emails/verify_email.html",
        {
            "user": user,
            "verify_url": verify_url,
            "year": now().year,
        }
    )

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
