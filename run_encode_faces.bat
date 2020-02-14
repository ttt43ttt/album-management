set ANACONDA_HOME=C:\apps\Anaconda3
call %ANACONDA_HOME%\Scripts\activate.bat %ANACONDA_HOME%\envs\py36_x86

python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog
