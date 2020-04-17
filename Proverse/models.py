from django.db import models

class User(models.Model) :
	username = models.CharField(max_length = 15)
	password = models.CharField(max_length = 50)
	firstname = models.CharField(max_length = 25)
	lastname = models.CharField(max_length = 25)
	chats = models.TextField()				# usernames of users seperated by ;
	blacklist = models.TextField()
	onlineNow = models.BooleanField()
	lastActive = models.CharField(max_length = 20)

class Message(models.Model) :
	msgID = models.PositiveIntegerField()
	sender = models.CharField(max_length = 15)
	receiver = models.CharField(max_length = 15)
	msg = models.TextField()
	datetime = models.CharField(max_length = 20)
	delivered = models.BooleanField()
	seen = models.BooleanField()
	# visibleToSender = models.BooleanField()
	# visibleToReceiver = models.BooleanField()

class MessageQueue(models.Model) :
	msgID = models.PositiveIntegerField()
	sender = models.CharField(max_length = 15)
	receiver = models.CharField(max_length = 15)
	msg = models.TextField()
	datetime = models.CharField(max_length = 20)
	# visibleToSender = models.BooleanField()
	# visibleToReceiver = models.BooleanField()

class DeliveredQueue(models.Model) :
	msgID = models.PositiveIntegerField()
	sender = models.CharField(max_length = 15)
	receiver = models.CharField(max_length = 15)

class SeenQueue(models.Model) :
	msgID = models.PositiveIntegerField()
	sender = models.CharField(max_length = 15)
	receiver = models.CharField(max_length = 15)

class SessionList(models.Model) :
	key = models.CharField(max_length = 100)
	username = models.CharField(max_length = 25)