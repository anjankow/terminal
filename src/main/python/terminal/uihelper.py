# This Python file uses the following encoding: utf-8

import subprocess
import glob
import os


def generate_ui(ui_dir):
    # generated python path should be added to the current directory
    current_dir = os.path.dirname(__file__)

    for file in glob.glob(ui_dir + '/*.ui'):
        # get basename of file and remove .ui from the end (3 chars)
        ui_name = (os.path.basename(file))[:-3]
        print('Generating python file for ', ui_name, ' ui')
        cmd = ['pyuic5.exe', '-x', file, '-o', current_dir + '/Ui_' + ui_name + '.py']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        for line in process.stdout:
            print(line)

if __name__ == "__main__":
    pass
