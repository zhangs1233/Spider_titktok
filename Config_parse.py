import configparser
import os
BASE_URL_PATH= os.path.dirname(os.path.abspath(__file__))
cfgPath=os.path.join(BASE_URL_PATH,"config.ini")
class Parser_config:
    def __init__(self):
        self.cf=configparser.ConfigParser()
        self.cf.read(cfgPath)
    def get_user(self):
        return self.cf.get("ProxyBASE","username")
    def get_passwd(self):
        return self.cf.get("ProxyBASE","password")
    def get_ip_port(self):
        return self.cf.get("URL","ip")+":"+self.cf.get("URL","port")
if __name__=="__main__":
    parse=Parser_config()
