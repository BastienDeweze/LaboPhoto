# from .models import Account
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import EmailMessage
# from django.contrib.sites.models import Site

# @receiver(post_save, sender=Account)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         print(sender)
#         print(kwargs)
#         print(instance)
#         current_site = Site.objects.get_current()
#         print(current_site)
#         mail_subject = 'Activation de votre compte.'
#         message = render_to_string('accounts/account_verification_email.html', {
#             'user': instance,
#             'domain': current_site,
#             'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
#             'token': default_token_generator.make_token(instance),
#         })
#         to_email = instance.email
#         send_email = EmailMessage(mail_subject, message, to=[to_email])
#         send_email.send()
