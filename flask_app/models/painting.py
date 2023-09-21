from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user

class Painting:
    db = "Painting_App_Schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def create_painting(cls, data):
        query = "INSERT INTO paintings(title, description, price, user_id) VALUES(%(title)s, %(description)s, %(price)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_painting(cls, data):
        query = """
        UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def painting_validate(data):
        is_valid = True
        query = "SELECT * FROM paintings WHERE title = %(title)s;"
        results = connectToMySQL("Painting_App_Schema").query_db(query, data)
        if len(results) != 0:
            flash("")
            is_valid = False
        if len(data['title']) < 3:
            flash("Title must be atleast 3 characters.")
            is_valid = False
        if len(data['description']) < 5:
            flash("Description must be atleast 5 characters.")
            is_valid = False
        if data['price'] == '':
            flash("Price must not be empty.")
            is_valid = False
        return is_valid

    @classmethod
    def get_all_user_paintings(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"
        paintings = connectToMySQL(cls.db).query_db(query)
        results = []
        for painting in paintings:
            data = {
                'id': painting['users.id'],
                'first_name': painting['first_name'],
                'last_name': painting['last_name'],
                'email': painting['email'],
                'password': painting['password'],
                'created_at': painting['users.created_at'],
                'updated_at': painting['users.updated_at']
            }
            get_all_painting = cls(painting)
            get_all_painting.creator = user.Person(data)
            results.append(get_all_painting)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at']
        }
        get_painting = cls(results[0])
        get_painting.creator = user.Person(data)
        return get_painting

    @classmethod
    def get_a_painting(cls, data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])