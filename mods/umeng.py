#coding=utf-8
import sys
from umessage.pushclient import PushClient
from umessage.androidpush import *
from umessage.iospush import *
from umessage.errorcodes import APIServerErrorCode
from config import UMENG_APPKEY
from config import UMENG_SECRET
from datetime import datetime

#注意andorid和ios是不同的appkey和appMasterSecret。 在不同需求下换成各自的appkey。
appKey = UMENG_APPKEY
appMasterSecret = UMENG_SECRET
# 安卓客户端需要注意这部分的activity解析，厂商通道在app关闭的时候，收到推送使用这个配置
# activityAfter='com.xxx.xxx.ui.activity.UmengPushHelperActivity'
custom='xxx' #如果使用了extraKey解析，custom可以忽略

def sendAndroidBroadcast(title, text):
    broadcast = AndroidBroadcast(appKey, appMasterSecret)
    broadcast.setTicker('不知道是啥')
    broadcast.setTitle(title)
    broadcast.setText(text)
    # broadcast.goAppAfterOpen(activityAfter);
    # broadcast.goCustomAfterOpen(custom);
    broadcast.setDisplayType(AndroidNotification.DisplayType.NOTIFICATION)
    # 正式环境
    broadcast.setProductionMode()
    # broadcast.setTestMode()
    # Set customized fields
    broadcast.serExtra({'不知道是什么': '不知道是什么'})

    broadcast.setMiPush('true')
    # broadcast.setMiActivity(activityAfter)

    pushClient = PushClient()
    r = pushClient.send(broadcast)
    return r


def send_message(db_info):
    if int(db_info['basic']['year']) >= datetime.now().year - 1:
        pre_title = '上新'
    else:
        pre_title = '上旧'
    title = '{}：[{}]{}（{}）  {}'.format(pre_title, db_info['basic']['_type'],db_info['basic']['title'],db_info['basic']['year'],db_info['basic']['douban_rating'])
    content = db_info['basic']['intro']
    r = sendAndroidBroadcast(title,content)
    return r