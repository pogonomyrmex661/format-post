import os
import sys
import re

imagePath = "images"

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
             if "])" in line and len(imagePath) == 0:
                 imagePath = imagePath + line.split("])")[1].split(")\n")[0]
    outText = "![picture](" + imagePath + ") \"picture\")\n"
    if len(imageCaption) > 0:
        outText = outText + "*" + imageCaption + "*"
    outText = outText + "\n"
    return outText

in_filename = 'index.md'
out_filename = 'test.md'
#print(sys.argv[1:])
path = sys.argv[1]
in_file_name = os.path.join(path, in_filename)
out_file_name = os.path.join(path, out_filename )
in_file = open(in_file_name, "r")
out_file = open(out_file_name, "w")
handled_front_matter = False
handling_front_matter = False
postdate = "" 
description = ""
title = ""
newfilename = ""
    
for line in in_file:
    print(line)
    out = ""
    if (handled_front_matter == False and not handling_front_matter and line == '---\n'):
        # if we're here, we have not yet handled front matter, but have read the tag starting it
        handling_front_matter = True
        out_file.write(line)
    else:
        if (handling_front_matter):
            # if we're here, we're currently processing the front matter contents.
            if (line == '---\n'):
                # if we're here, we're closing the end matter tag
                if (len(description) == 0):
                    out_file.write("description: \n")
                out_file.write(line)
                handled_front_matter = True
                handling_front_matter = False
            else:
                if (line.startswith("title:")):
                    out = line.replace("\"", "")
                #if (line[0] != ' '):
                if (line.startswith("date:")):
                    postdate = line.replace("date:", "")
                    postdate = postdate.replace("\"", "")
                    postdate =  postdate.strip()
                    newfilename = postdate
                    out = "date: " + postdate + " 02:02:02 +0700" +"\n"
                if (line.startswith("coverImage:")):
                    out = line.replace("coverImage:", "")
                    out = out.replace("\"", "")
                    out = out.strip()
                    out = "image: " + os.path.join(imagePath, out) + "\n"
                if (line.startswith("categories:")):
                    out = line
                if (line.startswith("tags:")):
                    out = line
                if (line.startswith("title:")):
                    title = line.replace("title:", "")
                    title = title.replace("\"", "")
                    title = title.strip()
                if (line.startswith("description:")):
                    description = out
                    description = out.replace("description:", "")
                    description = description.strip()
                    out = line
                out_file.write(out)
        else:
            # if we're here, we are not processing front matter. Likely the body of the post.
            if (line.startswith("<figure>")):
                imageTag = processImageTag(in_file)
                out_file.write(imageTag)
            else:
                out_file.write(line)
        
    
in_file.close()
out_file.close()
title = re.sub(r'[^\w\s]', '', title)
newfilename = postdate + "-" + title.replace("'", "") + ".md"
os.rename (os.path.join(path, out_filename), os.path.join(path, newfilename))
