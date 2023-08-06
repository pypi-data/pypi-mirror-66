import chaoslib
import json

'''
 * @param {string} _name is the substring of what you want search
		 * @param {("cu"|"us"|"agent"|"cds"|"webui"|"variable"|"snapshotsof"|"snapshots"|"script"|"zone"|"class")} _what operation type 
		 * @param {boolean} _alive search among alive (true) or all(false)
		 * @param  {okcb} [handleFunc] callback if ok, enable async mode
		 * @param  {badcb} [handlerr] callback if error
		 * @return an array of strings or objects
		 * @function search
 		 * @example
 		 * // search all CU alive
         * jchaos.search("","cu",true,function(ls){jchaos.print(JSON.stringify(ls));});
'''
def search(_name,_what,_alive,opts={}):
    opt = {
        "what": _what,
        "alive": _alive
         }
    if isinstance(_name, list): 
        opt["names"]=_name
    else:
        opt['name']=_name
    return chaoslib.mdsBase("search",opt)

'''
/**
         * Retrive the specified dataset correspoding to a given CU
         * @param  {String|String[]} devs CU or array of CU
         * @param  {channelid} channel_id (-1: all,0: output, 1: input, 2:custom,3:system, 4: health, 5 cu alarm, 6 dev alarms,128 status)
         * @return {object} the specified dataset
         * @function getChannel
         * @example
         * //retrive all channels of a give CU
         * chaos.getChannel("BTF/QUADRUPOLE/QUATB001",-1,function(ls){jchaos.print(JSON.stringify(ls));});
         *
         */
'''
def getChannel(_name,channel_id):

    if isinstance(_name, list): 
        dev_array=dev_array = ','.join(_name)

    else:
        dev_array=_name


    str_url_cu = "dev=" + dev_array + "&cmd=channel&parm=" + str(channel_id);

    return chaoslib.basicPost("CU",str_url_cu)


'''
 /**
             * Sends a command to a CU, with explicit params
             * @param  {string|string[]} devs CU or array of CU
             * @param  {string} cmd command to send
             * @param  {object} [param]
             * @param  {integer} force
             * @param  {integer} prio
             * @function sendCUFullCmd
             */
'''
def sendCUCmd(_name,cmd,param={}):
    
    if isinstance(_name, list): 
        dev_array=dev_array = ','.join(_name)

    else:
        dev_array=_name


    str_url_cu = "dev=" + dev_array
    if( isinstance(cmd,dict)):
         str_url_cu += "&cmd="+cmd["cmd"];
         if("mode" in cmd):
            str_url_cu += "&mode="+str(cmd["mode"])
         if("prio" in cmd):
            str_url_cu += "&prio="+str(cmd["prio"]);
         if("sched" in cmd):
            str_url_cu += "&sched="+str(cmd["sched"]);
    else:
        str_url_cu += "&cmd="+cmd;
 

    if(param):
        str_url_cu+= "&parm="+json.dumps(param)
        

    return chaoslib.basicPost("CU",str_url_cu)

'''
    /**
    Set an input attribute to the specified value
         * @param  {string|string[]} devs CU or array of CU
         * @param  {string} attr attribute name
         * @param  {string} value attribute value
    */
'''
def setAttribute(devs,attr,value):
    parm={}
    parm[attr]=str(value)
    return sendCUCmd(devs,"attr",parm)
       