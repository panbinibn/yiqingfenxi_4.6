from flask import Flask,render_template,request
from flask import jsonify
import utils


app = Flask(__name__)


@app.route('/')
def hello_world():
   # return 'Hello World!'
    return render_template("hello.html")

@app.route('/main')
def china_page():
    return render_template("main.html")

@app.route('/ajax',methods=["get","post"])
def hello_ajax():
    name = request.values.get("name")
    score = request.values.get("score")
    print(f"name:{name},score:{score}")
    return 'Add oil!'

@app.route("/time")
def get_time():
    return utils.get_time()


@app.route("/c1")
def get_c1_data():
    data=utils.get_c1_data()
    return jsonify({"confirm":data[0],"suspect":data[1],"heal":data[2],"dead":data[3]})

@app.route("/c2")
def get_c2_data():
    res=[]
    for tup in utils.get_c2_data():
        print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route("/l1")
def get_l1_data():
    data=utils.get_l1_data()
    day,confirm,suspect,heal,dead=[],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})

@app.route("/l2")
def get_l2_data():
    data=utils.get_l2_data()
    day,confirm_add,suspect_add=[],[],[]
    for a,b,c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})

@app.route("/r1")
def get_r1_data():
    data=utils.get_r1_data()
    city,confirm=[],[]
    for a,b in data:
        city.append(a)
        confirm.append(b)
    return jsonify({"city":city,"confirm":confirm})

@app.route("/r2")
def get_r2_data():
    data=utils.get_r2_data()
    country,confirm,dead=[],[],[]
    for a,b,c in data:
        country.append(a)
        confirm.append(b)
        dead.append(c)
    return jsonify({"country":country,"confirm":confirm,"dead":dead})

@app.route("/center")
def get_all_data():
    res=[]
    for tup in utils.get_all_data():
        print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})

@app.route("/form")
def get_form_data():
    res=[]
    for tup in utils.get_form_data(): #sql.get_form_data()是元组里面有多个元组
        print(tup)  #tup格式：元组
        res.append({"country":tup[0],"confirm":int(tup[1]),"dead":int(tup[2])})
    return jsonify({"data":res})

import json
import flask
import decimal

#g改写jsonencoder方法
class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)
app.json_encoder = MyJSONEncoder


if __name__ == '__main__':

    app.run()
