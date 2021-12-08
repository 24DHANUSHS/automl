from flask import Flask,flash, render_template, request, redirect, url_for, session,Response,flash,jsonify,json
import os
import pandas as pd
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'your secret key'
@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        project_name=request.form['pname']
        type=request.form['type']
        file=request.files['file']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(secure_filename(file.filename))
        session['name']=project_name
        session['type']=type
        session['file']=filename
        return redirect(url_for('home'))


    else:
        return render_template('login.html')


@app.route('/home',methods=['POST','GET'])
def home():
    if 'file' in session:
        filename=session.get('file')
        project_name=session.get('name')
        type=session.get('type')
        df=pd.read_csv(filename)#get the csv data
        cols=df.columns#csv columns
        cols_type=list(df.dtypes)
        #print(type(cols_type))
        #print(cols_type)
        row_len=[]
        nan_len=[]
        for i in cols:#count the null and correct values
            lenght=df[i].count()
            nan_lenght=df[i].isnull().sum()
            nan_len.append(nan_lenght)
            row_len.append(lenght)

        sum1=[] #get the correct and null values
        sum1.append(sum(row_len))
        sum1.append(sum(nan_len))
        data =df
        len1=row_len[0]+nan_len[0]
        return render_template('index.html',cols=cols,cols_type=cols_type,row_len=row_len,nan_len=nan_len,len=len(cols),sum1=sum1,data=data,len1=len1,project_name=project_name,type=type)







if __name__ == "__main__":
    app.run(debug=True)