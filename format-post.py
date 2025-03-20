import os
import sys
import re

imagePath = "images"
postdate = "" 
title = ""
newfilename = ""

def processImageTag(inFile):
    # if we're here, our caller has read in a "<figure>" tag. Process untill we get to the
    # matching "</figure>" tag
    imagePath = ""
    imageCaption = ""
    readingCaption = False
    line = ""
    while (line := inFile.readline()):
        if (line.startswith("</figure>")):
            break
        if (line.startswith("<figcaption>")):
            # if we're here, were looking for the text of the figure caption
            while (line := inFile.readline()):
                if (line.startswith("</figcaption>")):
                    break
                imageCaption = imageCaption + line.strip()
        else:
             if "](" in line and len(imagePath) == 0:
                 startidx = line.find("](")
                 stopidx = line.find(")", startidx)
                 imagePath = line[startidx + 2:stopidx]
    outText = "![picture](" + imagePath + ")\n"
    if len(imageCaption) > 0:
        outText = outText + "*" + imageCaption + "*"
    outText = outText + "\n"
    return outText

def processFrontMatter(inFile):
    global newfilename
    outText = "---\n"
    line = ""
    currentText = ""
    description = ""
    while (line := inFile.readline()):
        if (line.startswith("---\n")):
            # if we're here - found end of front matter tag. We're done.
            break
        if (line.startswith("categories:")):
            currentText = "categories: ["
            categorycount = 0
            while (line := inFile.readline()):
                temp = line.strip()
                if temp.startswith("-"):
                    temp = temp.replace("-", "")
                    temp = temp.replace("\"", "")
                    temp = temp.strip()
                    if (len(temp) > 0):
                        if (categorycount > 0):
                            currentText = currentText + ", "
                        categorycount = categorycount + 1
                        currentText = currentText + temp
                else:
                    break
            currentText = currentText + "]\n"
            outText = outText + currentText
        if (line.startswith("tags:")):
            currentText = "tags: ["
            tagcount = 0
            while (line := inFile.readline()):
                temp = line.strip()
                if temp.startswith("-"):
                    temp = temp.replace("-", "")
                    temp = temp.replace("\"", "")
                    temp = temp.strip()
                    if (len(temp) > 0):
                        if (tagcount > 0):
                            currentText = currentText + ", "
                        tagcount = tagcount + 1
                        currentText = currentText + temp
                else:
                    break
            currentText = currentText + "]\n"
            outText = outText + currentText
        if (line.startswith("date:")):
            postdate = line.replace("date:", "")
            postdate = postdate.replace("\"", "")
            postdate =  postdate.strip()
            newfilename = postdate
            outText =  outText + "date: " + postdate + " 02:02:02 +0700" +"\n"
        if (line.startswith("coverImage:")):
            currentText = line.replace("coverImage:", "")
            currentText = currentText.replace("\"", "")
            currentText = currentText.strip()
            currentText = "image: " + os.path.join(imagePath, out) + currentText + "\n"
            outText = outText + currentText
        if (line.startswith("title:")):
            outText = outText + "title: "
            title = line.replace("\"", "")
            title = title.replace("title:", "")
            title = title.strip()
            outText = outText + title + "\n"
        if (line.startswith("description:")):
            description = line
            # description = line.replace("description:", "")
            description = description.strip()
            outText = outText + line + "\n"
    if (len(description) == 0):
        outText = outText + "description: \n"
    newfilename = re.sub(r'[^\w\s]', '', title)
    newfilename = "-" + newfilename.replace("'", "")
    newfilename = postdate + newfilename + ".md"
    outText = outText + "---\n"
    return outText

in_filename = 'index.md'
out_filename = 'test.md'
path = sys.argv[1]
in_file_name = os.path.join(path, in_filename)
out_file_name = os.path.join(path, out_filename )
in_file = open(in_file_name, "r")
out_file = open(out_file_name, "w")
handled_front_matter = False
handling_front_matter = False
    
for line in in_file:
    print(line)
    out = ""
    if (line.startswith("---\n")and not handled_front_matter):
        frontMatterText = processFrontMatter(in_file)
        out_file.write(frontMatterText)
        handled_front_matter = True
    else:
        if (line.startswith("<figure>")):
            imageTag = processImageTag(in_file)
            out_file.write(imageTag)
        else: 
            out_file.write(line)
        
    
in_file.close()
out_file.close()
os.rename (os.path.join(path, out_filename), os.path.join(path, newfilename))
