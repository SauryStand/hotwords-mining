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


def hashtag_pie_data(request):
    res = pie.get_hashtag_pie_data_by_date()
    return HttpResponse(json.dumps(res), content_type="application/json")