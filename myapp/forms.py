from django import forms
from myapp.models import Order, Review, Student

class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks')
    ]

    name = forms.CharField(max_length=100, required=False, label='Student Name')
    max_price = forms.IntegerField(min_value=0, label='Maximum Price')
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int, required=False, label='Preferred Course Duration')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'Student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'Student': u'Student Name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email:', 'rating': u'Rating: An integer between 1(worst) and 5(best):'}

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = {'username', 'password', 'first_name', 'last_name', 'city', 'interested_in', 'image'}
        field_order = ['username', 'password', 'first_name', 'last_name', 'city', 'interested_in', 'image']
        widgets = {
            'city': forms.RadioSelect(attrs={'class': 'radio'}),
            'password': forms.PasswordInput
        }
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'interested_in': "Interested In"
        }