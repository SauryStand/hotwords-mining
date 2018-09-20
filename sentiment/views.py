from django.shortcuts import render


# Create your views here.
from sentiment.models.SentimentManager import query_sentiment_for_online_data
import json
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from sentiment.models.SentimentManager import query_sentiment_for_online_data
import json
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'sentiment/index.html')