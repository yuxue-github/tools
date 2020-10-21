import os
import sys
import re

def char_replace(path, char_old, char_new):
    print "start to replace " + char_old + " --> " + char_new
    if (os.path.exists(path)):
        for root, dirs, files in os.walk(path):
#        files = os.listdir(path)
            for file in files:
                file_data = ""
                file = root + '\\' + file
                print "start file: " + file
                f = open(file)
                changed = False
                for line in f.readlines():
                    if ("Force Tags" in line) and (char_old in line):
                        changed = True
                        line = line.replace(char_old, char_new)
                    if ("[Tags]" in line) and (char_old in line):
                        changed = True
                        line = line.replace(char_old, char_new)
                    file_data += line
                f.close()

                if changed:
                    with open(file, "w") as f:
                        f.write(file_data)
                    f.close()

def update_qc_files(path, char_old, char_new):
    print "start to update_qc_files " + char_old + " --> " + char_new
    if (os.path.exists(path)):
        for root, dirs, files in os.walk(path):
            #        files = os.listdir(path)
            for file in files:
                if ".qc" == file[-3:]:
                    print "start qc file: " + file
                    file_data = ""
                    file = root + '\\' + file
                    f = open(file)
                    changed = False
                    for line in f.readlines():
                        if "SB.*_" in line:
                            changed = True
                            line = line.replace(char_old, char_new)
                        if "SBTS.*_" in line:
                            changed = True
                            line = line.replace("SBTS", char_new)
                        if "SBTS00.*_" in line:
                            changed = True
                            line = line.replace("SBTS", char_new)
                        file_data += line
                    f.close()

                    if changed:
                        with open(file, "w") as f:
                            f.write(file_data)
                        f.close()

def tag_enable_disable(path, mark):
    enable = True
    if "enable" == mark:
        print "start to enable the Tag"
    elif "disable" == mark:
        enable = False
        print "start to disable the Tag"
    if (os.path.exists(path)):
        for root, dirs, files in os.walk(path):
#        files = os.listdir(path)
            for file in files:
                file_data = ""
                file = root + '\\' + file
                print "start file: " + file
                f = open(file)
                changed = False
                for line in f.readlines():
                    if enable:
                        if "#Force Tags" in line:
                            changed = True
                            line = line.replace("#Force Tags", "Force Tags")
                        """if "#[Tags]" in line:
                            changed = True
                            line = line.replace("#[Tags]", "[Tags]")
                        if "#	[Tags]" in line:
                            changed = True
                            line = line.replace("#	[Tags]", "	[Tags]")
                        if "#    [Tags]" in line:
                            changed = True
                            line = line.replace("#    [Tags]", "	[Tags]")
                        if "#   [Tags]" in line:
                            changed = True
                            line = line.replace("#   [Tags]", "	[Tags]")"""
                    else:
                        if ("Force Tags" in line) and ("#Force Tags" not in line):
                            changed = True
                            line = line.replace("Force Tags", "#Force Tags")
                        if ("[Tags]" in line) and ("#[Tags]" not in line) and ("#    [Tags]" not in line) and\
                                ("#	[Tags]" not in line) and ("#   [Tags]" not in line):
                            changed = True
                            line = line.replace("[Tags]", "#[Tags]")
                    file_data += line
                f.close()

                if changed:
                    with open(file, "w") as f:
                        f.write(file_data)
                    f.close()

def copyfile_from_to(file_list, from_dir, to_dir):
    print "start to copy files from " + from_dir + " to " +  to_dir
    f = open(file_list)
    if (os.path.exists(from_dir)):
        files_from = os.listdir(from_dir)
    else:
        print "didn't found the from_dir: " + from_dir
        return False
    for line in f.readlines():
        found = False
        for file_from in files_from:
            if file_from.replace('_', '') in line.replace('_', '').replace(' ', ''):
                found = True
                break
        file = from_dir + '\\' + file_from
        if found:
            print "start to copy file: " + file_from
            cpCommand = 'cp ' + file + ' ' + to_dir + '\\' + file_from
            os.system(cpCommand)
        else:
            print "didn't find the file: " + line


if __name__ == '__main__':
    operation = sys.argv[1]
    print "start operation: " + operation
    if "char_replace" == operation:
        path = sys.argv[2]
        print "the case locate at:" + path
        char_old = sys.argv[3]
        char_new = sys.argv[4]
        char_replace(path, char_old, char_new)
    if "update_qc" == operation:
        path = sys.argv[2]
        print "the case locate at:" + path
        char_old = sys.argv[3]
        char_new = sys.argv[4]
        update_qc_files(path, char_old, char_new)
    elif "tag_enable_disable" == operation:
        path = sys.argv[3]
        print "the case locate at:" + path
        mark = sys.argv[2]
        tag_enable_disable(path, mark)
    elif "copyfile_from_to" == operation:
        file_list = sys.argv[2]
        from_dir = sys.argv[3]
        to_dir = sys.argv[4]
        copyfile_from_to(file_list, from_dir, to_dir)
    print "Done!"
