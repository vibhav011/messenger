from django.urls import path
from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('signup/', views.signup, name='signup'),
	path('signup/', views.signup, name='signup'),
	path('temporary-page1/', views.signuprequest, name='signuprequest'),
	path('temporary-page2/', views.loginrequest, name='loginrequest'),
	path('ajax/new-chat-request', views.newChatRequest, name='newchatrequest'),
	path('ajax/send-new-message', views.sendNewMessage, name='sendnewmessage'),
	path('ajax/get-new-message', views.getNewMessage, name='getnewmessage'),
	path('ajax/seen-request', views.seenRequest, name='seenrequest'),
]