set ANACONDA_HOME=C:\apps\Anaconda3
call %ANACONDA_HOME%\Scripts\activate.bat %ANACONDA_HOME%\envs\py36_x86

python cluster_faces.py --encodings encodings.pickle
