"""
    Maya Scanner Tools Remove Two Node vaccine_gene / breed_gene

"""


import os
import json

import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds
import pymel.core as pm

class Maya_Scanner(object):
    def __init__(self):
        self._temp_dir = os.environ['temp']
        self._logfile_path = os.path.join (self._temp_dir, 'reference_path.json').replace ('\\', '/')

    def vaccine(self):
        infojson = []
        refs = pm.listReferences (recursive=True)
        for file_ref in refs:
            refnode = file_ref.refNode
            source_file = pm.referenceQuery (refnode, filename=True, withoutCopyNumber=True)
            infojson.append (source_file)

        my_final_list = dict.fromkeys (infojson)
        src = (list (my_final_list))
        
        with open (self._logfile_path, 'w') as fd:
            json.dump (src, fd, indent=4)

    # ==========================================================================================
    def get_file_for_dir(self, dir_path = None):
        self._dir = dir_path
        mayafile = [".ma", ".mb"]

        file_list = []
        all_files = list()
        for root, dirs, files in os.walk(self._dir, topdown=False):
            all_files.extend([os.path.join(root, f) for f in files])
        
        for x in range(len(all_files)):
            if all_files[x].endswith(mayafile[0]) or all_files[x].endswith(mayafile[1]):
                file_list.append(all_files[x])

        with open (self._logfile_path, 'w') as fd:
            json.dump (file_list, fd, indent=4)

        print ("EXPORT LIST FILE INTO JSON")
        
    # ==========================================================================================
    def openfile(self, save_path = None):

        virus = ['*vaccine_gene*', '*breed_gene*']
        with open (self._logfile_path, 'r') as f:
            data = json.load (f)

        f.close()

        for fil in data:
            if os.path.isfile (fil):
                try:
                    #cmds.file (fil, loadReferenceDepth='none', prompt=False, o=1, f=1)
                    cmds.file (fil, loadAllReferences=True, prompt=False, o=1, f=1)
                    sn_name = cmds.file (sceneName=True, query=True)
                    print("FILE IS OPEN >>>> %s", sn_name)

                    get_src_path = os.path.dirname(sn_name).split(':/')[1]
                    filename = os.path.basename(sn_name)

                    dst_path = os.path.join(save_path, get_src_path)
                    if not os.path.exists(dst_path):
                        os.makedirs(dst_path)

                    for v in virus:
                        cmds.select (v)
                        selected = cmds.ls (sl=True)
                        if selected:
                            cmds.delete (selected)
                            print("delete >>> ", selected)

                    filePathExport = os.path.join(dst_path, filename)
                    cmds.file(rename=filePathExport)
                    cmds.file(force=True,type="mayaAscii" ,save=True)
                    print("%s >>>>>>>>> file is save", filePathExport)

                except:
                    pass
    print("DONE >>>>>>>>>>>>>>>>>>>>")


path = r'Y:\MASILA\01_assets\char'
SC = Maya_Scanner()
SC.get_file_for_dir(dir_path = path)

path = r'D:\Cosmos'
SC.openfile(save_path = path)