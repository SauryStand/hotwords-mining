from django.conf.urls import url
import statistic.views

urlpatterns = [

    url(r'hashtag_timeline$', statistic.views.hashtag_timeline),
    url(r'hashtag_timeline_data$', statistic.views.hashtag_timeline_data),



]