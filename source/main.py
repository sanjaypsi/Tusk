"""
Maya Scanner Tools Remove Two Node vaccine_gene / breed_gene

"""

import maya.cmds as cmds
import pymel.core as pm
import os
import json

class Maya_Scanner(object):
    def __init__(self) -> None:
        pass

    def vaccine(self):
        TempDir = os.environ['TMPDIR']
        infojson = []
        refs = pm.listReferences (recursive=True)
        for file_ref in refs:
            refnode = file_ref.refNode
            source_file = pm.referenceQuery (refnode, filename=True, withoutCopyNumber=True)
            infojson.append (source_file)

        my_final_list = dict.fromkeys (infojson)
        src = (list (my_final_list))
        logfile_path = os.path.join (TempDir, 'reference_path.json').replace ('\\', '/')
        with open (logfile_path, 'w') as fd:
            json.dump (src, fd, indent=4)

    # ==========================================================================================
    def get_file_for_dir(self, dir_path = None):
        self._dir = dir_path

        all_files = list()
        for root, dirs, files in os.walk(self._dir, topdown=False):
            all_files.extend([os.path.join(root, f) for f in files])
        
        print(all_files)

    # ==========================================================================================
    def openfile(self):
        TempDir = os.environ['TMPDIR']
        virus = ['*vaccine_gene*', '*breed_gene*']
        logfile_path = os.path.join (TempDir, 'reference_path.json').replace ('\\', '/')
        with open (logfile_path, 'r') as f:
            data = json.load (f)

        f.close()

        for fil in data:
            if os.path.isfile (fil):
                try:
                    #cmds.file (fil, loadReferenceDepth='none', prompt=False, o=1, f=1)
                    cmds.file (fil, loadAllReferences=True, prompt=False, o=1, f=1)
                    sn_name = cmds.file (sceneName=True, query=True)
                    for v in virus:
                        cmds.select (v)
                        selected = cmds.ls (sl=True)[0]
                        if selected:
                            cmds.delete (selected)
                            print("delete >>> ", selected)

                    cmds.file (save=True, type='mayaAscii')
                    # print("%s >>>>>>>>> file is save", sn_name)

                except:
                    pass

path = r'V:\demo\Tusk'
SC = Maya_Scanner()
SC.get_file_for_dir(dir_path = path)