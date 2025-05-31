import os
import shutil

def copy_static(path_dest,path_src):
    if os.path.exists(path_dest):
        shutil.rmtree(path_dest)
        print("Public Directory Deleted")
    os.mkdir(path_dest)
    print("public Dirictory created")

    copy_all_files(path_dest,path_src)

def copy_all_files(path_dest,path_src):
    files = os.listdir(path_src)
    for file in files:
        s_item = os.path.join(path_src,file)
        d_item = os.path.join(path_dest,file)

        if os.path.isdir(s_item):
            os.makedirs(d_item, exist_ok=True)
            copy_all_files(d_item,s_item)
        else:
            shutil.copy(s_item,d_item)
            print(f"Copied file: {s_item} -> {d_item}")


