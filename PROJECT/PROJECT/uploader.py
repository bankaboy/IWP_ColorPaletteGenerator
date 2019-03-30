from flask import Flask, render_template, request, flash, request, redirect, url_for
from werkzeug import secure_filename
from image_kmeans import color_palette
import os

#file_folder = '~/Desktop/COLLEGE/SECOND_YEAR/FOURTH_SEMESTER/CSE 3002 - INTERNET AND WEB PROGRAMMING/PROJECT/static'
app = Flask(__name__)

@app.route('/')
def renderHome():
 return render_template('img_submit.html')
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
 if request.method == 'POST':
   f = request.files['file']
   final_colors = color_palette(f.filename)
   file_name = secure_filename(f.filename)
   #os.path.join((file_folder),f.filename)
   f.save(secure_filename(f.filename))
   page_start = '''
<!DOCTYPE html>
<html>
<head>
<title>COLORS IN THE PICTURE</title>
<style>

body {
background-color : grey;
}

</style>
</head>
<body>
<h3> The Final Colors are </h3><br>
<div>
'''
   page_end = '''
   </div>
   </body>
   </html>
   '''
   for i in range(len(final_colors)):
       page_start = page_start + final_colors[i] + '<table width ="400" bgcolor="'+final_colors[i]+'"><tr><td></td></tr></table>' +'<br>'
  #picture = '''<img src='/static/"+file_name+"' style='float:right;'></img>'''
   return page_start+"<img src='/static/"+file_name+"'></img>"+page_end

if __name__ == '__main__':
 app.run(debug = True)

