# album-management
Photo album management system based on face recognition

<img src="https://user-images.githubusercontent.com/132509/145827516-731b7404-15d8-4023-ba9f-5a35420c6bad.png" style="width: 500px;"/>


# Original Article
https://www.pyimagesearch.com/2018/07/09/face-clustering-with-python/
http://www.atyun.com/23521.html


# How to run the example
- From Anaconda command line: `conda activate py36_x86`
  - To setup Python and modules: python3.6 x86
    - `pip install imutils face_recognition scikit-learn`
- Encode faces: `python encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method hog`
- Cluster faces: `python cluster_faces.py --encodings encodings.pickle`
