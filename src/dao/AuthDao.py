from src.utill.DBHelper import db_helper
from operator import eq, ne

class AuthDao():

  def __init__(self) -> None:
    pass

  @staticmethod
  def selectEmployeeById(id):

    sql = "SELECT COUNT(1) AS count FROM employee WHERE id = %s;"        
    param = (id,)
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)
        result = cursor.fetchone()
      
    return int(result["count"])

  @staticmethod
  def insertEmployee(employee):

    sql = "INSERT INTO employee VALUES(NULL, %s, %s, %s, %s, SHA2(%s, 256), 'Y', NOW());"

    param = (employee['level'], employee['title'], employee['name'], employee['id'], employee['password'])
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)

    return 1

  @staticmethod
  def updateEmployee(employee):

    if eq(employee["update_password"], "Y"):      
      sql = "UPDATE employee SET level = %s, title = %s, passwd = SHA2(%s, 256), live = %s WHERE idx = %s;"
      param = (employee['level'], employee['title'], employee['password'], employee['live'], employee['idx'])
      
    else:
      sql = "UPDATE employee SET level = %s, title = %s, live = %s WHERE idx = %s;"
      param = (employee['level'], employee['title'], employee['live'], employee['idx'])
      
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)

    return 1

  @staticmethod
  def deleteEmployee(employee):

    """
    직원 삭제(실제 삭제 안함.)
    """
    sql = "UPDATE employee SET live = 'N' WHERE idx = %s;"

    param = (employee['idx'], )
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)

    return 1  
  
  @staticmethod
  def updateEmployeePassword(employee_idx, args):
    
    sql = "SELECT COUNT(1) AS count FROM employee WHERE idx = %s AND passwd = SHA2(%s, 256);"
    
    print(args)
    
    param = (employee_idx, args["ori_password"])
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)
        result = cursor.fetchone()
    
    print("updateEmployeePassword !!!!")
    count = int(result["count"])
    print(count)
    if  ne(1, count):
      return 0
    
    sql = "UPDATE employee SET passwd = SHA2(%s, 256) where idx = %s;"
    
    param = (args["new_password"], employee_idx)
    
    with db_helper.get_resource_rdb() as (cursor, _):
        cursor.execute(sql, param)
  
    return 1