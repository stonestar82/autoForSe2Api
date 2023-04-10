import jwt
import bcrypt
from flask import request
from flask_restful import Resource, Api, fields
from src.utill.DBHelper import db_helper
from src.process.AuthProcess import AuthProcess
from src.utill.Decorator import *
from src.evn.appEnvirment import *
import random
from src.utill.AES256 import AES256

users = {}
        
class AuthLogin(Resource):
	"""
	직원 로그인
	"""
	def post(self):
		
		id = request.json['id']
		password = request.json['password']
		
		result = {}

		sql = "SELECT idx, name, level FROM employee WHERE id = %s AND passwd = SHA2(%s, 256);"
		
		pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
		param = (id, password)
		
		with db_helper.get_resource_rdb() as (cursor, _):
				cursor.execute(sql, param)
				result = cursor.fetchone()

		if not result:
			return {
				"result": False
			}
		else:
    
			## request에서 ip 가져오기
			ip = request.remote_addr
			

			## 로그인 히스토리 저장
			sql = "INSERT INTO employee_login_history VALUES(Null, %s, %s, 'auto', Now());"
   
			param = (result["idx"], ip)
    
			with db_helper.get_resource_rdb() as (cursor, _):
					cursor.execute(sql, param)
     
			## 랜덤 숫자 생성
			randomNumber = random.randint(1000000000, 9999999999)
   
			## 랜덤숫자중 2,5,6,10번째 숫자를 |로 변경
			kkk = str(randomNumber)
			kkk = kkk[:1] + "&" + kkk[2:4] + "x" + kkk[5:6] + "q" + kkk[7:9] + "#" + kkk[10:]

			## randomNumber 16자리로 맞추기
			kkk = kkk + "l^2rq@aij121"
			kkk = kkk[:16]
   
			## chip을 AES256으로 암호화
			aes = AES256(kkk)
   
			en = aes.encrypt(password)
   
			## 암호화키, 마지막 로그인 저장
			sql = "UPDATE employee SET chip_key = %s, last_login_date = now() WHERE idx = %s;"
			param = (en, result['idx'])

			with db_helper.get_resource_rdb() as (cursor, _):
					cursor.execute(sql, param)
       
			return {
				"result": True,
				"disit": randomNumber,
				"check": en,
				'Authorization': jwt.encode( {"employee_idx": result["idx"], 'id': id, "name": result["name"], 'level':result["level"]}, JWT_PASSWORD, algorithm=JWT_ALGORITHMS) # str으로 반환하여 return
			}


class Auth(Resource):
  
	def get(self):
		header = request.headers.get('Authorization')  # Authorization 헤더로 담음
		if header == None:
			return {
				"result": False,
				"message": "로그인후 이용하실 수 있습니다."
			}

		try:
			data = jwt.decode(header, JWT_PASSWORD, algorithms=JWT_ALGORITHMS)
		except Exception as e:
			data = {	"result": False,"message": "오류가 발생하였습니다." }
		
		return data, 200
  