from django import forms

from .models import Download

class URLForm(forms.Form):
	your_url = forms.CharField(label='Your url', max_length=500)


class Form(forms.ModelForm):

    class Meta:
        model = Download
        fields = ('youtube_link',)

