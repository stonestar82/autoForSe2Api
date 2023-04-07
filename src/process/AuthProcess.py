from src.dao.AuthDao import AuthDao
from operator import eq, ne, truediv

class AuthProcess():

  def __init__(self) -> None:
    pass

  
  @staticmethod
  def putEmployee(employee):
    
    ## 관리자 등급으로는 변경 방지
    if (int(employee["level"]) > 80):
      return 0;
    
    AuthDao.updateEmployee(employee)
    
    return 1;
  
  @staticmethod
  def deleteEmployee(employee):

    if (int(employee["level"]) > 80):
      return 0;
    
    AuthDao.deleteEmployee(employee)
    
    return 1;
  
  
  @staticmethod
  def updatePassword(auth, params):
    return AuthDao.updateEmployeePassword(auth["employee_idx"], params)