import hashlib
import time
import requests


class THVClient:
    def __init__(self, appid, appkey, server, cluster, user, timeout=60):
        self.appid = appid
        self.appkey = appkey
        self.server = server
        self.cluster = cluster
        self.user = user
        self.timeout = timeout

    def _make_sig(self, timestamp, vapp=None):
        str1 = "appkey=%s&timestamp=%s&cluster=%s&user=%s" % (
            self.appkey, timestamp, self.cluster, self.user)

        if vapp is not None:
            str1 = str1 + "&vapp=" + vapp

        hashStr = hashlib.sha256()
        hashStr.update(str1.encode())
        sig = hashStr.hexdigest()
        return sig

    def listApps(self):
        url = "%s/v1/%s/%s/visual/list?appid=%s" % (self.server, self.cluster, self.user, self.appid)
        print(url)
        timestamp = int(time.time())
        data = {
            "sig": self._make_sig(timestamp),
            "timestamp": timestamp,
        }

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            #print(resp.json())
            return resp.json()
        else:
            #print(resp.json())
            raise ValueError(resp.json())

    def launchApp(self, vapp,gpu=0,version="",param="",client="w"):
        if vapp == "shell":
            url = "%s/v1/%s/%s/web/shell/launch?appid=%s" % (self.server, self.cluster, self.user, self.appid)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp),
                "timestamp": timestamp,
            }
        else:
            url = "%s/v1/%s/%s/visual/%s/launch?appid=%s" % (self.server, self.cluster, self.user, vapp, self.appid)
            #print(url)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp, vapp),
                "timestamp": timestamp,
            }
            if param != "":
                data["param"] = param
            if int(gpu) == 1:
                data["gpu"] = "true"
            data["client"] = client
            data["version"] = version
            data["resolution"] = "1920x1200"
            #print(data)

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            resJ = resp.json()
            #print(resJ)
            return resJ
        else:
            #print(resp.json())
            raise ValueError(resp.json())

    def closeApp(self,vapp,gpu=0,version="",param="",client="w"):
        if vapp == "shell":
            return {"status":False,"error":"shell app not allowed close!!"}
        else:
            url = "%s/v1/%s/%s/visual/%s/close?appid=%s" % (self.server, self.cluster, self.user, vapp, self.appid)
            timestamp = int(time.time())
            data = {
                "sig": self._make_sig(timestamp, vapp),
                "timestamp": timestamp,
            }
            if param != "":
                data["param"] = param
            if int(gpu) == 1:
                data["gpu"] = "true"
            data["client"] = client
            data["version"] = version
            #print(data)

        resp = requests.post(url=url, data=data, timeout=self.timeout)

        if resp.status_code < 300:
            return {"status":True}
        else:
            raise ValueError(resp.json())


if __name__ == "__main__":
    # examples
    server = "http://127.0.0.1:8000"
    appid = "123456"
    appkey = "21212121212121212121212121212121"

    cluster = "th-1a"
    user = "user1"

    client = THVClient(appid, appkey, server, cluster, user)
    try:
        jobs = client.listApps()
        token = client.launchApp("desktop")
    except Exception as e:
        print(e)
    else:
        print(jobs)
        print(token)
