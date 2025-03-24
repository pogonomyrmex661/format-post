import os
import sys
import re

imagePath = "images"
postdate = "" 
title = ""
newfilename = ""

in_filename = '2021-08-01-San Juan Mountain Mushrooms.md'
out_filename = 'test.md'
path = sys.argv[1]
firstimage = ""
in_file_name = os.path.join(path, in_filename)
out_file_name = os.path.join(path, out_filename )
in_file = open(in_file_name, "r")
out_file = open(out_file_name, "w")

imageIdx = -1
firstImage = True
textList = in_file.readlines()

for i in range(len(textList)):
    line = textList[i]
    print(line)
    out = ""
    if line.startswith("image:"):
        imageIdx = i
        
    if (line.startswith("\[caption id=")):
        startidx = line.find("![")
        line = line[startidx:]
        startidx = line.find(") ")
        imgstring = line[:startidx + 1]
        if firstImage:
            idx = imgstring.find("](")
            temp = imgstring[idx+2:]

            if len(temp) == temp.rfind(")"):
                temp = temp[:-1]
            textList[imageIdx]  =  "image: "  + temp +"\n"
            firstImage = False
        captionstring = line[startidx + 2:]
        startidx = captionstring.find("\[/captio")
        captionstring = captionstring[:startidx] 
        captionstring = "*" + captionstring + "*"
        textList[i] = imgstring + " " + captionstring + "\n"

out_file.writelines(textList)
        
in_file.close()
out_file.close()
#os.rename (os.path.join(path, out_filename), os.path.join(path, newfilename))
