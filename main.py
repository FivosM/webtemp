import sys, os, os.path, shutil
import time
import json
import re

try:
    import htmlmin
    #minification does not touch your files but the /build directory files
    minify = True #turn this off to disable minification of code 
except:
    minify = False

try:
    import markdown
    md = True
except:
    md = False


startTime = time.time()
startCpuTime = time.process_time()

contentEndsWith = ".webcontent"
templateEndsWith = ".webtemp"
contentUniqueString = "#####CONTENT#####" #text to replace in *.webtemp files
templateUniqueString = "#####" #text for identifying template in .webcontent files (eg: #####main#####)
templateRegex = re.compile(templateUniqueString+r'([\S]+)'+templateUniqueString)

verbose = False
def verbosePrint(s):
    if verbose == True:
        print(s)

def markdownAddTemplate(filepath, templateDir):
    try:
        f = open(filepath, "r+")
        if f:
            w = re.search(templateRegex, f.readline().rstrip())
            if w:
                template = w.group(1)
                if os.path.isfile(templateDir+"/"+template+templateEndsWith):
                    try:
                        templatef = open(templateDir+"/"+template+templateEndsWith, "r")
                        k = templatef.read()
                        templatef.close()
                        l = f.read()
                        k = k.replace(contentUniqueString, markdown.markdown(l))
                        f.seek(0)
                        if minify: k = htmlmin.minify(k, remove_empty_space=True, keep_pre=True, reduce_boolean_attributes=True)
                        f.write(k)
                    except:
                        print("ERROR cannot read {}".format(templateDir+"/"+template+templateEndsWith))
            f.close()
            os.rename(filepath, filepath[:-len(".md")]+".html")
    except:
        print("ERROR opening file: {}".format(filepath))

def addTemplate(filepath, templateDir):
    try:
        f = open(filepath, "r+")
        if f:
            w = re.search(templateRegex, f.readline().rstrip())
            if w:
                template = w.group(1)
                if os.path.isfile(templateDir+"/"+template+templateEndsWith):
                    try:
                        templatef = open(templateDir+"/"+template+templateEndsWith, "r")
                        k = templatef.read()
                        templatef.close()
                        l = f.read()
                        k = k.replace(contentUniqueString, l)
                        f.seek(0)
                        if minify: k = htmlmin.minify(k, remove_empty_space=True, keep_pre=True, reduce_boolean_attributes=True)
                        f.write(k)
                    except:
                        print("ERROR cannot read {}".format(templateDir+"/"+template+templateEndsWith))
            f.close()
            os.rename(filepath, filepath[:-len(contentEndsWith)]+".html")
    except:
        print("ERROR opening file: {}".format(filepath))

def recurseWalk(path, templateDir): #loop recursively through the build directory
    for root, dirs, files in os.walk(path, followlinks=True):
        for i in dirs:
            recurseWalk(root+"/"+i, templateDir)
        for i in files:
            if i.endswith(contentEndsWith):
                addTemplate(root+"/"+i, templateDir)
            if i.endswith(".md") and md:
                markdownAddTemplate(root+"/"+i, templateDir)

def main():
    rootPath = os.getcwd()
    if os.path.isfile(rootPath+'/csettings.json'):
        with open(rootPath+'/csettings.json', "r") as f:
            try:
                jsonf = json.load(f)
                if jsonf["settings"]["site-directory"] and jsonf["settings"]["template-directory"] and jsonf["settings"]["build-directory"]:
                    try:
                        if os.path.isdir(rootPath+'/'+jsonf["settings"]["build-directory"]):
                            shutil.rmtree(rootPath+'/'+jsonf["settings"]["build-directory"])
                            verbosePrint("Deleted pre-existing build directory and its contents")
                        shutil.copytree(rootPath+'/'+jsonf["settings"]["site-directory"], rootPath+'/'+jsonf["settings"]["build-directory"])
                        verbosePrint("Copied build directory: {}".format(rootPath+'/'+jsonf["settings"]["build-directory"]))
                        verbosePrint("Entering build directory")
                        recurseWalk(rootPath+'/'+jsonf["settings"]["build-directory"], rootPath+'/'+jsonf["settings"]["template-directory"])
                    except:
                        print("ERROR: Directory error")
            except:
                print("ERROR: csettings.json parsing error")
    else:
        print('ERROR: csettings.json does not exist')
    print("EXITING\nReal time: {}\nCpu time: {}".format(time.time() - startTime, time.process_time() - startCpuTime))

if __name__ == '__main__':
  main()