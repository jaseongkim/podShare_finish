from flask import Flask, render_template, request, jsonify #기본 라이브러리들
from pymongo import MongoClient #디비 연결 라이브러리
import certifi
import detail

import requests
from bs4 import BeautifulSoup

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.u82lpnm.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.db8bteam4
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

#이재혁님 프로그램
@app.route('/detail')
def podcast_detial():
    card_num = request.args.get('card_num')
    detailget = detail.podcastPage(card_num)
    print(detailget)
    return render_template('detail.html',detailget=detailget)

#김은경님 프로그램
@app.route("/podcast", methods=["POST"])
def podcast_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    url = 'https://www.podbbang.com/channels/12548/episodes/24396721'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one('meta[property="og:image"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']

    doc = {
        'title':title,
        'image':image,
        'comment':comment_receive
    }
    db.podshare.insert_one(doc)

    return jsonify({'msg':'등록 완료!'})

@app.route("/podcast", methods=["GET"])
def podcast_get():
    podcast_list = list(db.podshare.find({}, {'_id': False}))
    return jsonify({'all_podcast':podcast_list})

@app.route('/api/delete', methods=['POST'])
def deleteRow():
    comment_receive = request.form['comment_give']
    db.podshare.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
