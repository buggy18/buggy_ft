# -*- coding: utf-8 -*-

from linepy import *
from akad.ttypes import Message
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, shutil
from subprocess import check_output

botStart = time.time()

#puy = LINE()
puy = LINE("Auth Token")
#puy = LINE("Email","Password")
puy.log("Your Auth Token : \n" + str(puy.authToken))

settingOpen = codecs.open("setting.json","r","utf-8")

puyMID = puy.profile
puyProfile = puy.getProfile()
puySettings = puy.getSettings()
oepoll = OEPoll(puy)
call = puy
settings = json.load(settingOpen)
MOD = ["uac8e3eaf1eb2a55770bf10c3b2357c33","u99b45ddca57a7f98ef13a92c32b28d44"]

read = {
	"readPoint": {},
	"readMember": {},
	"readTime": {},
	"ROM": {}
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

cctv = {
	"point1":{}, #cyduk
	"point2":{}, #point
	"point3":{}, #MENTION
	"point4":{} #SIDER MEM
}

with open('owner.json', 'r') as fp:
	owner = json.load(fp)

myProfile["displayName"] = puyProfile.displayName
myProfile["statusMessage"] = puyProfile.statusMessage
myProfile["pictureStatus"] = puyProfile.pictureStatus

buggyhelp="""- Buggy Free Used -

Speed
@bye
Rerun
Runtime
Myinfo
About
Checkalive
Getpicture @
Getcover @
Infogroup
Groupmemberlist
  - REMOTE -
List Group
Memberlist to (num)
Openlink to (num)
Closelink to (num)
  - MEDIA -
InstaUser
Motivate
Quotes
CreepyPasta"""

def restartBot():
	print ("[ INFO ] BOT RESETTED")
	time.sleep(3)
	python = sys.executable
	os.execl(python, python, *sys.argv)

def removeCmd(text, key=''):
	if key == '':
		setKey = '' if not settings['setKey']['status'] else settings['setKey']['key']
	else:
		setKey = key
	text_ = text[len(setKey):]
	sep = text_.split(' ')
	return text_[len(sep[0] + ' '):]

def command(text):
	anuan = text.lower()
	if anuan.startswith(settings["keyCommand"]):
		cmd = anuan.replace(settings["keyCommand"],"")
	else:
		cmd = "command"
	return cmd

def logError(text):
	puy.log(" ( ERROR MESSAGES DETECTED ) " + str(text))
	time_ = datetime.now()
	with open("errorlogs.txt","a") as error:
		error.write("\n[%s] %s" % (str(time), text))

def puyStarted(op):
	try:
		if op.type == 0:
			print (" -> 0 ( NO ONE WORKING )")
			return
		if op.type == 5:
			print (" -> 5 ( SOMEONE ADDED BUGGY )")
			if settings["autoAdd"] == True:
				puy.sendMessage(op.param1, "Hello Mr.{} Thx for added buggy as y'friend!".format(str(puy.getContact(op.param1).displayName)))
		if op.type == 13:
			print (" -> 13 ( INVITE GROUP NOTIFY )")
			group = puy.getGroup(op.param1)
			inviters = puy.getContact(op.param2)
			if settings["autoJoin"] == True:
				puy.acceptGroupInvitation(op.param1)
				puy.sendMessage(op.param1, "Hello Mr.{} Thx for invite buggy!".format(str(puy.getContact(op.param2).displayName)))
		if op.type == 15:
			print (" -> 15 ( NOTIFY MEMBER LEFT FROM GROUP )")
			if settings['greet']['leave']['status']:
			  tz = pytz.timezone("Asia/Jakarta")
			  timeNow = datetime.now(tz=tz)
			  puy.sendMessage(op.param1, settings['greet']['leave']['message'].format(name=puy.getCompactGroup(op.param1).name)+"\n\n"+timeNow.strftime('%H : %M : %S'))
		if op.type == 17:
			print (" -> 17 ( NOTIFY MEMBER JOINED A GROUP )")
			if settings['greet']['join']['status']:
			  tz = pytz.timezone("Asia/Jakarta")
			  timeNow = datetime.now(tz=tz)
			  puy.sendMessage(op.param1, settings['greet']['join']['message'].format(name=puy.getCompactGroup(op.param1).name)+"\n\n"+timeNow.strftime('%H : %M : %S'))
		if op.type == 25 or op.type == 26:
			print (" -> ( SEND MESSAGES & RECEIVED MESSAGES )")
			msg = op.message
			text = msg.text
			msg_id = msg.id
			receiver = msg.to
			sender = msg._from
			if msg.toType == 0:
				if sender != puy.profile.mid:
					to = sender
				else:
					to = receiver
			else:
				to = receiver
			if msg.contentType == 0:
				if text is None:
					return
				else:
				  #pass
					cmd = command(text)
				for text in text.split(" & "):
					if cmd.startswith("help"):
					   puy.sendMessage(to, buggyhelp)
### COMMANDS ###
					elif cmd.startswith("speed"):
						start = time.time()
						puy.sendMessage("u1d174074f386d370eb36f8395258e2a2", ' ')
						elapsed_time = time.time() - start
						took = time.time() - start
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"%.3fms" % (took)+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("@bye"):
					  if msg.toType == 2:
						ginfo = puy.getGroupIdsJoined()
						puy.sendMessage(to, 'See u!')
						puy.leaveGroup(to)
					  else:
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("rerun"):
					  if sender in MOD:
						puy.sendMessage(to,"Preparing for Restart the System!")
						restartBot()
					  else:
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("runtime"):
					  if sender in MOD:
						timeNow = time.time()
						runtime = timeNow - botStart
						runtime = format_timespan(runtime)
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to, "{}".format(str(runtime)+"\n\n"+timeNow.strftime('%H : %M : %S')))
					  else:
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("myinfo"):puy.sendMessage(to,"Hello, {}".format(puy.getContact(sender).displayName+"\n\n{}".format(puy.getContact(sender))))

					elif cmd.startswith("about"):puy.sendMessage(to,"FREE USE BUGGY!\n\nSpecial Thanks To TUHAN YME, ERR0RTEAMS, HELLOWORLD, and the Friends Around Me!")

					elif cmd.startswith("checkalive"):
					  if sender in MOD:
						puy.sendMessage(to,"Hi MOD")
					  else:puy.sendMessage(to,"Hiii!")

					elif msg.text.lower().startswith("getpicture "):
						if 'MENTION' in msg.contentMetadata.keys()!= None:
							names = re.findall(r'@(\w+)', text)
							mention = ast.literal_eval(msg.contentMetadata['MENTION'])
							mentionees = mention['MENTIONEES']
							lists = []
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							for mention in mentionees:
								if mention["M"] not in lists:
									lists.append(mention["M"])
							for ls in lists:
								path = "http://dl.profile.line.naver.jp/" + puy.getContact(ls).pictureStatus
								puy.sendImageWithURL(to, str(path))
								puy.sendMessage(to, "Get Picture at"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif msg.text.lower().startswith("getcover "):
						if puy != None:
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								tz = pytz.timezone("Asia/Jakarta")
								timeNow = datetime.now(tz=tz)
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									path = puy.getProfileCoverURL(ls)
									puy.sendImageWithURL(to, str(path))
									puy.sendMessage(to, "Get Cover at"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif text.lower() == 'infogroup':
					  if msg.toType == 2:
						group = puy.getGroup(to)
						try:
							gCreator = group.creator.displayName
						except:
							gCreator = "Not Found"
						if group.invitee is None:
							gPending = "0"
						else:
							gPending = str(len(group.invitee))
						if group.preventedJoinByTicket == True:
							gQr = "Closed"
							gTicket = "Open"
						else:
							gQr = "Open"
							gTicket = "https://line.me/R/ti/g/{}".format(str(puy.reissueGroupTicket(group.id)))
							path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
						ret_ = "    ( Group Info )"
						ret_ += "\n Nama Group : {}".format(str(group.name))
						ret_ += "\n ID Group : {}".format(group.id)
						ret_ += "\n Pembuat : {}".format(str(gCreator))
						ret_ += "\n Jumlah Member : {}".format(str(len(group.members)))
						ret_ += "\n Jumlah Pending : {}".format(gPending)
						ret_ += "\n Group Qr : {}".format(gQr)
						ret_ += "\n Group Ticket : {}".format(gTicket)
						#ret_ += "\n    [ Group Info ]"
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
						puy.sendImageWithURL(to, path)
					  else:
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif text.lower() == 'groupmemberlist':
						if msg.toType == 2:
							group = puy.getGroup(to)
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							ret_ = "╔══[ Member List ]"
							no = 0 + 1
							for mem in group.members:
								ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
								no += 1
							ret_ += "\n╚══[ Total {} ]".format(str(len(group.members)))
							puy.sendMessage(to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
						else:
						  tz = pytz.timezone("Asia/Jakarta")
						  timeNow = datetime.now(tz=tz)
						  puy.sendMessage(to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

### MEDIA ###
					elif text.lower() == "instauser":
						if sender in MOD:
							sep = text.split(" ")
							search = text.replace(sep[0] + " ","")
							r = requests.get("http://syadnysyz2.herokuapp.com/api/instagram/{}".format(search))
							data = r.json()
							a=""
							a+="Name : "+str(data["graphql"]["user"]["full_name"])
							a+="\nUsername : "+str(data["graphql"]["user"]["username"])
							a+="\nBio : "+str(data["graphql"]["user"]["biography"])
							a+="\nUser Blocked : "+str(data["graphql"]["user"]["blocked_by_viewer"])
							a+="\nURL : "+str(data["graphql"]["user"]["external_url"])
							a+="\nURL link : "+str(data["graphql"]["user"]["external_url_linkshimmed"])
							a+="\nFollowers : "+str(data["graphql"]["user"]["edge_followed_by"]["count"])
							a+="\nFollowing View : "+str(data["graphql"]["user"]["followed_by_viewer"])
							a+="\nFollowed : "+str(data["graphql"]["user"]["edge_follow"]["count"])
							a+="\nFollower View : "+str(data["graphql"]["user"]["follows_viewer"])
							a+="\nChannel  : "+str(data["graphql"]["user"]["has_channel"])
							a+="\nBlocked Viewer : "+str(data["graphql"]["user"]["has_blocked_viewer"])
							a+="\nReal Account : "+str(data["graphql"]["user"]["highlight_reel_count"])
							a+="\nRequest Viewer : "+str(data["graphql"]["user"]["has_requested_viewer"])
							a+="\nUser Id : "+str(data["graphql"]["user"]["id"])
							a+="\nBussines Account : "+str(data["graphql"]["user"]["is_business_account"])
							a+="\nPrivate Account : "+str(data["graphql"]["user"]["is_private"])
							a+="\nVerified : "+str(data["graphql"]["user"]["is_verified"])
							a+="\nFollow Real Account : "+str(data["graphql"]["user"]["edge_mutual_followed_by"]["count"])
							a+="\nPicture url : "+str(data["graphql"]["user"]["profile_pic_url"])
							a+="\nPicture url HD : "+str(data["graphql"]["user"]["profile_pic_url_hd"])
							a+="\nConnected Facebook : "+str(data["graphql"]["user"]["connected_fb_page"])
							a+="\nRequested View : "+str(data["graphql"]["user"]["requested_by_viewer"])
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							puy.sendImageWithURL(to, str(data["graphql"]["user"]["profile_pic_url_hd"]))
							puy.sendMessage(to, a+"\n\n"+timeNow.strftime('%H : %M : %S'))
						else:
						  tz = pytz.timezone("Asia/Jakarta")
						  timeNow = datetime.now(tz=tz)
						  puy.sendMessage(to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif text.lower() == "motivate":
						puy1 = requests.get("https://talaikis.com/api/quotes/random")
						data=puy1.text
						data=json.loads(data)
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to, " 「 Fun 」\nType: Motivasi\n\n" + str(data["quote"])+"\n\n"+timeNow.strftime('%H : %M : %S'))
						print ("Motivate")

					elif text.lower() == "quotes":
						r=requests.get("https://talaikis.com/api/quotes/random")
						data=r.text
						data=json.loads(data)
						hasil = " 「 Fun 」\nType: Random Quotes\n\n"
						hasil += "Genre : " +str(data["cat"])
						hasil += "\n" +str(data["quote"])
						hasil += "\n\nDari : " +str(data["author"])+ " "
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to, str(hasil)+"\n\n"+timeNow.strftime('%H : %M : %S'))
						print ("Quotes")

					elif text.lower() == "creepypasta":
						r=requests.get("http://hipsterjesus.com/api")
						data=r.text
						data=json.loads(data)
						hasil = "     「 Fun 」 \nType: CreepyPasta\n\n"
						hasil += str(data["text"])
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to, str(hasil)+"\n\n"+timeNow.strftime('%H : %M : %S'))
						print ("Creepypasta")
### REMOTE COMMANDS ###
					elif cmd == "list group":
					  if sender in MOD:
						groups = puy.getGroupIdsJoined()
						ret_ = "  - Grouplist -"
						no = 0
						for gid in groups:
							group = puy.getGroup(gid)
							no += 1
							ret_ += "\n (#) {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
						ret_ += "\n - {} Groups -".format(str(len(groups)))
						puy.sendMessage(to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
					  else:
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

				  
					elif cmd.startswith("openlink to"):
						if sender in MOD:
							number = cmd.replace("openlink to","")
							groups = puy.getGroupIdsJoined()
							try:
								group = groups[int(number)-1]
								G = puy.getGroup(group)
								try:
									G.preventedJoinByTicket = False
									puy.updateGroup(G)
									gurl = "https://line.me/R/ti/g/{}".format(str(puy.reissueGroupTicket(G.id)))
									tz = pytz.timezone("Asia/Jakarta")
									timeNow = datetime.now(tz=tz)
								except:
									G.preventedJoinByTicket = False
									puy.updateGroup(G)
									tz = pytz.timezone("Asia/Jakarta")
									timeNow = datetime.now(tz=tz)
									gurl = "https://line.me/R/ti/g/{}".format(str(puy.reissueGroupTicket(G.id)))
								puy.sendMessage(to, "Success Open Join By Ticket\nInGroup : (" + G.name + ")\n  Url : " + gurl+"\n\n"+timeNow.strftime('%H : %M : %S'))
							except Exception as error:
								puy.sendMessage(to, str(error))
						else:
						  tz = pytz.timezone("Asia/Jakarta")
						  timeNow = datetime.now(tz=tz)
						  puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("closelink to"):
						if sender in MOD:
							number = cmd.replace("closelink to","")
							groups = puy.getGroupIdsJoined()
							try:
								group = groups[int(number)-1]
								G = puy.getGroup(group)
								try:
									G.preventedJoinByTicket = True
									puy.updateGroup(G)
									tz = pytz.timezone("Asia/Jakarta")
									timeNow = datetime.now(tz=tz)
								except:
									G.preventedJoinByTicket = True
									puy.updateGroup(G)
									tz = pytz.timezone("Asia/Jakarta")
									timeNow = datetime.now(tz=tz)
								puy.sendMessage(to, "Success Prevented Join By Ticket\nInGroup : (" + G.name + ")"+"\n\n"+timeNow.strftime('%H : %M : %S'))
							except Exception as error:
								puy.sendMessage(to, str(error))
						else:
						  tz = pytz.timezone("Asia/Jakarta")
						  timeNow = datetime.now(tz=tz)
						  puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("memberlist to"):
						if sender in MOD:
							number = cmd.replace("memberlist to","")
							groups = puy.getGroupIdsJoined()
							ret_ = ""
							try:
								group = groups[int(number)-1]
								G = puy.getGroup(group)
								no = 0
								ret_ = " < Member List >"
								for mem in G.members:
									no += 1
									ret_ += "\n " + str(no) + ". " + mem.displayName
									tz = pytz.timezone("Asia/Jakarta")
									timeNow = datetime.now(tz=tz)
								puy.sendMessage(to,"Member in Group : \n"+ str(G.name) + "\n\n" + ret_ + "\n\n - (%i Members) -" % len(G.members)+"\n\n"+timeNow.strftime('%H : %M : %S'))
							except: 
								pass
						else:
						  tz = pytz.timezone("Asia/Jakarta")
						  timeNow = datetime.now(tz=tz)
						  puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))
## SETTINGS ON/OFF ##
					elif text.lower() == 'notif on':
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings['greet']['join']['status'] == True
						puy.sendMessage(to," [ Notify ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
					elif text.lower() == 'notif off':
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings['greet']['join']['status'] = False
						puy.sendMessage(to," [ Notify ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("autoadd on"):
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoAdd"] = True
						puy.sendMessage(to, " [ Auto Add ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
					elif cmd.startswith("autoadd off"):
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoAdd"] = False
						puy.sendMessage(to, " [ Auto Add ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif cmd.startswith("autojoin on"):
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoJoin"] = True
						puy.sendMessage(to, " [ Auto Join ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
					elif cmd.startswith("autojoin off"):
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoJoin"] = False
						puy.sendMessage(to, " [ Auto Join ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

					elif text.lower() == 'autoleave on':
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoLeave"] = True
						puy.sendMessage(to, " [ Auto Leave ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
					elif text.lower() == 'autoleave off':
						tz = pytz.timezone("Asia/Jakarta")
						timeNow = datetime.now(tz=tz)
						settings["autoLeave"] = False
						puy.sendMessage(to, " [ Auto Leave ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

		if op.type == 55:
			print (" -> 55 ( NOTIFY READ MESSAGES )")
			try:
				if op.param1 in read['readPoint']:
					if op.param2 in read['readMember'][op.param1]:
						pass
					else:
						read['readMember'][op.param1] += op.param2
					read['ROM'][op.param1][op.param2] = op.param2
					backupData()
				else:
				   pass
			except:
				pass
	except Exception as error:
		logError(error)

while True:
	try:
		ops = oepoll.singleTrace(count=50)
		if ops is not None:
			for op in ops:
				puyStarted(op)
				oepoll.setRevision(op.revision)
	except Exception as e:
		logError(e)
