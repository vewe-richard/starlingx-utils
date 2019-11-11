import os
import subprocess
from baseaction import BaseAction

class PackingSysApp(BaseAction):
    def cmd(self):
        return "packingsysapp"

    def summary(self):
        return "Packing applications for starlingx system command information"

    def description(self):
        return '''
SYNOPSIS:
    Packing applications for starlingx system command information

DESCRIPTIONS:
    show help information for the specific command

OPTIONS:
    directory
        application directory
'''

    def run(self, args, opts):
        if len(args) == 0:
            print "Error: Missing directory"
            self.usage()
            return

        try:
            self.packing(args[0])
        except Exception as e:
            print e
        
    def packing(self, directory):
        lines = self.genmd5(directory)
        self.writemd5(directory, lines)
        subprocess.call(["tar", "-C", directory, "-cvzf", "output.tgz", "./"])
        

    def writemd5(self, appdir, lines):
        with open(appdir + "/checksum.md5", 'w') as f:
            f.writelines(lines)
        

    def genmd5(self, appdir):
        files = []
        skip = 0
        for r, d, f in os.walk(appdir):
            for file in f:
                if "checksum.md5" == file:
                    continue
                if "metadata.yaml" == file:
                    skip = len(r)
                files.append(os.path.join(r, file))

        if skip == 0:
            raise Exception("Error: can not find metadata.yaml")

        lines = []
        for file in files:
            result = subprocess.check_output(["md5sum", file])
            items = result.split()
            if len(items) != 2:
                continue
            lines.append(items[0] + "  ./" + items[1][skip:] + "\n")
        return lines


