from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from Analyzer import Analyzer

uploadFolder = './Mhmt1918Website/uploads/'
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
        lenght = int(request.form.get("lenght"))
        maxOutput = int(request.form.get("maxOutput"))
        if maxOutput > 25: maxOutput = 25

        analyzer = Analyzer(uploadFolder,lenght,maxOutput)
  
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']     
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = "tempFile."+filename.split(".")[1]
            file.save(uploadFolder+filename)
            

            analyzer.filename = filename
            analyzer = analyzer.wordCounter()
            tempdata = analyzer["Count"].to_json()

            return render_template('wordAnalyze.html',tempdata=tempdata)

        else:
            data = request.form.get('text_area')

            analyzer = analyzer.wordCounter(data)
            tempdata= analyzer["Count"].to_json()

            return render_template('wordAnalyze.html',tempdata=tempdata)

    return render_template('wordAnalyze.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105,debug=True)