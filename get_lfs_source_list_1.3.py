import os
import sys
import re
import subprocess

class get_lfs_source_list:
    def __init__(self, machine):
        os.system("source ./env.sh " + machine + " && bitbake -c do_fetchall lfs-release-full")
        self.__shell_source(machine)
        self.buildDir = os.environ["BUILDDIR"]
        self.machine = machine
        
    def start(self):
        lfs_source_list = []
        gitList = self.__get_git_list_through_grep_log()
        print gitList
        lfs_source_list = self.__gen_source_list_from_git_list(gitList)
        return lfs_source_list

    def __get_git_list_through_grep_log(self):
        print ("start to grep log.do_fetch files ... ")
        git_list = []
        path = self.buildDir + "/tmp/work"
        if not (os.path.exists(path)):
            print ('Path "' + path + '" not exists!')
            path = self.buildDir
            print ('change Path to "' + path)
        if (os.path.exists(path)):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if "log.do_fetch" == file:
                        file = root + '/' + file
                        print ("start file: " + file)
                        f = open(file)
                        for line in f.readlines():
                            if re.search("git ls-tree HEAD:src \| grep '\[\[:blank:\]\](.*)\$'", line):
                                git = "MN/RPSW/LFS/build/" + re.search("git ls-tree HEAD:src \| grep '\[\[:blank:\]\](.*)\$'", line).group(1)
                                if git not in git_list:
                                    print ("Add " + git + " to git list by git ls-tree HEAD")
                                    git_list.append(git)
                            if re.search("git -c(.*)clone(.*)ssh://(.*) (.*)", line):
                                gitGet = re.search("git -c(.*)clone(.*)ssh://(.*) (.*)", line).group(3)
                                git = gitGet[gitGet.find("/") + 1:]
                                if git[-4:] == ".git":
                                    git = git[:-4]
                                if git not in git_list:
                                    print ("Add " + git + " to git list")
                                    git_list.append(git)
                        f.close()
        else:
            print ('Warning: Path "' + path + '" not exists!')
        return git_list

    def __gen_source_list_from_git_list(self, gitList):
        git_ls_tree_list = []
        p = subprocess.Popen("git ls-tree HEAD:src", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        for line in p.stdout.readlines():
            git_ls_tree_list.append(line.strip())
        lfs_source_list = []
        for git in gitList:
            getRevision = False
            for line in git_ls_tree_list:
                if git.split("/")[-1] in line and re.search("(.*)\t(.*)", line)\
                   and (git.split("/")[-1] == re.search("(.*)\t(.*)", line).group(2)):
                    getRevision = True
                    lfs_source_list.append(git + " src/" + git.split("/")[-1] + " " + re.search("([0-9]*) commit (.*)\t", line).group(2))
            if not getRevision:
                revision = self.__get_revision_from_downloads_git2(git)
                if revision:
                    lfs_source_list.append(git + " src/" + git.split("/")[-1] + " " + revision)
                else:
                    print ("Warning: didn't find revision for " + git)
        return lfs_source_list

    def __get_revision_from_downloads_git2(self, git):
        git2Path = self.buildDir + "/downloads/git2"
        gitPath = ""
        for dir in os.listdir(git2Path):
            if git.replace('/', '.') in dir and ".done" != dir[-5:]:
                gitPath = dir
        if gitPath:
            revision = os.popen("cd " + git2Path + "/" + gitPath + " && git show")
            return revision.readlines()[0].strip().split(" ")[-1]
        return ""

    def __shell_source(self, machine):
        pipe = subprocess.Popen("source ./env.sh %s; env" % machine, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        for line in output.splitlines():
            if "=" in line:
                parameter = line.split("=")[0]
                value = line.split("=")[1]
                os.environ[parameter] = value

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Usage: python ${SCRIPT_NAME} <MACHINE>")
    machine = sys.argv[1]
    getList = get_lfs_source_list(machine)
    sourceList = getList.start()
    for source in sourceList:
        print source
    print len(sourceList)
    print ("Done!")
