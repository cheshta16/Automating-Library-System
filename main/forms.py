from django.forms import ModelForm
from main.models import Details

class BookForm(ModelForm):
    class Meta:
        model = Details
        fields = ['bookno', 'bookname', 'bookauthor', 'dateissued', 'returndate']