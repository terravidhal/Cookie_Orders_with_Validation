from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re  # the regex module



class Cookies:
    DB = 'cookies_db'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.num_of_boxes = data["num_of_boxes"]
        self.created_at = data["created_at"].strftime("%B %drd %Y %H:%M:%S %p")
        self.updated_at = data["updated_at"].strftime("%B %drd %Y %H:%M:%S %p")

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cookies;"
        results = connectToMySQL(cls.DB).query_db(query)
        cookies_Arr = []
        for one_cookie in results:
            #print('one_cookie++++++++',one_cookie)
            cookies_Arr.append(cls(one_cookie))
            #print(cls(one_cookie))
        return cookies_Arr
    

    @classmethod
    def create_cookie(cls, datas):
        query = "INSERT INTO cookies (name, type, num_of_boxes, created_at, updated_at) VALUES (%(name)s, %(type)s, %(nboxes)s, NOW(), NOW());"
        results = connectToMySQL(cls.DB).query_db(query, datas)
        cookie_id_created = results
        return cookie_id_created 

    # READ
    # ONE elt
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM cookies WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    # UPDATE
    @classmethod
    def update(cls,data):
        query = """UPDATE cookies 
                SET name=%(name)s, type=%(type)s, num_of_boxes=%(nboxes)s , updated_at = NOW() 
                WHERE id = %(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    

    # DELETE        
    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM cookies WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    

    # VALIDATE COOKIE INFOS
    @staticmethod
    def validate_cookie_infos(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Invalid user name !")
            is_valid = False
        if len(data['type']) < 2:
            flash("Invalid cookie type !")
            is_valid = False
        if not data["nboxes"] or int(data["nboxes"]) < 0:
            is_valid = False
            flash("The number of boxes must be positive !")

        return is_valid
    

    # VALIDATE UNIQUE USER NAME
    @classmethod
    def is_unique_user(cls, data):
        query = "SELECT name FROM cookies;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        is_valid = True
        for elt in results:
            #print(elt)  
            if elt["name"] == data["name"]:
                flash("user name already exists")
                is_valid = False
               
        return is_valid
    

    # VALIDATE UNIQUE USER NAME PAGE UPDATE
    @classmethod
    def is_unique_user_update(cls, data, cookie):
        query = "SELECT name FROM cookies;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        is_valid = True
        last_value_name = cookie.name
        new_value_name = data["name"] 
        for elt in results:
            #print(elt)  
            if elt["name"] == data["name"]:
                flash("user name already exists")
                is_valid = False
        if last_value_name == new_value_name: 
            is_valid = True
               
        return is_valid
    
    