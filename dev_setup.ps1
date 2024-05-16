C:\Python310\python -m pip install --upgrade pip
C:\Python310\Scripts\virtualenv C:\VirtualEnvs\cascade

$PROJECT_LOCATION = "D:\GitHub\cascade"
cd $PROJECT_LOCATION

C:\VirtualEnvs\cascade\Scripts\activate.ps1

pip install -e .
pip install -r requirements.txt
