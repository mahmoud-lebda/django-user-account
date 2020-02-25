from django.shortcuts import render
from django.core.mail import send_mail


def sendmail(request):
    send_mail('subject3', 'body of the messafsdafadsfsadfasdfdsafsdage', 'django@opelownersgang.com',
              ['mahmoud_lebda@hotmail.com', 'mahmoud.lebda@gmail.com'])
    return render(request, 'email.html')
