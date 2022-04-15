import os
from flask import Flask, request, render_template, send_from_directory 
app = Flask(__name__)

gUploadsDir = "uploads"

class FileSystemLevel():
    def __init__(self, path, fileList):
        self.path = path
        self.fileList = fileList

class FileSystemNode():
   def __init__(self, name, link, isDir):
      self.name = name
      self.link = link
      self.isDir = isDir

def GenerateFileLevel(path):
   fullPath = os.path.join(gUploadsDir, path)
   fileList = []
   try: files = os.listdir(fullPath)
   except OSError:
      pass
   else:
      for name in files:
         entry = os.path.join(fullPath, name)
         relativeEntry = os.path.join(path, name)
         if os.path.isdir(entry):
            fileList.append(FileSystemNode(name, f"{name}/", True))
         else:
            fileList.append(FileSystemNode(name, f"/download/{relativeEntry}", False))
   return FileSystemLevel(path, fileList)

def RenderPage(path = ""):
   return render_template('files.html', fileSystemLevel=GenerateFileLevel(path))

@app.route('/')
def render_main_page():
   return RenderPage()

@app.route('/<path:directory>')
def render_child_page(directory):
   return RenderPage(directory)
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(gUploadsDir + "/" + f.filename)
      return 'File was uploaded successfully!'

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
   uploadsPath = os.path.join(app.root_path, gUploadsDir)
   return send_from_directory(uploadsPath, filename)
		
if __name__ == '__main__':
   app.run(debug = True)