
import re
import os,sys,random,string
from copy import copy
import xml.etree.ElementTree as ET
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Max, Min
from django.conf import settings

from mysite.models import FbImage,  userfile

class utils(object):
    queryFbImage = QuerySet(model=FbImage)
    allFbImageCount = FbImage.objects.count()
    allFbImage = FbImage.objects.all()
    
    dirSettings = settings.STATICFILES_DIRS 

    userfileQuery = QuerySet(model=userfile)
            
    def getRandomString(self, size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(size))

    def getRandomSet(self, iCnt):
        iCnt = int(iCnt)
        iTotalCnt = len(self.allFbImage)
        if iTotalCnt < 2:
            iTotalCnt = 2
        #if iCnt < 0 or iCnt > iTotalCnt:
        #    iCnt = iTotalCnt
        randomSet = []
        for i in range(iCnt):
            randId = random.randint(0, iTotalCnt - 2)
            try:
                randomSet.append(self.allFbImage.filter(pk=randId)[0])
            except IndexError:
                continue
        return copy(randomSet)

    def getMaxFbId(self):
        return self.allFbImage.aggregate(Max('facebookid'))['facebookid__max']

    def getMinFbId(self):
        return self.allFbImage.aggregate(Min('facebookid'))['facebookid__min']
    
    def doesExists(self, facebookId):
        self.facebookId = facebookId
        try:
            if self.queryFbImage.filter(facebookid=facebookId).exists():
                return True
            else:
                return False
        except ValueError:
            print facebookId
            print " is not valid"
            return False
            
    def getImageDirectory(self, subDirectory = ""):
        for s in self.dirSettings:
            if s[0] == 'image':
                return s[1] + subDirectory + "/"
        return ""

    def getFileDirectory(self, subDirectory = ""):
        for s in self.dirSettings:
            if s[0] == 'file':
                return s[1] + str(subDirectory) + "/"
        return ""

    def getPanoviewDirectory(self, subDirectory = ""):
        for s in self.dirSettings:
            if s[0] == 'panoview':
                return s[1] + str(subDirectory) + "/"
        return ""

    def getPanoviewSceneXML(self, username, textid):
        return self.getPanoviewDirectory("%s/%s" % (username, textid)) + "scenes.xml"

    def getPanoviewFileDirectory(self, username, textid, subDirectory = ""):
        return self.getPanoviewDirectory("%s/%s" % (username, textid)) + subDirectory
        
    def getFileList(self, sDirectory):
        aFileList = []
        oDir = os.listdir(sDirectory)
        for f in oDir:
            aFileList.append(f)
        return aFileList

    def num (self, s):
        try:
            return int(s)
        except exceptions.ValueError:
            return float(s)

    def drawProgressBar(self, percent, barLen = 20):
        sys.stdout.write("\r")
        progress = ""
        for i in range(barLen):
            if i < int(barLen * percent):
                progress += "="
            else:
                progress += " "
        sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
        sys.stdout.flush()

    def getTempUserId(self):
        return 5555

    def getUserFileByName(self, userId, fileName):
        if fileName == "":
            userfileSet = self.userfileQuery.filter(userid = userId)
        else:
            userfileSet = self.userfileQuery.filter(userid = userId, filename = fileName)

        if len(userfileSet) == 0:
            return None
        return userfileSet
    ## fileSize: -1 means not set yet
    ## validTime: 1 means 1 hour, -1 means forever, 0 means in memory
    def saveUserFileByName(self, userId, fileName, fileRelPath):
        ## add validtime handler by userid and appkey
        validTime = 1 # 1 hour by default
        directory = self.getFileDirectory(userId)

        userId = int(userId)
        fullPath = "%s%s" % (directory, fileName)
        try:
            fileSize = os.path.getsize(fullPath)
        except OSError:
            fileSize = -1

        userFile = userfile(
                userid= userId,
                filename= fileName,
                filepath= fileRelPath,
                filesize = fileSize,
                validtime = validTime,
                )

        userFile.save()
        return 0

    def isInOption(self, options, option):
        return re.search(option, options)
            
if __name__ == '__main__':
    oUtils = utils()
    tempUserId = oUtils.getTempUserId()

    appKeyQuery = QuerySet(model=appkey)
    if not appKeyQuery.filter(userid = tempUserId).exists():
        appKey = appkey(
            userid = tempUserId,
            appkey = 'QCxCQ'
            )
        appKey.save()
            

    print oUtils.getAppKey(1);
    print oUtils.getAppKey(2);
    print oUtils.getAppKey(tempUserId);
