from django.urls import path

from .views import *

app_name = 'performer_app'

urlpatterns = [
    path('<int:id>', PerformerPage.as_view(), name='performer_page'),
    path('', Performers.as_view(), name='performers'),
    path('candidates/', Candidates.as_view(), name='candidates'),
    path('orders', PerformerOrders.as_view(), name='orders'),
]
