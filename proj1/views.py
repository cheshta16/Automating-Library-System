from django.shortcuts import render, redirect, reverse
from main.models import Member, Details
from datetime import date
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .sendmail import sendmail

def homepage(request):
    return render(request, 'homepage.html')
def signup(request):
    if request.method=='POST':
        if request.POST.get:
            member = Member()
            member.name = request.POST.get('name')
            member.rollno = request.POST.get('roll')
            member.phone = request.POST.get('phone')
            member.email = request.POST.get('email')
            member.password = request.POST.get('psw')
            member.save()
            return redirect(reverse('login'))

    return render(request, 'signup form.html')

def login(request):
    if request.method == 'GET':
        mail = request.GET.get('email')
        psw = request.GET.get('psw')
        try:
            info = Member.objects.get(email=mail, password=psw)
            return redirect(reverse('details', kwargs={'info': info}))
        except Member.DoesNotExist:
            return render(request, 'login form.html', {'error_message': ' Login Failed! Enter the username and password correctly'})

    return render(request, 'login form.html')

def details(request, info):
    inform = Member.objects.get(name=info)
    mail = inform.email
    booklist = Details.objects.filter(email=mail)
    count = Details.objects.filter(email=mail).count()
    fine = 0
    today = date.today()
    sendmail()
    
    for book in booklist:
        if(today > book.returndate):
            fine+= (((today - book.returndate).days)*5)
    if request.method == 'POST':
        if 'issue' in request.POST:
            book = Details()
            book.bookno = request.POST.get('bookno')
            book.bookname = request.POST.get('bookname')
            book.bookauthor = request.POST.get('bookauthor')
            book.email = mail
            book.dateissued = request.POST.get('dateissued')
            book.returndate = request.POST.get('returndate')
            book.save()
            count = Details.objects.filter(email=mail).count()
            booklist = Details.objects.filter(email=mail)
            return render(request, 'student.html', {'inform':inform, 'booklist':booklist, 'count':count, 'fine':fine, 'today':today})

        elif 'return' in request.POST:
            bno = request.POST.get('return')
            Details.objects.filter(bookno=bno, email=mail).delete()
            count = Details.objects.filter(email=mail).count()
            booklist = Details.objects.filter(email=mail)
            return render(request, 'student.html', {'inform': inform, 'booklist': booklist, 'count': count, 'fine':fine, 'today':today})

    else:
        return render(request, 'student.html', {'inform':inform, 'booklist':booklist, 'count':count, 'fine':fine, 'today':today})

@periodic_task(run_every=crontab(hour="*/24"))
def trigger_emails():
    sendmail()