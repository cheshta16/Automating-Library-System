from main.models import Details
from django.core.mail import send_mail
from datetime import date

def sendmail():
    today = date.today()
    for p in Details.objects.raw('SELECT * FROM Main_Details'):
        if(today > p.returndate):
            mail = p.email
            message = 'This is a reminder to return the Book : %s (Book No.:%s), whose return date is : %s' %(p.bookname,p.bookno,p.returndate)
            send_mail('Book Return Reminder', message , 'librarybookreminder@gmail.com', [mail], fail_silently=False)