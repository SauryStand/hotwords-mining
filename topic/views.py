import json
from django.http import HttpResponse
from django.shortcuts import render
from topic.models.TopicTrendsManager import TopicTrendsManager
from topic.models.TopicParameterManager import TopicParameterManager


def index(request):
    return render(request,'topic/index.html');