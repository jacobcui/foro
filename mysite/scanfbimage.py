import os, time, sys
from mysite.models import FbImage
from mysite.utils import utils

oUtils = utils()
sFbImageDir = oUtils.getImageDirectory('fb')
aImgList = oUtils.getFileList(sFbImageDir)

limit = 200 # unlimited when greater than 100
iProcessedCnt = 0;
iTotalCnt = len(aImgList)

for sName in aImgList:
    if limit <= 0:
        break
    if limit < 100:
        iimit = limit - 1

    iProcessedCnt = iProcessedCnt + 1
    oUtils.drawProgressBar(1.0 * iProcessedCnt / iTotalCnt )

    (facebookId, sep, suffix) = sName.partition('.')
    try:
        iFacebookId = int(facebookId)
    except ValueError:
        print "\n", str(facebookId), " is invalid, skipping"
        continue
    if oUtils.doesExists(facebookId):
        continue

    sFile = sFbImageDir + sName

    try:
        iFileSize = os.stat(sFile).st_size
        print "%s %d %d" % (sFile, oUtils.num(facebookId), iFileSize)

        fbImg = FbImage(
            facebookid = facebookId,
            name = sName,
            size = iFileSize
            )
        fbImg.save()
    except os.error:
        print "File %s doesn't exists!" % sFile
    

print ""
sys.exit()
