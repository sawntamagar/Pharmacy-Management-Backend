from django.core.mail import EmailMessage
import os
# from account.models import PmsUser nghnhxeyykggpgui
class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        from_email=os.environ.get('EMAIL_FROM'),
        to=[data['to_email']]
        )
        email.send()
        
# def send_reset_email(user, token):
#     reset_url = 'http://localhost:3000/api/user/reset/' + token
#     body = 'Click Following Link to Reset Your Password '+reset_url
#     data = {
#     'subject':'Reset Your Password',
#     'body':body,
#     'to_email':user.email
#     }
#     email = EmailMessage(
#     subject=data['subject'],
#     body=data['body'],
#     from_email='pharmacypost8@gmail.com',
#     to=[data['to_email']]
#     )
#     email.send()
#     email.send(
#         {"type": "reset", "recipient": user.email, "subject": "Reset Account Password", "message": reset_url}
#     )

# def send_reset_email(user, token):
   
#     user= PmsUser.objects.get(email=email)
#     token = user.get_token()
#     reset_url = 'http://localhost:3000/api/user/reset/' + token
#             #send Email
#     body = 'Click Following Link to Reset Your Password '+reset_url
#     data = {
#     'subject':'Reset Your Password',
#     'body':body,
#     'to_email':user.email
#     }
#     reset_url = 'http://localhost:3000/api/user/reset/' + token
#     print(reset_url)
#     email = EmailMessage(
#     subject=data['subject'],
#     body=data['body'],
#     from_email='pharmacypost@gmail.com',
#     to=[data['to_email']]
#     )
#     email.send()
        
   
    
    
# def send_confirmation_email(user):
#     token = user.get_token()
#     confirmation_url = os.environ.get("CLIENT_SERVER_URL") + "company-verify-email/" + token
#     QueueUtils.add_mail_to_queue(
#         {"type": "verify", "recipient": user.email, "subject": "Confirm Account Email", "message": confirmation_url}
#     )        