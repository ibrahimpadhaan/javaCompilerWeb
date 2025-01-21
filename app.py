from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def code():
    code = request.form['code']
    name = request.form['class_name']
    classname = name+".java"
    with open(classname, 'w') as temp:
        temp.write(code)

    try:
       compiled =  subprocess.run(['javac', classname], capture_output=True)
       subprocess.run(['rm', name+'.java'])
    except Exception as e:
        return "<pre>"+str(e)+"</pre>"

    try:
        result = subprocess.run(['java', name], capture_output=True, text=True)
        subprocess.run(['rm', name+'.class'])
        return "<pre>"+result.stdout+"</pre>"
    except Exception as f:
        return "<pre>"+str(f)+"</pre>"


if __name__ == '__main__':
    app.run(debug=True)
