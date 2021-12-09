from flask import Flask,flash, render_template, request, redirect, url_for, session,Response,flash,jsonify,json
import os
import statistics
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

        #central tendency
        #mean-median-mode
        ct=[]
        c=[]
        for i in cols:
            if df[i].dtype=='object':
                c.append('Str')
            else:
                c.append(round(df[i].mean(),2))
        ct.append(c)
        #median
        c=[]
        for i in cols:
            if df[i].dtype == 'object':
                c.append('Str')
            else:
                c.append(round(df[i].median(),2))
        ct.append(c)

        #mode
        c = []
        for i in cols:
            if df[i].dtype == 'object':
                c.append('Str')
            else:
                c.append(statistics.mode(df[i]))
        ct.append(c)
        print(float('nan'))

        return render_template('index.html',cols=cols,cols_type=cols_type,row_len=row_len,nan_len=nan_len,len=len(cols),sum1=sum1,data=data,len1=len1,project_name=project_name,type=type,ct=ct,na=float('nan'))
    else:
        return render_template('login.html')


@app.route('/replace_nan',methods=['POST','GET'])
def replace_nan():
    if 'file' in session:
        type=request.args.get('type')
        cols=request.args.get('cols')
        # data change code

        filename = session.get('file')
        df = pd.read_csv(filename)

        if type=='mean':
            df[cols].fillna(value=round(df[cols].mean(),2),inplace=True)

        elif type=='median':
            df[cols].fillna(value=round(df[cols].median(),2),inplace=True)
        elif type=='mode':
            df[cols].fillna(value=statistics.mode(df[cols]), inplace=True)

        df.to_csv('{0}'.format(filename),index=False)
        flash("you are successfuly logged in")
        return redirect(url_for('home'))

@app.route('/drop_dummies',methods=['POST','GET'])
def drop_dummies():
    if 'file' in session:
        type=request.args.get('type')
        cols=request.args.get('cols')
        filename = session.get('file')
        df = pd.read_csv(filename)
        if type=='drop':

            df.drop([cols], axis=1,inplace=True)
            df.to_csv('{0}'.format(filename), index=False)
            flash("you are successfuly logged in")

            return redirect(url_for('home'))
        elif type=='dummies':
            df = pd.get_dummies(df, columns=[cols],drop_first=True)
            df.to_csv('{0}'.format(filename), index=False)
            return redirect(url_for('home'))
        elif type=='dummies1':
            df = df[df[cols].notna()]
            df.to_csv('{0}'.format(filename), index=False)
            return redirect(url_for('home'))









if __name__ == "__main__":
    app.run(debug=True)