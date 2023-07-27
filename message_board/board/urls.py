from django.urls import path
from .views import *

urlpatterns = [
   path('', SearchAnnouncement.as_view(), name='announcement_search'),
   # pk — это первичный ключ объявления, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
   path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
   path('<int:pk>/edit/', AnnouncementUpdate.as_view(), name='announcement_update'),
   path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcement_delete'),
   path('private/', PrivateAnnouncements.as_view(), name='private_page'),
   path('responses/<int:pk>', ResponseList.as_view(), name='response_list'),
   path('private_resp/', PrivateResponseList.as_view(), name='private_resp'),
   path('response/<int:pk>', ResponseDetail.as_view(), name='response_detail'),
   path('<int:pk>/resp_create/', ResponseCreate.as_view(), name='response_create'),
   path('<int:pk>/resp_edit/', ResponseUpdate.as_view(), name='response_edit'),
   path('<int:pk>/resp_delete/', ResponseDelete.as_view(), name='response_delete'),
   path('response/<int:pk>/accept', accept, name='accept'),
   path('response/<int:pk>/reject', reject, name='reject'),
]
