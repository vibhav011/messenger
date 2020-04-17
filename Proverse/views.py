from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, Message, SessionList, MessageQueue, DeliveredQueue, SeenQueue
import datetime

def getdatetime() :
	d = datetime.datetime.now()
	return str(d.day)+'/'+str(d.month)+'/'+str(d.year)+' '+str(d.hour)+':'+str(d.minute)

class UserSend :
	def __init__(self, username, firstname, lastname, onlineNow, lastActive) :
		self.username = username
		self.firstname = firstname
		self.lastname = lastname
		self.onlineNow = onlineNow
		self.lastActive = lastActive

def WhoIsLoggedIn(request) :
	if not request.session.session_key :
		request.session.save()

	ses_key = request.session.session_key
	user = None

	ses = SessionList.objects.filter(key = ses_key)

	if ses.exists() :
		user = User.objects.get(username = ses[0].username)

	return user

def homepage(request) :
	if not request.session.session_key :
		request.session.save()

	usr = WhoIsLoggedIn(request)

	if usr is None :
		return redirect(login)

	msgs = []

	for msg in Message.objects.all() :
		if msg.sender == usr.username or msg.receiver == usr.username:
			msgs.append(msg)
	
	chatsUsers = usr.chats.split(';')
	chats = []
	for uname in chatsUsers :
		if uname != "" :
			u = User.objects.get(username = uname)
			chats.append(UserSend(u.username, u.firstname, u.lastname, u.onlineNow, u.lastActive))

	blacklist = usr.blacklist.split(';')

	return render(request, 'interface.html', {'user' : usr, 'msgss' : msgs, 'chats' : chats, 'blacklist' : blacklist})

def login(request) :
	if WhoIsLoggedIn(request) is not None :
		return redirect(homepage)

	return render(request, 'login.html')

def logout(request) :
	if not request.session.session_key:
		request.session.save()

	ss = SessionList.objects.get(key = request.session.session_key)
	uu = User.objects.get(username = ss.username)
	uu.onlineNow = False
	uu.save()
	ss.delete()
	return redirect(login)

def signup(request) :
	if WhoIsLoggedIn(request) is not None :
		return redirect(homepage)

	return render(request, 'signup.html')

def loginrequest(request) :

	if not request.session.session_key:
		request.session.save()

	usern = request.POST.get("username", "")
	pwd = request.POST.get("password", "")

	users = User.objects.all()
	for u in users :
		if u.username == usern :
			if u.password == pwd :
				SessionList.objects.create(key = request.session.session_key, username = usern)
				u.onlineNow = True
				u.save()
				return redirect(homepage)
			break
	return redirect(login)

def signuprequest(request) :

	if not request.session.session_key :
		request.session.save()

	fname = request.POST.get("fname", "")
	lname = request.POST.get("lname", "")
	usern = request.POST.get("username", "")
	pwd = request.POST.get("password", "")

	users = User.objects.all()
	for u in users :
		if u.username == usern :
			return redirect(signup)

	User.objects.create(username = usern, password = pwd, firstname = fname, lastname = lname, chats = "", blacklist = "", onlineNow = True, lastActive = getdatetime())
	SessionList.objects.create(key = request.session.session_key, username = usern)

	return redirect(homepage)

def newChatRequest(request) :
	requestFrom = request.POST.get('myself', '')
	requestTo = request.POST.get('withwhom', '')
	
	usr = User.objects.filter(username = requestTo)

	if usr.exists() and requestFrom != requestTo :
		u = usr[0]
		blah = User.objects.get(username = requestFrom)
		blah.chats += ";" + requestTo
		blah.save()
		usrObj = {'username' : u.username, 'firstname' : u.firstname, 'lastname' : u.lastname, 'onlineNow' : u.onlineNow, 'lastActive' : u.lastActive}
		data = {'exists' : True, 'userDetails' : usrObj}
		return JsonResponse(data)
	else :
		data = {'exists' : False}
		return JsonResponse(data)

def sendNewMessage(request) :
	From = request.POST.get('from', '')
	To = request.POST.get('to', '')
	msg1 = request.POST.get('message', '')

	if From in User.objects.get(username = To).blacklist.split(';') :
		To = '__blacklist__'

	msgid = Message.objects.all().count() + 1

	Message.objects.create(msgID = msgid, sender = From, receiver = To, msg = msg1, datetime = getdatetime(), delivered = False, seen = False)
	MessageQueue.objects.create(msgID = msgid, sender = From, receiver = To, msg = msg1, datetime = getdatetime())

	data = {'mid' : msgid}
	return JsonResponse(data)

def getNewMessage(request) :
	From = request.POST.get('from', '')
	userStatus = request.POST.get('userStatus', '')
	blah = User.objects.get(username = From)
	ar = blah.chats.split(';')
	msgs = []
	delv = []
	seen = []
	users = []

	nm = MessageQueue.objects.filter(receiver = From)
	for msg in nm :
		msgs.append({"msgID" : msg.msgID, "sender" : msg.sender, "receiver" : msg.receiver, "msg" : msg.msg, "datetime" : msg.datetime})
		wtf = Message.objects.get(msgID = msg.msgID)
		wtf.delivered = True
		wtf.save()
		DeliveredQueue.objects.create(msgID = msg.msgID, sender = msg.sender, receiver = From)
		if msg.sender not in ar :
			blah.chats += ';' + msg.sender
			blah.save()
			udetails = User.objects.get(username = msg.sender)
			users.append({'username' : udetails.username, 'firstname' : udetails.firstname, 'lastname' : udetails.lastname, 'onlineNow' : udetails.onlineNow, 'lastActive' : udetails.lastActive})
	nm.delete()

	dq = DeliveredQueue.objects.filter(sender = From)
	for msg in dq :
		delv.append({"msgID" : msg.msgID, "sender" : msg.sender, "receiver" : msg.receiver})
	dq.delete()

	sq = SeenQueue.objects.filter(sender = From)
	for msg in sq :
		seen.append({"msgID" : msg.msgID, "sender" : msg.sender, "receiver" : msg.receiver})
	sq.delete()

	uf = User.objects.get(username = userStatus)

	data = {'users' : users, 'msgs' : msgs, 'delv' : delv, 'seen' : seen, 'userOnline' : uf.onlineNow, 'lastSeen' : uf.lastActive}
	return JsonResponse(data)

def seenRequest(request) :
	mids = request.GET.get('mids', '').split(";")

	for mmm in mids :
		if mmm != "" :
			mo = Message.objects.get(msgID = mmm)
			mo.seen = True
			mo.save()
			SeenQueue.objects.create(msgID = mmm, sender = mo.sender, receiver = mo.receiver)

	return JsonResponse({"success" : True})

