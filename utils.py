import os

def generate_dirlist(dirpath,outfile):
    filelist = os.listdir(dirpath)
    with open(outfile,'w') as f:
        for tmp in filelist:
            f.write(os.path.relpath(os.path.join(dirpath,tmp)).replace('\\','/'))
            f.write('\n')
    return