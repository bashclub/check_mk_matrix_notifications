#!/usr/bin/env python3

import json
import os
import random
import string
import sys
import urllib.request

MATRIXHOST = os.environ["NOTIFY_PARAMETER_1"]
MATRIXTOKEN = os.environ["NOTIFY_PARAMETER_2"]
MATRIXROOM = os.environ["NOTIFY_PARAMETER_3"]

data = {
    "TS": os.environ["NOTIFY_SHORTDATETIME"],

    # Host related info.
    "HOST": os.environ["NOTIFY_HOSTNAME"],
    "HOSTADDR": os.environ["NOTIFY_HOSTADDRESS"],
    "HOSTSTATE": os.environ["NOTIFY_HOSTSTATE"],
    "HOSTSTATEPREVIOUS": os.environ["NOTIFY_LASTHOSTSTATE"],
    "HOSTSTATECOUNT": os.environ["NOTIFY_HOSTNOTIFICATIONNUMBER"],
    "HOSTOUTPUT": os.environ["NOTIFY_HOSTOUTPUT"],

    # Service related info.
    "SERVICE": os.environ["NOTIFY_SERVICEDESC"],
    "SERVICESTATE": os.environ["NOTIFY_SERVICESTATE"],
    "SERVICESTATEPREVIOUS": os.environ["NOTIFY_LASTSERVICESTATE"],
    "SERVICESTATECOUNT": os.environ["NOTIFY_SERVICENOTIFICATIONNUMBER"],
    "SERVICEOUTPUT": os.environ["NOTIFY_SERVICEOUTPUT"]
}

servicemessage = '''Service <b>{SERVICE}</b> at <b>{HOST}</b> ({HOSTADDR}) | TS: {TS} | STATE: <b>{SERVICESTATE}</b>
<br>{SERVICEOUTPUT}<br>'''

hostmessage = '''Host <b>{HOST}</b> ({HOSTADDR}) | TS: {TS} | STATE: <b>{HOSTSTATE}</b>
<br>{HOSTOUTPUT}<br>'''

message = ""

print(data)

# Checking host status first.
if (data["HOSTSTATE"] != data["HOSTSTATEPREVIOUS"] or data["HOSTSTATECOUNT"] != "0"):
    message = hostmessage.format(**data)

# Check service state.
if (data["SERVICESTATE"] != data["SERVICESTATEPREVIOUS"] or data["SERVICESTATECOUNT"] != "0") and (data["SERVICE"] != "$SERVICEDESC$"):
    message = servicemessage.format(**data)

# Data we will send to Matrix Homeserver.
matrixDataDict = {
    "msgtype": "m.text",
    "body": message,
    "format": "org.matrix.custom.html",
    "formatted_body": message,
}
matrixData = json.dumps(matrixDataDict)
matrixData = matrixData.encode("utf-8")

# Random transaction ID for Matrix Homeserver.
txnId = ''.join(random.SystemRandom().choice(
    string.ascii_uppercase + string.digits) for _ in range(16))

# Authorization headers and etc.
matrixHeaders = {"Authorization": "Bearer " + MATRIXTOKEN,
                 "Content-Type": "application/json", "Content-Length": len(matrixData)}
# Request.
req = urllib.request.Request(url=MATRIXHOST + "/_matrix/client/r0/rooms/" + MATRIXROOM +
                             "/send/m.room.message/" + txnId, data=matrixData, headers=matrixHeaders, method="PUT")
# Exec.
urllib.request.urlopen(req)
