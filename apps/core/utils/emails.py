from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_html_email(subject, template_name, context, to_email):
    """
    Utility to send HTML emails using Django templates.
    """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
