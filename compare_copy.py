import filecmp
import os
import shutil

test_src1 = '/media/xigu/DensoML/xinyu/tools/move/1/'
test_src2 =  '/media/xigu/DensoML/xinyu/tools/move/2/'

test_dst = '/media/xigu/DensoML/xinyu/tools/move/0/' 

def rename(old_filename):
    new_filename = old_filename.split('/')[-2] + '_' + old_filename.split('/')[-1]
    return new_filename

def SafeCopy(src, dst):
    """Copies a file from path src to path dst.

    If a file already exists at dst, it will not be overwritten, but:

     * If it is the same as the source file, do nothing
     * If it is different to the source file, pick a new name 'samename_1' 
       or 'samename_2' for the copy, then copy the file there.

    """
    if not os.path.exists(src):
        raise ValueError("Source file does not exist: {}".format(src))

    # Create a folder for dst if one does not already exist
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    target = src.split('/')[-1]
    dst_file = dst + target
    print(dst_file)
    if os.path.exists(dst_file):
    # If the file is the same as the source file, do nothing
        if filecmp.cmp(src, dst):
            pass
    # If the source file is not the same with the dst file, 
    # rename the source file and copy to dst folder
        else:
            renamed_file = rename(src)
            new_dst = dst + renamed_file
            shutil.copyfile(src, new_dst)
        
    # If there is no file of the same name at the destination path, copy
    # to the destination
    else:
        shutil.copyfile(src, dst_file)

for file in os.listdir(test_src1):
    if file[0] == '.':
        continue
    SafeCopy(test_src1+str(file), test_dst)
