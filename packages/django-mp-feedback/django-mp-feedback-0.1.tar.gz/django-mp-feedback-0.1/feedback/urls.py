
from django.urls import path

from feedback.views import CreateFeedbackView


app_name = 'feedback'


urlpatterns = [

    path('', CreateFeedbackView.as_view(), name='create')

]
