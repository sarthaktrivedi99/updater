import os
import sys
from halo import Halo
import shutil
import json
import urllib.request
import urllib.error
from pkg_resources import parse_version
import re
import zipfile
class update():
    def __init__(self,host,fileconst,verfile='ver.json'):
        self.file = fileconst
        self.hostname = host
        self.ver = verfile
        self.spinner = None
        self.updatepath = None
        self.verB = None
        self.name = None
        self.filename = None
        print('\33[94m'+"""
 _____      _             
|  _  |    (_)            
| | | |_ __ _  ___  _ __  
| | | | '__| |/ _ \| '_ \ 
\ \_/ / |  | | (_) | | | |
 \___/|_|  |_|\___/|_| |_|
                          
                          """+ '\33[0m')
        try:
            self.verfile()
            self.getinfo()
            self.checkver()
            self.getfiles()
            self.createbackself()
            self.unzip()
            self.replacewithoriginal()
        except NameError:
            pass
    def verfile(self):
        self.spinner = Halo()
        try:
            self.r = open(self.ver ,'r')
            self.info = json.loads(self.r.read())
            self.name = self.info["app"]
            self.ver = self.info["version"]
            print('App: '+self.name,'\t',"Version: "+self.ver)
        except FileNotFoundError:
            self.spinner.fail('Please Add a {} file'.format(self.ver))
            exit()

    def getinfo(self):
        self.info=[]
        self.spinner = Halo(text='Loading info', spinner='dots')
        self.spinner.color = 'blue'
        self.spinner.start()
        try:
            self.request = urllib.request.urlopen(self.hostname+'/info.json')
            self.temp = self.request.read().decode('ascii').split('\n')
            for i in range(len(self.temp)):
                self.info.append(json.loads(self.temp[i]))
            self.temp=next((item for item in self.info if item["app"] == self.name))
            self.verB = self.temp["version"]
            self.updatepath =self.temp["path"]
            self.spinner.stop()
            sys.stdout.write("\033[F")
            self.spinner.succeed("Fetched Info")
        except urllib.error.URLError:
            self.spinner.fail("Sorry File on the server could not be found")
            exit()

    def checkver(self):
        if parse_version(self.ver) < parse_version(self.verB):
            pass
        else:
            print("App Upto Date!")
            rasie NameError()

    def getfiles(self):
        self.info=[]
        self.spinner = Halo(text='Getting Files', spinner='dots')
        self.spinner.start()
        try:
            self.request = urllib.request.urlopen(self.hostname+self.updatepath)
            [self.info.append(i.split()[-1]) for i in self.request.read().decode('ascii').split('\r\n')[:-1]]
            self.filename = [i for i in self.info if re.search('.*\.zip',i)]
            if(self.filename.__len__()==0):
                self.spinner.fail("Could not find the archive")
                exit()
            self.filename = "".join(self.filename)
            urllib.request.urlretrieve(self.hostname+self.updatepath+self.filename,'/tmp/'+self.filename)
        except urllib.error.URLError:
            self.spinner.fail("Could not find the archive")
            exit()

    def createbackup(self):
        self.spinner = Halo(text='Creating a Backup', spinner='dots')
        self.spinner.start()
        try:
            self.dir = os.path.dirname(os.path.realpath(self.file))
            self.dst='/tmp/.'+ self.name
            shutil.copytree(self.dir,self.dst)
        except FileExistsError:
            shutil.rmtree(self.dst)
            shutil.copytree(self.dir, self.dst)
        except:
            self.spinner.fail('Sorry Backup Failed =(')
            exit()
        self.spinner.stop()
        sys.stdout.write("\033[F")
        self.spinner.succeed("Backup Created Successfully at {}".format(self.dst))

    def unzip(self):
        self.spinner = Halo(text='Extracting zip', spinner='dots')
        self.spinner.start()
        try:
            self.zip_obj = zipfile.ZipFile('/tmp/'+self.filename,'r')
            self.zip_obj.extractall('/tmp/.update')
            self.zip_obj.close()
        except zipfile.BadZipfile:
            self.spinner.fail("Bad ZIP")
            exit()
        self.spinner.succeed("Extracted Files")

    def replacewithoriginal(self):
        self.spinner = Halo(text='Copying the Update', spinner='dots')
        self.spinner.start()
        try:
            self.files = os.listdir('/tmp/.update')
            for i in self.files:
                shutil.copy2('/tmp/.update/'+i,self.dir)
            self.spinner.succeed('Updated Successfully!')
            self.temp = open('ver.json','w')
            self.info = {"app":self.name,"version":self.verB}
            self.temp.write(json.dumps(self.info))
            self.temp.close()
        except:
            self.spinner.fail("Failed to update. Rolling Back")
            self.files = os.listdir(self.dst)
            for i in self.files:
                shutil.copy2(self.dir+i,self.dir)
            self.spinner.succeed("Rolled Back Successfully")

if __name__ == '__main__':
    up = update('ftp://192.168.0.8',__file__)
    
