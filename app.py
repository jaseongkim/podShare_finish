from flask import Flask, render_template, request, jsonify  # 기본 라이브러리들
from pymongo import MongoClient  # 디비 연결 라이브러리
import certifi
import hashlib
import datetime
import jwt

SECRET_KEY = 'SPARTA'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.u82lpnm.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.db8bteam4
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signchange')
def signchange():
    id = 'hash'
    user = db.account.find_one({'id': id})
    print(user)

    return render_template('signchange.html', user=user)


@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/api/login', methods=['POST'])
def login_post():
    userId_receive = request.form['userId_give']
    userPw_receive = request.form['userPw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(userPw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.account.find_one({'id': userId_receive, 'password': pw_hash})

    print(userId_receive, userPw_receive , pw_hash, result)

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
    # JWT 토큰에는, payload와 시크릿키가 필요합니다.
    # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
    # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
    # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.

        payload = {
            'id': userId_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        print(token)

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': "아이디/비밀번호가 일치하지 않습니다."})

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def signup_post():
    id = request.form['id']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']

    doc = {
        'id': id,
        'password': password_hash,
        'email': email,
        'phone': phone,
        'gender': gender
    }

    db.account.insert_one(doc)

    return jsonify({'msg': '회원가입 성공.'})


@app.route('/dupcheck', methods=["POST"])
def dupCheck():
    id = request.form['id']
    print(id)
    if db.account.find_one({'id': id}):
        return jsonify(({'msg': '1'}))
    else:
        return jsonify(({'msg': '0'}))


@app.route('/deleteaccount', methods=["POST"])
def deleteAccount():
    id = request.form['id']

    db.account.delete_one({'id': id})

    return jsonify(({'msg': '탈퇴 완료.'}))


@app.route('/modifyaccount', methods=["POST"])
def modifyAccount():
    id = request.form['id']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']

    print(id, password, email, phone)

    user = db.account.find_one({'id': id})

    print(user)
    print(user['password'], user['email'], user['phone'])

    if password != '':
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if password_hash == user['password']:
            return jsonify(({'msg': '1'}))
        else:
            db.account.update_one({'id': id}, {'$set': {'password': password_hash}})

    if email != '':
        if email == user['email']:
            return jsonify(({'msg': '2'}))
        else:
            db.account.update_one({'id': id}, {'$set': {'email': email}})

    if phone != '':
        if phone == user.phone:
            return jsonify(({'msg': '3'}))
        else:
            db.account.update_one({'id': id}, {'$set': {'phone': phone}})

    return jsonify(({'msg': '수정 완료.'}))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
