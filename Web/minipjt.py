from flask import Flask
from flask import render_template
from flask import request
import requests
import pymysql

app = Flask(__name__)

@app.route('/')
def main_mlpjt():
    return render_template('index.html')

@app.route('/selectfile')
def select_file():
    return render_template('selectfile.html')

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['select']
        print(file.filename)
        if file.filename != '':
            save_file_name=file.filename
            file.save("./static/test/"+save_file_name)
    # 프로젝트 1 url = "https://minipjtcv.cognitiveservices.azure.com/customvision/v3.0/Prediction/cf594382-97ff-42df-bb81-4f864a258394/classify/iterations/Iteration1/image"
    url = "https://minipjtcv.cognitiveservices.azure.com/customvision/v3.0/Prediction/1200ec59-5fd4-402d-8c4f-d48e37967ecf/classify/iterations/Iteration1/image"
    headers = {'content-type': 'application/octet-stream', 'Prediction-Key': '8ce925f290e644a5bde8d48cfec9b09b'}
    response = requests.post(url, data=open("./static/test/"+save_file_name, "rb"), headers=headers)
    analysis = response.json()
    val = analysis['predictions'][0]['tagName']
    print(val)
    try:
        db = pymysql.connect(host='localhost', port=3306, db='minipjt', passwd='root', user='root', charset='utf8')
        cur = db.cursor()
        sql = "SELECT * FROM food WHERE foodname like '%"+val+"%' limit 1"
        cur.execute(sql)
        data_list = cur.fetchall()
        return render_template('graphfile.html', data_list=data_list)
    except Exception as e:
        print('Error :', e)
    finally:
        cur.close()
        db.close()
    return render_template('errorsearch.html')

@app.route('/temp')
def temp_file():
    return render_template('temp.html')

@app.route('/searchfile')
def search_file():
    return render_template('beforesearch.html')

@app.route('/searchresult', methods=['POST'])
def search_result():
    val = request.form['searchbar']
    print(val)
    try:
        db = pymysql.connect(host='localhost', port=3306, db='minipjt', passwd='root', user='root', charset='utf8')
        cur = db.cursor()
        sql = "SELECT * FROM food WHERE foodname like '%"+val+"%' OR regionmanufacturing like '%"+val+"%' OR foodcategory like '%"+val+"%' limit 20"
        cur.execute(sql)
        data_list = cur.fetchall()
        return render_template('searchresult.html', data_list=data_list)
    except Exception as e:
        print('Error :', e)
    finally:
        cur.close()
        db.close()
    return render_template('errorsearch.html')

@app.route('/detailed', methods=['POST'])
def detailed_result():
    val = request.form.get('detailed')
    print(val)
    try:
        db = pymysql.connect(host='localhost', port=3306, db='minipjt', passwd='root', user='root', charset='utf8')
        cur = db.cursor()
        sql = "SELECT * FROM food WHERE foodname like '%" + val + "%' limit 1"
        cur.execute(sql)
        data_list = cur.fetchall()
        return render_template('graphfile.html', data_list=data_list)
    except Exception as e:
        print('Error :', e)
    finally:
        cur.close()
        db.close()
    return render_template('errorsearch.html')

@app.route('/rangefile')
def range_file():
    return render_template('rangefile.html')

@app.route('/rangeselect', methods=['POST'])
def range_select():
    category_val = request.form.get('categories')
    sort_val = request.form.get('cp_item')
    range_val1 = request.form.get('rangeleft')
    range_val2 = request.form.get('rangeright')
    try:
        db = pymysql.connect(host='localhost', port=3306, db='minipjt', passwd='root', user='root', charset='utf8')
        cur = db.cursor()
        sql = "SELECT * FROM food WHERE "+category_val+" > "+str(range_val1)+" AND "+category_val+" < "+str(range_val2)+" ORDER BY "+category_val+" "+sort_val+" limit 20"
        print(sql)
        cur.execute(sql)
        data_list = cur.fetchall()
        return render_template('rangeresult.html', data_list=data_list)
    except Exception as e:
        print('Error :', e)
    finally:
        cur.close()
        db.close()
    return render_template('errorsearch.html')