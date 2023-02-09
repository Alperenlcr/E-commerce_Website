# Oluşturulacak database tablolari ve fonksiyonlari burada tutuluyor
from app import db, conn_obj

"""
Table content:  Title, Price, Rating, Ram, ScreenSize, SiteName, Url
"""

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(256), nullable=True)
    Price = db.Column(db.Integer, nullable=True)
    Rating = db.Column(db.Float, nullable=True)
    Ram = db.Column(db.Integer, nullable=True)
    ScreenSize = db.Column(db.Float, nullable=True)
    SiteName = db.Column(db.String(256), nullable=False)
    Url = db.Column(db.String(256), nullable=False)


# databasede item var mi diye kontrol edip eger yoksa ekler
def add_item_to_db(item):
    if is_item_in_db(item['Url']) == -1:
        id = conn_obj.execute("INSERT INTO  `computer_db`.`computer` (`Title`,`Price`,`Rating`,`Ram`,`ScreenSize`,`SiteName`,`Url`)\
                 VALUES('{}' ,'{}','{}','{}','{}','{}','{}')".format(
                    item['Title'], item['Price'], item['Rating'], item['Ram'], item['ScreenSize'], item['SiteName'], item['Url']
                 ))


# admin sayfasinda girilen title ile item db'de var mi diye bakilip id ile bu fonksiyon cagirilir
# degistirilmek istenen veri ile komut olusturulur ve db'de degisiklik yapilir
def update_item_from_db(id, update_dict):
    query = "UPDATE computer SET"
    for key, value in update_dict.items():
        query += " {} = \"{}\",".format(key, value)
    query = query[:-1]
    query += " WHERE id = {}".format(id)
    conn_obj.execute(query)


# searchs item in database and returns id
# if item is not in database then returns -1
def is_item_in_db(Title):
    rows = list(conn_obj.execute("SELECT * FROM computer"))
    ids_name = [[row[0], row[1]] for row in rows]
    for row in ids_name:
        if Title == row[1]:
            return row[0]
    return -1


# title'i verilen item db'de aranir var ise id'si ile db'den silinir
def remove_item_from_db(Title):
    id = is_item_in_db(Title)
    if id == -1:
        return False
    conn_obj.execute("DELETE FROM computer WHERE id={}".format(id))
    return True    
