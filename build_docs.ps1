$VENV_PATH="C:\VirtualEnvs\cascade"
$PROJECT_PATH="D:\GitHub\cascade"
cd $PROJECT_PATH
."$VENV_PATH\Scripts\activate.ps1"

sphinx-build -w "$PROJECT_PATH\logs\sphinx.log" -b html "$PROJECT_PATH\docs" "$PROJECT_PATH\docs-build"

# to run in a local browser
$PROJECT_PATH="D:\GitHub\cascade"
cd $PROJECT_PATH
$VENV_PATH="C:\VirtualEnvs\cascade"
."$VENV_PATH\Scripts\activate.ps1"
C:\Python310\python -m http.server --directory="$PROJECT_PATH\docs-build" 57921

# http://localhost:57921