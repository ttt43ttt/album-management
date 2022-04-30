# album-management
Photo album management system based on face recognition

<img src="https://user-images.githubusercontent.com/132509/145827516-731b7404-15d8-4023-ba9f-5a35420c6bad.png" style="width: 500px;"/>

# How to run this project
- Install softwares:
  - Anaconda or other Python env
    - Install required modules
  - PostgreSQL or other relational database
    - See `db` folder for how to initialize database
  - Node.js
    - Run `npm install` in `webui` directory
- `start-service.bat` starts the backend service.
- `start-webui.bat` starts the web UI service which uses the backend service. Open a web browser to access the web UI.


# Original Article
https://www.pyimagesearch.com/2018/07/09/face-clustering-with-python/
http://www.atyun.com/23521.html


### How to run demo in the original article (not this project)
- From Anaconda command line: `conda activate py36_x86`
  - To setup Python and modules: python3.6 x86
    - `pip install imutils face_recognition scikit-learn`
- Encode faces: `python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog`
- Cluster faces: `python cluster_faces.py --encodings encodings.pickle`
