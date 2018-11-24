# -*- coding: utf-8 -*-

from linepy import *
from akad.ttypes import Message
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, shutil
from subprocess import check_output
from gtts import gTTS
from googletrans import Translator

botStart = time.time()

puy = LINE("Ez9NXV49sfJZbVO95dD4.MBrD3kv6F5JVe6KSmRknra.NGNwyeH3lrOR4YwjO8/+OkkxoF2emJPLHj11Ytd2bG4=")
#puy = LINE("mpuy18@messagea.gq","Muhamad18")
puy.log("Your Auth Token : \n" + str(puy.authToken))

readOpen = codecs.open("read.json","r","utf-8")
settingOpen = codecs.open("setting.json","r","utf-8")

puyMID = puy.profile
puyProfile = puy.getProfile()
puySettings = puy.getSettings()
oepoll = OEPoll(puy)
call = puy
read = json.load(readOpen)
settings = json.load(settingOpen)
admin = ["uac8e3eaf1eb2a55770bf10c3b2357c33","u99b45ddca57a7f98ef13a92c32b28d44"]

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
Closelink to (num)"""

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
    pesan = text.lower()
    if pesan.startswith(settings["keyCommand"]):
        cmd = pesan.replace(settings["keyCommand"],"")
    else:
        cmd = "command"
    return cmd

def waktu(to):
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    day = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis","Jumat", "Sabtu"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    hr = timeNow.strftime("%A")
    bln = timeNow.strftime("%m")
    #puy.sendMessage(to, str(timeNow.strftime('%H : %M : %S')))
    puy.sendMessage(to, "\n\n"+"\n\n"+timeNow.strftime('%H : %M : %S'))

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
                       puy.sendReplyMessage(msg_id,to, buggyhelp+str(waktu))
### COMMANDS ###
                    elif cmd.startswith("speed"):
                        start = time.time()
                        puy.sendMessage("u1d174074f386d370eb36f8395258e2a2", ' ')
                        elapsed_time = time.time() - start
                        took = time.time() - start
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to,"%.3fms" % (took)+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("@bye"):
                      if msg.toType == 2:
                        ginfo = puy.getGroupIdsJoined()
                        puy.sendReplyMessage(msg_id,to, 'See u!')
                        puy.leaveGroup(to)
                      else:
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("rerun"):
                      if sender in admin:
                        puy.sendReplyMessage(msg_id,to,"Preparing for Restart the System!")
                        restartBot()
                      else:
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("runtime"):
                      if sender in admin:
                        timeNow = time.time()
                        runtime = timeNow - botStart
                        runtime = format_timespan(runtime)
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to, "{}".format(str(runtime)+"\n\n"+timeNow.strftime('%H : %M : %S')))
                      else:
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendMessage(to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("myinfo"):puy.sendReplyMessage(msg_id,to,"Hello, {}".format(puy.getContact(sender).displayName+"\n\n{}".format(puy.getContact(sender))))

                    elif cmd.startswith("about"):puy.sendReplyMessage(msg_id,to,"FREE USE BUGGY!\n\nSpecial Thanks To TUHAN YME, ERR0RTEAMS, HELLOWORLD, and the Friends Around Me!")

                    elif cmd.startswith("checkalive"):
                      if sender in admin:
                        puy.sendReplyMessage(msg_id,to,"Hi Admin")
                      else:puy.sendReplyMessage(msg_id,to,"Hiii!")

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
                                puy.sendReplyImageWithURL(msg_id,to, str(path))
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
                                    puy.sendReplyImageWithURL(msg_id,to, str(path))
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
                        puy.sendReplyMessage(msg_id,to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
                        puy.sendReplyImageWithURL(msg_id,to, path)
                      else:
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

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
                            puy.sendReplyMessage(msg_id,to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
                        else:
                          tz = pytz.timezone("Asia/Jakarta")
                          timeNow = datetime.now(tz=tz)
                          puy.sendReplyMessage(msg_id,to,"Only Work in Groups!"+"\n\n"+timeNow.strftime('%H : %M : %S'))
### REMOTE COMMANDS ###

                    elif cmd == "list group":
                      if sender in admin:
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
                        puy.sendReplyMessage(msg_id,to, str(ret_)+"\n\n"+timeNow.strftime('%H : %M : %S'))
                      else:
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        puy.sendReplyMessage(msg_id,to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                  
                    elif cmd.startswith("openlink to"):
                        if sender in admin:
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
                          puy.sendReplyMessage(msg_id,to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("closelink to"):
                        if sender in admin:
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
                          puy.sendReplyMessage(msg_id,to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("memberlist to"):
                        if sender in admin:
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
                          puy.sendReplyMessage(msg_id,to,"Command Denied!"+"\n\n"+timeNow.strftime('%H : %M : %S'))
## SETTINGS ON/OFF ##
                    elif text.lower() == 'notif on':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings['greet']['join']['status'] == True
                        puy.sendReplyMessage(msg_id,to," [ Notify ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
                    elif text.lower() == 'notif off':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings['greet']['join']['status'] = False
                        puy.sendReplyMessage(msg_id,to," [ Notify ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("autoadd on"):
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoAdd"] = True
                        puy.sendReplyMessage(msg_id,to, " [ Auto Add ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
                    elif cmd.startswith("autoadd off"):
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoAdd"] = False
                        puy.sendReplyMessage(msg_id,to, " [ Auto Add ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif cmd.startswith("autojoin on"):
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoJoin"] = True
                        puy.sendReplyMessage(msg_id,to, " [ Auto Join ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
                    elif cmd.startswith("autojoin off"):
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoJoin"] = False
                        puy.sendReplyMessage(msg_id,to, " [ Auto Join ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

                    elif text.lower() == 'autoleave on':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoLeave"] = True
                        puy.sendReplyMessage(msg_id,to, " [ Auto Leave ]\n Now Active."+"\n\n"+timeNow.strftime('%H : %M : %S'))
                    elif text.lower() == 'autoleave off':
                        tz = pytz.timezone("Asia/Jakarta")
                        timeNow = datetime.now(tz=tz)
                        settings["autoLeave"] = False
                        puy.sendReplyMessage(msg_id,to, " [ Auto Leave ]\n Now UnActive."+"\n\n"+timeNow.strftime('%H : %M : %S'))

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