from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=10)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Details(models.Model):
    bookno = models.CharField(max_length=100)
    bookname = models.CharField(max_length=100)
    bookauthor = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="", editable=False)
    dateissued = models.DateField('date issued')
    returndate = models.DateField('return date')

    def __str__(self):
        return self.bookname
