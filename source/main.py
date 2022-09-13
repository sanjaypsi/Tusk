import maya.cmds as cmds
import pymel.core as pm
import os
import json



def vaccine():
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

def openfile():
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


