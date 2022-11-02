from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from account import utils
last_email_data = []

def send_email(email, request, context, user, *args, **kwargs):
    uid = utils.encode_uid(user.pk)
    token = default_token_generator.make_token(user)
    template_data = {"first_name": user.first_name, "verification_link": f"/users/activate/{uid}/{token}/"}
    if settings.DEBUG:
        last_email_data.append(template_data)

    # TODO Test this after verifying zebec hcm email
    # VerificationEmail(user, context).send_email(user.email, template_data)
    print(template_data)


