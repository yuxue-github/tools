import os
import sys, getopt
from optparse import OptionParser
import re
import csv

tc_name = 4
tc_result = 9
tc_build = 13

def analyze_report(template, list, result, build):
    f = csv.reader(open(template, 'r'))
    result = open(result, 'w', newline='')
    writer = csv.writer(result)
    tcs = []

    for line in f:
        if line[tc_build] == build:
            tcs.append(line)

    noRun = 0
    passed = 0
    others =0
    for item in list:
        item_result = "Not Run"
        for tc in tcs:
            if item.strip('\n\r')  in tc[tc_name]:
                if  "passed" == tc[tc_result]:
                    item_result = "passed"
                    break
                else:
                    item_result = tc[tc_result]

        print (item.strip('\n\r') +"\n" + item_result)
        writer.writerow([item.strip('\n\r'), line[tc_build], item_result])

        if "passed" == item_result:
            passed += 1
        elif "Not Run" == item_result:
            noRun += 1
        else:
            others += 1

    print ("result total--passed:" + str(passed) + " Not-Run:" + str(noRun) +\
           " others(failed/not_analyze/environment_issue...):" + str(others))



if __name__ == '__main__':
    print ("report analyze start...")
    template = ""
    result = ""
    version = ""
    listFile = ""
    parser = OptionParser()
    parser.add_option("-t", "--template", action="store",
                     dest="template",
                     default=False,
                     help="case report")
    parser.add_option("-l", "--list", action="store",
                      dest="listFile",
                      default=False,
                      help="case list")
    parser.add_option("-r", "--result", action="store",
                      dest="result",
                      default=False,
                      help="analyze result")
    parser.add_option("-v", "--version", action="store",
                      dest="version",
                      default=False,
                      help="software version")

    (options, args) = parser.parse_args()

    template = options.template
    result = options.result
    version = options.version
    listFile = options.listFile

    list = []
    fList = open(listFile, 'r')
    for line in fList:
        list.append(line)

    analyze_report(template, list, result, version)


