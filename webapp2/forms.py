from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Reviews.models import Profile
from .models import properties


class PropertyForm(ModelForm):

  class Meta:
    model = properties
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(PropertyForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):

  class Meta:
    model = Profile
    fields = ['bio', 'image']

  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ['first_name', 'email', 'username', 'password1', 'password2']
    labels = {
        'first_name': "Name",
    }

  def __init__(self, *args, **kwargs):
    super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})
