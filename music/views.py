from __future__ import unicode_literals
import youtube_dl

from django.core import serializers
from . import models

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .forms import URLForm
from .forms import Form


def index(request):
	if request.method == 'POST':
		form = Form(request.POST)
		if form.is_valid():

			form.save()# Saving form data to model
			
			youtube_link = form.cleaned_data['youtube_link']# Extracting form data

			request.session['youtube_link'] = youtube_link # Passing form data


			entry_list = list(models.Download.objects.values_list('youtube_link'))#Extracting youtube_link field
			
			return render(request, 'music/download.html', {'data': entry_list})

	else:
		form = Form()

	return render(request, 'music/index.html', {'form': form})
	
def download(request):

	youtube_link = request.session['youtube_link']# Recieving form data form index function
	
	if request.method == 'POST':# If user ckicks the button, download function is called
		download1(youtube_link)

	return render(request, 'music/download.html')	

def download1(video_url):
    ydl_opts = {
        'outtmpl': 'songs/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])