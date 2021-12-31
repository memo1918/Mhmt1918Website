from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from Analyzer import Analyzer



uploadFolder = './FirstProject/uploads/'
ALLOWED_EXTENSIONS = {'txt','csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = uploadFolder 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
#line 15 is for preventing an error
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize the databse
db = SQLAlchemy(app)

#Create db model
class main(db.Model):
    #you can add columns here like this
    id = db.Column(db.Integer,primary_key=True)
    
    #returns when we add something
    def __repr__(self):
        return "Id" % self.id
  
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/',methods=['GET'])
def index():
    return redirect('home')

@app.route('/home',methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/about",methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/wordAnalyze",methods=['GET','POST'])
def wordAnalyze():
    if request.method == 'POST':
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = "tempFile."+filename.split(".")[1]
            file.save(uploadFolder+filename)
            
            tempdata = Analyzer(filename,uploadFolder).wordCounter()
            tempdata= tempdata["Count"].to_json()

            return render_template('wordAnalyze.html',tempdata=tempdata)

    return render_template('wordAnalyze.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105,debug=True)