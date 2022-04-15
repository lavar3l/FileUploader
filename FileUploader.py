from flask import Flask, request, render_template 
app = Flask(__name__)

@app.route('/')
def render_page():
   return render_template('files.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("uploads/" + f.filename)
      return 'File was uploaded successfully!'
		
if __name__ == '__main__':
   app.run(debug = True)