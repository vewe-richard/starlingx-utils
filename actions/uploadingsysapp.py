import os
import subprocess
import time
from baseaction import BaseAction
from packingsysapp import PackingSysApp 

class UploadingSysApp(BaseAction):
    def cmd(self):
        return "uploadingsysapp"

    def summary(self):
        return "Uploading applications of starlingx system"

    def description(self):
        return '''
SYNOPSIS:
    Uploading application of starling system

DESCRIPTIONS:
    Uploading application of starling system

OPTIONS:
    directory
        application directory
'''

    def run(self, args, opts):
        if len(args) == 0:
            print "Error: Missing directory"
            self.usage()
            return
        directory = args[0]
#        self.uploading(directory)
        self.test(directory)

    def test(self, directory):
        app_name = self.app_name(directory) 
        print app_name


        count = 0
        while True:
            try:
                app_status = self.app_status(app_name)
            except APPLICATION_NOT_EXIST:-----------------------------
                break

            print "application status: app_status"
            if app_status == "apply-failed":
                count = 0
                print "system application-remove", app_name
                try:
                    subprocess.check_output(["system", "application-remove", app_name])
                except subprocess.CalledProcessError as grepexc:
                    raise Exception("Error: system call to application")
            elif app_status == "uploaded":
                count = 0
                print "system application-delete", app_name
                try:
                    subprocess.check_output(["system", "application-delete", app_name])
                except subprocess.CalledProcessError as grepexc:
                    raise Exception("Error: system call to application")
            else:
                print "Unprocessed status: ", app_status
            count += 1
            if count > 3:
                raise "Error: preprocess application status failed"
            time.sleep(1)
                

    def app_status(self, app_name):
        try:
            result = subprocess.check_output(["system", "application-show", app_name])
            for line in result.split("\n"):
                items = line.split("|")
                if len(items) < 3:
                    continue
                if items[1].strip() == "status":
                    return items[2].strip()
        except subprocess.CalledProcessError as grepexc:
            raise Exception("Error: system call to application")

        raise Exception("Error: can not find application status")

    def uploading(self, directory):
        # check if directory is exist
        if not os.path.isdir(directory):
            raise Exception("Error:" + directory + "is not a directory")

        if not os.path.exists(directory):
            raise Exception("Error:" + directory + "is not exist")

        app_name = self.app_name(directory)        
        print "Directory is ", directory, ", application name is ", app_name

        # generate output.tgz
        print "--- Packing application tgz ---"
        PackingSysApp().packing(directory)
        print ""

        # copy helm charts to www
        for file in os.listdir(directory + "/charts"):
            src = directory + "/charts/" + file
            dst = "/www/pages/helm_charts/test/"
            print "cp", src, "to", dst
            try:
                subprocess.check_output(["cp", src, dst])
            except subprocess.CalledProcessError as grepexc:
                raise Exception("Error on copy")

        # system upload
        # system applying
        # system application status
        # system log if error
        # 

    def app_name(self, directory):
        with open(directory + "/metadata.yaml", "r") as f:
            lines = f.readlines()
            for line in lines:
                items = line.split(":")
                if len(items) != 2:
                    continue
                if items[0].strip() == "app_name":
                    return items[1].strip()

        raise "Error: can not get application name"










