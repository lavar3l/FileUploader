import os
from flask import Flask, request, render_template, send_from_directory 
app = Flask(__name__)

gUploadsDir = "uploads"

def GenerateFileTree(path):
    tree = dict(name = os.path.basename(path), children=[])
    try: fileList = os.listdir(path)
    except OSError:
        pass # Ignore errors
    else:
        for name in fileList:
            entry = os.path.join(path, name)
            if os.path.isdir(entry):
               tree['children'].append(GenerateFileTree(entry))
            else:
               tree['children'].append(dict(name = name))
    return tree

def RenderPage(path = gUploadsDir):
   return render_template('files.html', fileTree=GenerateFileTree(path))

@app.route('/')
def render_main_page():
   return RenderPage()

@app.route('/<path:directory>')
def render_child_page(directory):
   return RenderPage(gUploadsDir + "/" + directory)
	
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