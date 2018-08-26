# Create your views here.

import json
from django.shortcuts import render
from django.http import HttpResponse


def hashtag_timeline(request):
    res = {
        'date': request.GET.get('date'),
        'hashtag': request.GET.get('hashtag'),
    }
    return render(request, 'statistic/hashtag_timeline.html', res)