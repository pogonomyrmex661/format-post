import os
import sys
import re

#imagePath = "images"
#postdate = "" 
#title = ""
newfilename = ""

in_filename = '2021-02-24-Acromyrmex versicolor Leafcutter Ants and Asagena Steatoda Spider.md'
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
    if line.strip().startswith("categories: [") or line.strip().startswith("category: ") or line.strip().startswith("category: "):
        textList[i] = "categories: [post]\n"
        
    if (line.startswith("\[caption id=")):
        startidx = line.find("![")
        line = line[startidx:]
        startidx = line.find(") ")
        imgstring = line[:startidx + 1]
        idx = imgstring.find("](http")
        if (idx > 0):
            imgstring = imgstring[:idx]
        if firstImage:
            idx = imgstring.find("](")
            temp = imgstring[idx+2:]
            if temp.rfind(")") > 0:
                temp = temp[:-1]
            textList[imageIdx]  =  "image: "  + temp +"\n"
            firstImage = False
        captionstring = line[startidx + 2:]
        startidx = captionstring.find("\[/captio")
        captionstring = captionstring[:startidx] 
        captionstring = "*" + captionstring + "*"
        textList[i] = imgstring + " " + captionstring + "\n"
    textList[i] = textList[i].replace("http:", "https:")

out_file.writelines(textList)
        
in_file.close()
out_file.close()
print("Finished!")
#new_in_filename = in_filename + ".bak"
#os.rename(os.path.join(path, in_filename), os.path.join(path, new_in_filename))
#os.rename (os.path.join(path, out_filename), os.path.join(path, in_filename))
