# -*- coding: utf-8 -*-
from akad.ttypes import Message, Location
from random import randint
from datetime import datetime, timedelta, date
import json, ntpath, time

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Talk(object):
    isLogin = False
    _messageReq = {}
    _unsendMessageReq = 0

    def __init__(self):
        self.isLogin = True

    """User"""

    @loggedIn
    def acquireEncryptedAccessToken(self, featureType=2):
        return self.talk.acquireEncryptedAccessToken(featureType)

    @loggedIn
    def getProfile(self):
        return self.talk.getProfile()

    @loggedIn
    def getSettings(self):
        return self.talk.getSettings()

    @loggedIn
    def getUserTicket(self):
        return self.talk.getUserTicket()

    @loggedIn
    def generateUserTicket(self):
        try:
            ticket = self.getUserTicket().id
        except:
            self.reissueUserTicket()
            ticket = self.getUserTicket().id
        return ticket

    @loggedIn
    def updateProfile(self, profileObject):
        return self.talk.updateProfile(0, profileObject)

    @loggedIn
    def updateSettings(self, settingObject):
        return self.talk.updateSettings(0, settingObject)

    @loggedIn
    def updateProfileAttribute(self, attrId, value):
        return self.talk.updateProfileAttribute(0, attrId, value)

    @loggedIn
    def updateContactSetting(self, mid, flag, value):
        return self.talk.updateContactSetting(0, mid, flag, value)

    @loggedIn
    def deleteContact(self, mid):
        return self.updateContactSetting(mid, 16, 'True')

    @loggedIn
    def renameContact(self, mid, name):
        return self.updateContactSetting(mid, 2, name)

    @loggedIn
    def addToFavoriteContactMids(self, mid):
        return self.updateContactSetting(mid, 8, 'True')

    @loggedIn
    def addToHiddenContactMids(self, mid):
        return self.updateContactSetting(mid, 4, 'True')

    """Operation"""

    @loggedIn
    def fetchOps(self, localRev, count, globalRev=0, individualRev=0):
        return self.poll.fetchOps(self, localRev, count, globalRev, individualRev)

    @loggedIn
    def fetchOperation(self, revision, count=1):
        return self.poll.fetchOperations(revision, count)

    @loggedIn
    def getLastOpRevision(self):
        return self.poll.getLastOpRevision()

    """Message"""
    def mycmd(self,text,settings):
        cmd = ''
        pesan = text.lower()
        if settings['setKey'] != '':
            if pesan.startswith(settings['setKey']):
                cmd = pesan.replace(settings['setKey']+' ','').replace(settings['setKey'],'')
        else:
            cmd = text
        return cmd

    def command(text):
        pesan = text.lower()
        if settings['setKey']['status']:
            if pesan.startswith(settings['setKey']['key']):
                cmd = pesan.replace(settings['setKey']['key'],'')
            else:
                cmd = 'Undefined command'
        else:
            cmd = text.lower()
        return cmd

    @loggedIn
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def postTemplate(self, to, data=[]):
        data = {
            "access_token": "EyqyXTwh4zMtcfDBwWc3.Ri4/RX6YPvDWVXddSJv8mW.86oJb+T0QwJJ5sGT45lGgn+Cks+C//LKTNC7G4R2ZoU=",
            "line_application": "IOSIPAD",
            "chat_id": to,
            "messages": data
        }
        headers = {
            "Content-Type": "application/json"
        }
        puy = requests.post("http://0.0.0.0:6000/api/sendMessage", headers=headers, json=data)

    @loggedIn
    def sendMessageObject(self, msg):
        to = msg.to
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendLocation(self, to, address, latitude, longitude, phone=None, contentMetadata={}):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = "Location by Hello World"
        msg.contentType, msg.contentMetadata = 0, contentMetadata
        location = Location()
        location.address = address
        location.phone = phone
        location.latitude = float(latitude)
        location.longitude = float(longitude)
        location.title = "Location"
        msg.location = location
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendMessageMusic(self, to, title=None, subText=None, url=None, iconurl=None, contentMetadata={}):
        """
        a : Android
        i : Ios
        """
        self.profile = self.getProfile()
        self.userTicket = self.generateUserTicket()
        title = title if title else 'LINE MUSIC'
        subText = subText if subText else self.profile.displayName
        url = url if url else 'line://ti/p/' + self.userTicket
        iconurl = iconurl if iconurl else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = title
        msg.contentType = 19
        msg.contentMetadata = {
            'text': title,
            'subText': subText,
            'a-installUrl': url,
            'i-installUrl': url,
            'a-linkUri': url,
            'i-linkUri': url,
            'linkUri': url,
            'previewUrl': iconurl,
            'type': 'mt',
            'a-packageName': 'com.spotify.music',
            'countryCode': 'JP',
            'id': 'mt000000000a6b79f9'
        }
        if contentMetadata:
            msg.contentMetadata.update(contentMetadata)
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def generateMessageFooter(self, title=None, link=None, iconlink=None):
        self.profile = self.getProfile()
        self.userTicket = self.generateUserTicket()
        title = title if title else self.profile.displayName
        link = link if link else 'line://ti/p/' + self.userTicket
        iconlink = iconlink if iconlink else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
        return {'AGENT_NAME': title, 'AGENT_LINK': link, 'AGENT_ICON': iconlink}

    @loggedIn
    def sendMessageWithFooter(self, to, text, title=None, link=None, iconlink=None, contentMetadata={}):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType = 0
        msg.contentMetadata = self.generateMessageFooter(title, link, iconlink)
        if contentMetadata:
            msg.contentMetadata.update(contentMetadata)
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendMention(self, to, mid, firstmessage='', lastmessage=''):
        arrData = ""
        text = "%s " %(str(firstmessage))
        arr = []
        mention = "@zeroxyuuki "
        slen = str(len(text))
        elen = str(len(text) + len(mention) - 1)
        arrData = {'S':slen, 'E':elen, 'M':mid}
        arr.append(arrData)
        text += mention + str(lastmessage)
        self.sendMessage(to, text, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

    @loggedIn
    def sendLocationS(self, to, address, latitude, longitude, phone=None, contentMetadata={}):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = "Location By ERROR TEAM"
        msg.contentType, msg.contentMetadata = 0, contentMetadata
        location = Location()
        location.address = address
        location.phone = phone
        location.latitude = float(latitude)
        location.longitude = float(longitude)
        location.title = "Location"
        msg.location = location
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def setsticker(self,settings,msg):
        #msg.text = self.lower(msg.text,settings)
        separate = msg.text.lower().split(" ")
        text = msg.text.lower().replace(separate[0]+" "+separate[1]+" ","")
        settings["Sticker"][text] = '{}'.format(text)
        settings["Img"] = '{}'.format(text)
        settings["Addsticker"] = True
        self.sendMessage(msg.to, " 「 Sticker 」\nSend the sticker")

    @loggedIn
    def autoredanu(self,msg,settings,kuciyose):
        if msg.toType == 0:
            if msg._from != self.getProfile().mid:
                to = msg._from
            else:
                to = msg.to
        else:
            to = msg.to
        soloi = threading.Thread(target=self.limitlimit, args=(to,kuciyose,)).start()
        if settings["autoread1"] == True:self.sendChatChecked(msg._from,msg.id)
        #if settings["autoread2"] == True:self.sendChatChecked(msg.to,msg.id)
        try:
            if settings['tos'][to]['setset'] == True:
                if to not in kuciyose['tos']:kuciyose['tos'][to] = {}
                kuciyose['tos'][to]['setset'] = True
                kuciyose['tos'][to][msg.id] = {'msg':msg}
                if msg.contentType == 1:
                    try:
                        if msg.contentMetadata != {}:path = self.downloadObjectMsg(msg.id,'path','dataSeen/%s.gif' % msg.id,True);kuciyose['tos'][to][msg.id]['path'] = path
                    except:path = self.downloadObjectMsg(msg.id);kuciyose['tos'][to][msg.id]['path'] = path
                if msg.contentType == 2 or msg.contentType == 3 or msg.contentType == 14:path = self.downloadObjectMsg(msg.id);kuciyose['tos'][to][msg.id]['path'] = path
            else:kuciyose['tos'][to]['setset'] = False
        except:
            e = traceback.format_exc()
            settings['tos'][to] = {}
        if msg._from in settings["target"] and settings["status"] == True:
            if msg.contentType == 4:
                return
            if msg.text is not None:
                settings['GN'] = msg
                self.sendMessages(msg)
                self.forward(msg)
            else:
                try:return self.sendMessages(msg)
                except:
                    a = self.shop.getProduct(packageID=int(msg.contentMetadata['STKPKGID']), language='ID', country='ID')
                    if a.hasAnimation == True:
                        path = self.downloadFileURL('https://stickershop.line-scdn.net/stickershop/v1/sticker/'+str(msg.contentMetadata['STKID'])+'/IOS/sticker_animation@2x.png', 'path','sticker.png')
                        a=subprocess.getoutput('apng2gif sticker.png')
                        return threading.Thread(target=self.sendGIF, args=(to,'sticker.gif',)).start()
                    self.sendImageWithURL(to,'https://stickershop.line-scdn.net/stickershop/v1/sticker/'+str(msg.contentMetadata['STKID'])+'/ANDROID/sticker.png')

    @loggedIn
    def fancynamehelp(self,settings,dd):
        if 'timer' not in settings['talkban']:
            settings['talkban']['timer'] = 60
        if 'name' not in settings['talkban']:
            settings['talkban']['name'] = self.getProfile().displayName
        try:
            if settings['timeline'] == False:settings['timeline'] = []
        except:pass
        if settings['ChangeCover'] == True:d = '\n│State: ON\n│Timer: {}second'.format(settings['talkban']['timer'])
        else:d = '\n│State: OFF'
        if settings["timeline"] == []:
            a='None'
        else:
            a = ""
            for b in settings["timeline"]:
                a+= '\n│'+b
        return "┌───「 Fancy Name 」───────\n│Backup Name: "+dd+"\n│FancyName Set:"+a+d+"\n│    | Command |  \n│Set Name\n│  Key: "+settings["setkey"].title()+" fancyname set [enter|name]\n│Set Time\n│  Key: "+settings["setkey"].title()+" fancyname on [time]\n└────────────"

    @loggedIn
    def setfancy(self,msg,settings):
        msg.text = self.command(msg.text,settings)
        settings['timeline'] = []
        settings['timeline'] = msg.text.split("\n")[1:]
        d = ' 「 Fancy Name 」\nFancy Name Set to:'
        for a in settings['timeline']:
            d+= '\n{}'.format(a)
        self.sendMessage(msg.to,'{}'.format(d))

    @loggedIn
    def image_search(self, query):
        query = query.replace(' ', "%20")
        url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs=isz:l&q=" + query
        mozhdr = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
        req = requests.get(url, headers = mozhdr)
        soupeddata = BeautifulSoup(req.content , "lxml")
        images = soupeddata.find_all("div", {"class": "rg_meta notranslate"})
        aa = random.randint(0,len(images))
        try:
            images = json.loads(images[aa].text)
            return images
        except Exception as e:return e
    def imagegoogle(self,msg,settings):
        msg.text = self.mycmd(msg.text,settings)
        to = msg.to
        data = self.image_search(self.adityasplittext(msg.text))
        try:
            a = data['ou']
            if '.gif' in a:
                return self.sendGIFWithURL(to,a)
            return self.sendImageWithURL(to,a,'Google Image')
            self.sendMention(to,' 「 Image 」\nInfo: Hy @! I get num #{} from #100'.format(aa+1),'',[msg._from])
        except Exception as e:
            self.sendMessage(to,' 「 Error 」\nStatus:\n{}'.format(e))

    @loggedIn
    def fancyfancy(self,settings):
                if settings['ChangeCover'] == True:
                        try:
                            if time.time() - settings['talkban']['time'] >= settings['talkban']['timer']:
                                a = random.randint(0,len(settings['timeline']))
                                self.updateProfileAttribute(2, settings['timeline'][a])
                                settings['talkban']['time'] = time.time()
                                settings['talkban']['timer'] = settings['talkban']['timer']
                        except:pass

    @loggedIn
    def autoreadon1(self,settings):
        if settings['autoread1'] == True:
            msgs=" 「 Auto Read 」\nAuto Read Personal already Enable♪\nNote: Auto Read message is not affected♪"
        else:
            msgs=" 「 Auto Read 」\nAuto Read Personal set to Enable♪\nNote: Auto Read message is not affected♪"
            settings['autoread1']= False
        return msgs

    def setImageS(self,settings,msg):
        msg.text = self.mycmd(msg.text,settings)
        separate = msg.text.lower().split(" ")
        text = msg.text.lower().replace(separate[0]+" "+separate[1]+" ","")
        settings["Images"][text] = 'dataSeen/{}.jpg'.format(text)
        settings["Img"] = '{}'.format(text)
        settings["Addimage"] = True
        self.sendMessage(msg.to, " 「 Picture 」\nSend a Picture to save")

    @loggedIn
    def stacks(self,to):
        start = time.time()
        a = [self.sendMessage(to,"- Taken: %.10f" % (time.time() - start)) for a in range(50)]

    def adityasplittext(self,text,lp=''):
        separate = text.split(" ")
        if lp == '':adalah = text.replace(separate[0]+" ","")
        elif lp == 's':adalah = text.replace(separate[0]+" "+separate[1]+" ","")
        else:adalah = text.replace(separate[0]+" "+separate[1]+" "+separate[2]+" ","")
        return adalah

    @loggedIn
    def debug(self):
        get_profile_time_start = time.time()
        get_profile = self.getProfile()
        get_profile_time = time.time() - get_profile_time_start
        get_group_time_start = time.time()
        get_group = self.getGroupIdsJoined()
        get_group_time = time.time() - get_group_time_start
        get_contact_time_start = time.time()
        get_contact = self.getContact(get_profile.mid)
        get_contact_time = time.time() - get_contact_time_start
        return " 「 Debug 」\nType:\n - Get Profile\n   %.10f\n - Get Contact\n   %.10f\n - Get Group\n   %.10f" % (get_profile_time/2,get_contact_time/2,get_group_time/2)

    def listsimpanan(self,text,data={}):
        if data == {}:
            msgs = " 「 {} List 」\nNo {}".format(text,text)
        else:
            no=0
            msgs=" 「 {} List 」\n{} List:".format(text,text)
            for a in data:
                no+=1
                if no % 2 == 0:msgs+="  %i. %s" % (no, a)
                else:msgs+="\n%i. %s" % (no, a)
            msgs+="\n\nTotal {} List: {}".format(text,len(data))
        return msgs

    @loggedIn
    def GroupPost(self,msg,settings):
        to = msg.to
        data = self.getGroupPost(to)
        msg.text = self.mycmd(msg.text,settings)
        if msg.text.lower() == 'get note':
            if data['result'] != []:
                try:
                    no = 0
                    b = []
                    a = " 「 Groups 」\nType: Get Note"
                    for i in data['result']['feeds']:
                        b.append(i['post']['userInfo']['writerMid'])
                        try:
                            for aasd in i['post']['contents']['textMeta']:b.append(aasd['mid'])
                        except:pass
                        no += 1
                        gtime = i['post']['postInfo']['createdTime']
                        try:g = i['post']['contents']['text'].replace('@','@!')
                        except:g="None"
                        if no == 1:sddd = '\n'
                        else:sddd = '\n\n'
                        a +="{}{}. Penulis : @!\nDescription: {}\nTotal Like: {}\nCreated at: {}".format(sddd,no,g,i['post']['postInfo']['likeCount'],humanize.naturaltime(datetime.fromtimestamp(gtime/1000)))
                    a +="Status: Success Get "+str(data['result']['homeInfo']['postCount'])+" Note"
                    self.sendMention(to,a,'',b)
                except Exception as e:
                    return self.sendMessage(to,"「 Auto Respond 」\n"+str(e))
        if msg.text.lower().startswith('get note '):
            try:
                music = data['result']['feeds'][int(msg.text.split(' ')[2]) - 1]
                b = [music['post']['userInfo']['writerMid']]
                try:
                    for a in music['post']['contents']['textMeta']:b.append(a['mid'])
                except:pass
                try:
                    g= "\n\nDescription:\n"+str(music['post']['contents']['text'].replace('@','@!'))
                except:
                    g=""
                a="\n   Total Like: "+str(music['post']['postInfo']['likeCount'])
                a +="\n   Total Comment: "+str(music['post']['postInfo']['commentCount'])
                gtime = music['post']['postInfo']['createdTime']
                a +="\n   Created at: "+str(humanize.naturaltime(datetime.fromtimestamp(gtime/1000)))
                a += g
                zx = ""
                zxc = " 「 Groups 」\nType: Get Note\n   Penulis : @!"+a
                try:
                    self.sendMention(to,zxc,'',b)
                except Exception as e:
                    self.sendMessage(to, str(e))
                try:
                    for c in music['post']['contents']['media']:
                        params = {'userMid': self.getProfile().mid, 'oid': c['objectId']}
                        path = self.server.urlEncode(self.server.LINE_OBS_DOMAIN, '/myhome/h/download.nhn', params)
                        if 'PHOTO' in c['type']:
                            try:
                                self.sendImageWithURL(to,path,'POST')
                            except:pass
                        else:
                            pass
                        if 'VIDEO' in c['type']:
                            try:
                                self.sendVideoWithURL(to,path)
                            except:pass
                        else:
                            pass
                except:
                    pass
            except Exception as e:
                return self.sendMessage(to,"「 Auto Respond 」\n"+str(e))

    @loggedIn
    def findcont(self,msg):
        if 'MENTION' in msg.contentMetadata.keys()!=None:
            key = eval(msg.contentMetadata["MENTION"])
            key1 = key["MENTIONEES"][0]["M"]
            a = self.getGroupIdsJoined();i = self.getGroups(a)
            az = self.getContact(key1)
            c = []
            for h in i:
                g = [c.append(h.name[0:20]+',.s/'+str(len(h.members))) for d in h.members if key1 in d.mid]
            h = "╭「 {} 」─".format(az.displayName)
            no=0
            for group in c:
                no+=1
                h+= "\n│"+"\n│{}. {} | {}".format(no, group.split(',.s/')[0], group.split(',.s/')[1])
            self.sendMessage(msg.to,h+"\n│\n╰─「 {} Grup yang sama」".format(len(c)))

    @loggedIn
    def sendMentionV2(self, to, text="", mids=[], isUnicode=False):
        arrData = ""
        arr = []
        mention = "@zeroxyuuki "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            unicode = ""
            if isUnicode:
                for mid in mids:
                    unicode += str(texts[mids.index(mid)].encode('unicode-escape'))
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx) if unicode == textx else len(textx) + unicode.count('U0')
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            else:
                for mid in mids:
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx)
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            textx += str(texts[len(mids)])
        else:
            raise Exception("Invalid mention position")
        self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

    """ Usage:
        @to Integer
        @text String
        @dataMid List of user Mid
    """
    @loggedIn
    def sendMessageWithMention(self, to, text='', dataMid=[]):
        arr = []
        list_text=''
        if '[list]' in text.lower():
            i=0
            for l in dataMid:
                list_text+='\n@[list-'+str(i)+']'
                i=i+1
            text=text.replace('[list]', list_text)
        elif '[list-' in text.lower():
            text=text
        else:
            i=0
            for l in dataMid:
                list_text+=' @[list-'+str(i)+']'
                i=i+1
            text=text+list_text
        i=0
        for l in dataMid:
            mid=l
            name='@[list-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int(ln_text.index(name))
                line_e=(int(line_s)+int(len(name)))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        return self.sendMessage(to, text, contentMetadata)

    @loggedIn
    def sendSticker(self, to, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendMessage(to, '', contentMetadata, 7)
        
    @loggedIn
    def sendContact(self, to, mid):
        contentMetadata = {'mid': mid}
        return self.sendMessage(to, '', contentMetadata, 13)

    @loggedIn
    def sendGift(self, to, productId, productType):
        if productType not in ['theme','sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendMessage(to, '', contentMetadata, 9)

    @loggedIn
    def sendMessageAwaitCommit(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessageAwaitCommit(self._messageReq[to], msg)

    @loggedIn
    def unsendMessage(self, messageId, msg_id):
        self._unsendMessageReq += 1
        return self.talk.unsendMessage(self._unsendMessageReq, messageId)

    @loggedIn
    def requestResendMessage(self, senderMid, messageId):
        return self.talk.requestResendMessage(0, senderMid, messageId)

    @loggedIn
    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    @loggedIn
    def removeMessage(self, messageId):
        return self.talk.removeMessage(messageId)
    
    @loggedIn
    def removeAllMessages(self, lastMessageId):
        return self.talk.removeAllMessages(0, lastMessageId)

    @loggedIn
    def removeMessageFromMyHome(self, messageId):
        return self.talk.removeMessageFromMyHome(messageId)

    @loggedIn
    def destroyMessage(self, chatId, messageId):
        return self.talk.destroyMessage(0, chatId, messageId, sessionId)
    
    @loggedIn
    def sendChatChecked(self, consumer, messageId):
        return self.talk.sendChatChecked(0, consumer, messageId)

    @loggedIn
    def sendEvent(self, messageObject):
        return self.talk.sendEvent(0, messageObject)

    @loggedIn
    def getLastReadMessageIds(self, chatId):
        return self.talk.getLastReadMessageIds(0, chatId)

    @loggedIn
    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    """Object"""

    @loggedIn
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)

    @loggedIn
    def sendImageWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage(to, path)

    @loggedIn
    def sendGIF(self, to, path):
        return self.uploadObjTalk(path=path, type='gif', returnAs='bool', to=to)

    @loggedIn
    def sendGIFWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGIF(to, path)

    @loggedIn
    def sendVideo(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2).id
        return self.uploadObjTalk(path=path, type='video', returnAs='bool', objId=objectId)

    @loggedIn
    def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendVideo(to, path)

    @loggedIn
    def sendAudio(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 3).id
        return self.uploadObjTalk(path=path, type='audio', returnAs='bool', objId=objectId)

    @loggedIn
    def sendAudioWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendAudio(to, path)

    @loggedIn
    def sendFile(self, to, path, file_name=''):
        if file_name == '':
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(file_size)}, contentType = 14).id
        return self.uploadObjTalk(path=path, type='file', returnAs='bool', objId=objectId, name=file_name)

    @loggedIn
    def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendFile(to, path, fileName)

    """Contact"""
        
    @loggedIn
    def blockContact(self, mid):
        return self.talk.blockContact(0, mid)

    @loggedIn
    def unblockContact(self, mid):
        return self.talk.unblockContact(0, mid)

    @loggedIn
    def findAndAddContactByMetaTag(self, userid, reference):
        return self.talk.findAndAddContactByMetaTag(0, userid, reference)

    @loggedIn
    def findAndAddContactsByMid(self, mid):
        return self.talk.findAndAddContactsByMid(0, mid, 0, '')

    @loggedIn
    def findAndAddContactsByEmail(self, emails=[]):
        return self.talk.findAndAddContactsByEmail(0, emails)

    @loggedIn
    def findAndAddContactsByUserid(self, userid):
        return self.talk.findAndAddContactsByUserid(0, userid)

    @loggedIn
    def findContactsByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    @loggedIn
    def findContactByTicket(self, ticketId):
        return self.talk.findContactByUserTicket(ticketId)

    @loggedIn
    def getAllContactIds(self):
        return self.talk.getAllContactIds()

    @loggedIn
    def getBlockedContactIds(self):
        return self.talk.getBlockedContactIds()

    @loggedIn
    def getContact(self, mid):
        return self.talk.getContact(mid)

    @loggedIn
    def getContacts(self, midlist):
        return self.talk.getContacts(midlist)

    @loggedIn
    def getFavoriteMids(self):
        return self.talk.getFavoriteMids()

    @loggedIn
    def getHiddenContactMids(self):
        return self.talk.getHiddenContactMids()

    @loggedIn
    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)

    @loggedIn
    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)

    @loggedIn
    def getContactWithFriendRequestStatus(self, id):
        return self.talk.getContactWithFriendRequestStatus(id)

    @loggedIn
    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.talk.reissueUserTicket(expirationTime, maxUseCount)
    
    @loggedIn
    def cloneContactProfile(self, mid, channel):
        contact = self.getContact(mid)
        path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
        path = self.downloadFileURL(path)
        self.updateProfilePicture(path)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        if channel.getProfileCoverId(mid) is not None:
            channel.updateProfileCoverById(channel.getProfileCoverId(mid))
        return self.updateProfile(profile)

    """Group"""

    @loggedIn
    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)

    @loggedIn
    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.talk.getChatRoomAnnouncements(chatRoomMid)

    @loggedIn
    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.talk.createChatRoomAnnouncement(0, chatRoomMid, type, contents)

    @loggedIn
    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    @loggedIn
    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    
    @loggedIn
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)

    @loggedIn
    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(0, groupId)

    @loggedIn
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @loggedIn
    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(0, groupId, contactIds)

    @loggedIn
    def createGroup(self, name, midlist):
        return self.talk.createGroup(0, name, midlist)

    @loggedIn
    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)

    @loggedIn
    def getGroups(self, groupIds):
        return self.talk.getGroups(groupIds)

    @loggedIn
    def getGroupsV2(self, groupIds):
        return self.talk.getGroupsV2(groupIds)

    @loggedIn
    def getCompactGroup(self, groupId):
        return self.talk.getCompactGroup(groupId)

    @loggedIn
    def getCompactRoom(self, roomId):
        return self.talk.getCompactRoom(roomId)

    @loggedIn
    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    @loggedIn
    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()

    @loggedIn
    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()

    @loggedIn
    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    @loggedIn
    def inviteIntoGroup(self, groupId, midlist):
        return self.talk.inviteIntoGroup(0, groupId, midlist)

    @loggedIn
    def kickoutFromGroup(self, groupId, midlist):
        return self.talk.kickoutFromGroup(0, groupId, midlist)

    @loggedIn
    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(0, groupId)

    @loggedIn
    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(0, groupId)

    @loggedIn
    def reissueGroupTicket(self, groupId):
        return self.talk.reissueGroupTicket(groupId)

    @loggedIn
    def updateGroup(self, groupObject):
        return self.talk.updateGroup(0, groupObject)

    """Room"""

    @loggedIn
    def createRoom(self, midlist):
        return self.talk.createRoom(0, midlist)

    @loggedIn
    def getRoom(self, roomId):
        return self.talk.getRoom(roomId)

    @loggedIn
    def inviteIntoRoom(self, roomId, midlist):
        return self.talk.inviteIntoRoom(0, roomId, midlist)

    @loggedIn
    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(0, roomId)

    """Call"""
        
    @loggedIn
    def acquireCallTalkRoute(self, to):
        return self.talk.acquireCallRoute(to)
    
    """Report"""

    @loggedIn
    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)
        
    @loggedIn
    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)
