
from django.conf.urls import url
import sentiment.views


urlpatterns = [
    url(r'^$', sentiment.views.index),
    url(r'^sentiment_query$', sentiment.views.query)
]
