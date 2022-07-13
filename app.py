from flask import Flask, render_template, request, jsonify, session, redirect, url_for  # 기본 라이브러리들
from pymongo import MongoClient  # 디비 연결 라이브러리
import certifi
import detail

import requests
from bs4 import BeautifulSoup
import hashlib
import datetime
import jwt
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

SECRET_KEY = 'SPARTA'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.u82lpnm.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.db8bteam4
app = Flask(__name__)

@app.route('/')
def home():

    token_receive = request.cookies.get('mytoken')
    return render_template('index.html', token_receive = token_receive)

#이재혁님 프로그램
@app.route('/detail')
def podcast_detial():

    card_num = request.args.get('card_num')
    detailget = detail.podcastPage(card_num)
    print(detailget)
    return render_template('detail.html', detailget = detailget, card_num=card_num)

#김은경님 프로그램
@app.route("/podcast", methods=["POST"])
def podcast_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    url = 'https://www.podbbang.com/channels/12548/episodes/24396721'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get(url_receive)

    soup = BeautifulSoup(data.text, 'html.parser')
    soup_1 = BeautifulSoup(driver.page_source, 'html.parser')
    
    image = soup.select_one('meta[property="og:image"]')['content']
    chan_title = soup_1.select_one('#__layout > section > section.app-container > section > section.content-wrapper > a').get_text().strip()
    epi_title = soup.select_one('meta[property="og:title"]')['content']
    description = soup.select_one('meta[property="og:description"]')['content']
    # new_des = re.sub(r"\s","",description)
    date = soup_1.select_one('#__layout > section > section.app-container > section > section.content-wrapper > section.misc > span.published-at > b').get_text()
    playtime = soup_1.select_one('#__layout > section > section.app-container > section > section.content-wrapper > section.misc > span.duration > b').get_text()
    like = soup_1.select_one('#__layout > section > section.app-container > section > section.content-wrapper > section.misc > span.likes > b').get_text()
    audio_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div/section/section[1]/section/section[1]/section[3]/button')
    audio_btn.click()
    driver.implicitly_wait(3)
    audio = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/section[2]/audio').get_attribute('src')
    driver.quit()
    card_num = url_receive.split("/")[-1]

    doc = {
        'comment':comment_receive,
        'chan_title': chan_title,
        'epi_title':epi_title,
        'image':image,
        'description':description,
        'date':date,
        'playtime':playtime,
        'like':like,
        'audio':audio,
        'card_num':card_num
    }

    db.podshare.insert_one(doc)


    return jsonify({'msg':'등록 완료!'})

@app.route("/podcast", methods=["GET"])
def podcast_get():

    podcast_list = list(db.podshare.find({}, {'_id': False}))

    return jsonify({'all_podcast':podcast_list})

@app.route('/api/delete', methods=['POST'])
def deleteRow():

    num_receive = request.form['num_give']

    db.podshare.delete_one({'card_num': num_receive})

    return jsonify({'msg': '삭제 완료!'})


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


@app.route('/signup/dupcheck', methods=["POST"])
def dupCheck():
    id = request.form['id']

    if db.account.find_one({'id': id}):
        return jsonify(({'msg': '1'}))
    else:
        return jsonify(({'msg': '0'}))


@app.route('/signchange')
def signchange():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('signchange.html', id=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signin"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signin"))


@app.route('/signchange/modify', methods=["POST"])
def modifyAccount():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload['id']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        print(id, password, email, phone)

        user = db.account.find_one({'id': id})

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
            if phone == user['phone']:
                return jsonify(({'msg': '3'}))
            else:
                db.account.update_one({'id': id}, {'$set': {'phone': phone}})

        return jsonify(({'msg': '수정 완료.'}))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("signin"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("signin"))


@app.route('/signchange/delete', methods=["POST"])
def deleteAccount():
    id = request.form['id']

    db.account.delete_one({'id': id})

    return jsonify(({'msg': '탈퇴 완료.'}))

##################################################################################################
# 로그인 / 댓글 시작
# 로그인
@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/api/login', methods=['POST'])
def login_post():
    userId_receive = request.form['userId_give']
    userPw_receive = request.form['userPw_give']

    pw_hash = hashlib.sha256(userPw_receive.encode('utf-8')).hexdigest()

    result = db.account.find_one({'id': userId_receive, 'password': pw_hash})

    if result is not None:

        payload = {
            'id': userId_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                                                        #배포시 캐시 유지 1시간
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': "아이디/비밀번호가 일치하지 않습니다."})


#  댓글
@app.route("/reply", methods=["GET"])
def reply_get():

    all_list = list(db.replydb.find({}, {'_id': False}))

    return jsonify({'list': all_list})

@app.route("/reply", methods=["POST"])
def reply_post():

    token_receive = request.cookies.get('mytoken')
    reply_receive = request.form['reply_give']
    card_receive = request.form['card_give']

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.account.find_one({"id": payload['id']})

        doc = {
            "id" : user_info["id"],
            "reply": reply_receive,
            "card_num": card_receive
        }

        db.replydb.insert_one(doc)

        return jsonify({'msg':'등록 완료!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'msg': "로그인 시간이 만료되었습니다."})
    except jwt.exceptions.DecodeError:
        return jsonify({'msg': "로그인 정보가 없습니다."})


# 로그인 / 댓글 끝


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
