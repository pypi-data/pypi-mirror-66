import requests
import json

options = {
    "uri":"localhost:8081",
    "timeout":5000,
}
def setOptions(opt):
    options= opt

def timestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class chaosException(Exception):
    """Exception raised for rest exception.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.msg = message

def basicPost(func,params):
    srv = options["uri"];
    url = "http://" + srv + "/" + func;
    r = requests.post(url, data=params)
    if(r.status_code == requests.codes.ok):
        return r.content
    else:
        raise chaosException("")

def mdsBase(cmd,opt):
    param = "cmd=" + cmd + "&parm=" + opt
    return basicPost("MDS", param)

def search(_name,_what,_alive,opts):
    opt = {
        "what": _what,
        "alive": _alive
         }
    if isinstance(_name, list): 
        opt["names"]=_name
    return mdsBase("search",opt)
