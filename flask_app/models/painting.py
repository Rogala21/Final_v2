from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers.dashboard import session
from flask import flash 

db = "artists_paintings_db"

class painting: 
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.painter_id = data['painter_id']
        self.painter = data['painter']
        self.number_of_sold = 0
        self.buy_sell = 'buy'

    @classmethod
    def new_painting(cls, data):
        query = "INSERT INTO artists_paintings_db.paintings (title, description, price, quantity, painter_id, painter) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(painter_id)s, %(painter)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def edit_painting(cls, data):
        query = "UPDATE artists_paintings_db.paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, painter_id = %(painter_id)s, painter = %(painter)s WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM artists_paintings_db.paintings;"
        results = connectToMySQL(db).query_db(query)
        paintings = []
        for painting in results:
            paintings.append(cls(painting))
        return paintings

    @classmethod
    def get_painting(cls, id):
        query = "SELECT * FROM artists_paintings_db.paintings LEFT JOIN artists_paintings_db.user_own_painting ON id = painting_id WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        painting = cls(results[0])
        if results[0]['user_id'] != None:
            painting.number_of_sold = len(results)
        for i in results:
            print(i, "i")
            if i['user_id'] == session['user_id']:
                painting.buy_sell = 'sell'
        return painting

    @classmethod
    def buy_painting(cls, data):
        query = "INSERT INTO artists_paintings_db.user_own_painting (user_id, painting_id) VALUES ( %(user_id)s, %(painting_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def sell_painting(cls, data):
        query = "DELETE FROM artists_paintings_db.user_own_painting WHERE user_id = %(user_id)s AND painting_id = %(painting_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_all_paintings_owned(cls, id):
        query = "SELECT * FROM artists_paintings_db.paintings JOIN artists_paintings_db.user_own_painting ON id = painting_id WHERE user_id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        paintings = []
        for painting in results:
            paintings.append(cls(painting))
        return paintings

    @classmethod
    def delete_owned_paintings(cls, id):
        query = "DELETE FROM artists_paintings_db.user_own_painting WHERE painting_id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return results

    @classmethod
    def delete_painting(cls, id):
        query = "DELETE FROM artists_paintings_db.paintings WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return results

    @staticmethod
    def check_stats_painting(painting):
        is_valid = True 
        if len(painting['title']) < 2:
            flash(u"Enter a Title")
            is_valid = False
        if int(painting['price']) < 1:
            flash(u"Price Needs to be higher")
            is_valid = False
        if int(painting['quantity']) < 1:
            flash(u"Quantity Needs to be higher")
            is_valid = False
        if len(painting['description']) < 10:
            flash(u"Needs a longer description")
            is_valid = False
        return is_valid