from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# for ReCaptchaField
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
#for CrearteListingForm
from .models import Product, Bidding, Comment #,Category


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()


# create or register a user(model form)
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
#authenticate a user (model form)


class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=TextInput())

    captcha= ReCaptchaField(widget=ReCaptchaV2Checkbox())
        


#create a listing
class CreateListingForm(forms.ModelForm):
    # CATEGORY_CHOICES = [(category.name, category.name) for category in Category.objects.all()]
    # category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    class Meta:
        model = Product
        labels = {
            'name' : 'Name',
            'description' : 'Description',
            'startingbid' : 'Starting Bid',
            'images' : 'Image',
            # 'category' : 'Category'
        }
        fields = ['name', 'brand','description', 'start_bid', 'image'] 


class BiddingForm(forms.ModelForm):
    class  Meta:
        model = Bidding
        labels = {
            'bidprice' : ''
        }
        fields = [
            'bidprice'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {
            'comment' : ''
        }
        fields = [
            'comment'
        ]


