from functools import wraps
from flask import request
from operator import eq, ne
import jwt
from src.evn.appEnvirment import *

def authAdmin(func):
  """
  admin 등급만 접근가능
  """
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    auth = request.headers.get('Authorization')  # Authorization 헤더로 담음
    
    if eq("", auth):
      return {
            "result": "not auth A"
        }
    
    try:
        data = jwt.decode(auth, JWT_PASSWORD, algorithms=JWT_ALGORITHMS)
    except Exception as e:
        return {
                "result": False,
                "message": "오류가 발생하였습니다. A"}
        
    level = int(data["level"])
    
    ## admin만 가능하다.
    if level < 99:
      return {
                "result": False,
                "message": "access denide A"}

    return func(self, *args, **kwargs)                               
  return wrapper

def authManager(func):
  """
  매니저 등급 이상만 접근가능
  """
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    auth = request.headers.get('Authorization')  # Authorization 헤더로 담음
    
    if not auth :
      return {
            "result": "not auth M"
        }
    
    try:
        data = jwt.decode(auth, JWT_PASSWORD, algorithms=JWT_ALGORITHMS)
    except Exception as e:
        return {
                "result": False,
                "message": "오류가 발생하였습니다. M"}
        
    level = int(data["level"])
    
    ## 매니저만 가능하다.
    if level < 80:
      return {
                "result": False,
                "message": "access denide M"}
            
    return func(self, *args, **kwargs)                               
  return wrapper

def authEmployee(func):
  """
  직원 등급 이상만 접근가능
  """
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    auth = request.headers.get('Authorization')  # Authorization 헤더로 담음
    
    if not auth :
      return {
            "result": "not auth E"
        }
    
    try:
        data = jwt.decode(auth, JWT_PASSWORD, algorithms=JWT_ALGORITHMS)
    except Exception as e:
        return {
                "result": False,
                "message": "오류가 발생하였습니다. E"}
        
    level = int(data["level"])
    
    employeeIdx = int(data["employee_idx"])
    
    ## 직원 이상만 가능하다.
    if level < 50:
      return {
                "result": False,
                "message": "access denide E"}
            
    return func(self, *args, **kwargs)                               
  return wrapper