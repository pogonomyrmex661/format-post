import os
import sys
from argparse import ArgumentParser

in_filename = 'index.md'
out_filename = 'test.md'
print(sys.argv[1:])
path = sys.argv[1];
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
        handling_front_matter = True
        out_file.write(line)
    else:
        if (handling_front_matter):
            if (line == '---\n'):
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
                    out = "image: " + "images/" + out + "\n"
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

            out_file.write(line)
        
    
in_file.close()
out_file.close()
newfilename = postdate + "-" + title + ".md"
os.rename (os.path.join(path, out_filename), os.path.join(path, newfilename))
