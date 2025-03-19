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

    # reading each line    
for line in in_file:
    if (handled_front_matter == False and line == '---'):
        handling_front_matter = True
        out_file.write(line)
    else:
        if (handling_front_matter):
            if (line == '---'):
                out_file.write(line)
                handled_front_matter = True
                handling_front_matter = False

        else:
            out_file.write_line
        
    
in_file.close()
out_file.close()
