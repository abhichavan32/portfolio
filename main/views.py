from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Certificate
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def projects(request):
    return render(request, 'main/projects.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Email sending logic
        subject = f'New message from {name} ({email})'
        full_message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
        recipient_list = ['abhi22chavan@gmail.com']  # Replace with your recipient email

        try:
            send_mail(subject, full_message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
        except Exception as e:
            messages.error(request, f'There was an error sending your message: {e}')

        return redirect('contact')

    return render(request, 'main/contact.html')

def certifications(request):
    if request.method == 'POST' and request.FILES.get('certificate_file'):
        Certificate.objects.create(
            title=request.POST.get('title'),
            issuer=request.POST.get('issuer'),
            description=request.POST.get('description'),
            issue_date=request.POST.get('issue_date'),
            certificate_file=request.FILES['certificate_file']
        )
        messages.success(request, 'Certificate uploaded successfully!')
        return redirect('certifications')
    
    certificates = Certificate.objects.all()
    return render(request, 'main/certifications.html', {'certificates': certificates})
