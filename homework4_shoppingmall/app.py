from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 5000)  # mongoDB는 5000 포트로 돌아갑니다.
db = client.order_sheet  # 'order_sheet'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_order():
    order_name_receive = request.form['name_give']
    order_count_receive = request.form['quantity_give']
    order_address_receive = request.form['address_give']
    order_phone_receive = request.form['phone_number_give']

    order = {
        'order_name': order_name_receive,
        'order_count': order_count_receive,
        'order_address': order_address_receive,
        'order_phone': order_phone_receive
    }

    db.orders.insert_one(order)
    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 접수되었습니다.'})


@app.route('/orders', methods=['GET'])
def read_orders():
    orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'order': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
