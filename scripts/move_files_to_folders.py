# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:02:29 2020
@author: TianHx
把文件按规则移动到文件夹下
"""

# %%
import os
import glob
import shutil

# %%
srcFiles = "C:\\datasets\\jaffedbase-images\\*.tiff"
destFolder = r"C:\datasets\jaffedbase-images"


def move_files():
    files = glob.glob(srcFiles)
    for file in files:
        fileName = os.path.basename(file)
        folderName = fileName.split('.')[0]
        targetFolder = os.path.join(destFolder, folderName)
        os.makedirs(targetFolder, exist_ok=True)
        shutil.move(file, targetFolder)


# %%
move_files()
