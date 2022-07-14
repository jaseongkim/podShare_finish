from flask import Flask, render_template, request, jsonify #기본 라이브러리들
from pymongo import MongoClient #디비 연결 라이브러리
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.u82lpnm.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.db8bteam4
app = Flask(__name__)

#app.py > podcastPage card_num 요청
#card_num int 자료형 변경
