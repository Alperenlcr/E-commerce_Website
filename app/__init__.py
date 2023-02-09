from turtle import pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, create_engine, null, desc
from werkzeug import exceptions

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:467843.@127.0.0.1/computer_db?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
conn_obj = create_engine('mysql://root:467843.@127.0.0.1/computer_db?charset=utf8mb4')
db = SQLAlchemy(app=app)

from app.core import *
from app.db_models import *


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        data = Computer.query.all()
        data_query = Computer.query
        msg = ""
        # hangi POST ile istek geldigini anlamak icin try-except yapisi
        try:
            request.form['Sort by Rating']
            msg = 'Sort by Rating'
        except exceptions.BadRequestKeyError:
            try:
                request.form['Sort by Price Descending']
                msg = 'Sort by Price Descending'
            except exceptions.BadRequestKeyError:
                try:
                    request.form['Sort by Price Ascending']
                    msg = 'Sort by Price Ascending'
                except exceptions.BadRequestKeyError:
                    try:
                        request.form['Scrap']
                        msg = 'Scrap'
                    except exceptions.BadRequestKeyError:
                        try:
                            request.form['PriceFilter']
                            msg = 'PriceFilter'
                        except exceptions.BadRequestKeyError:
                            try:
                                request.form['RatingFilter']
                                msg = 'RatingFilter'
                            except exceptions.BadRequestKeyError:
                                try:
                                    request.form['Search']
                                    msg = 'Searching is done'
                                except exceptions.BadRequestKeyError:
                                    msg == "Refreshed"
        # istege gore islemler
        if msg == 'Scrap':
            scraper()
            msg = "Scrapping is done"
        elif msg == 'Sort by Price Ascending':
            msg = "Sorted by Price Ascending"
            data = conn_obj.execute("SELECT * FROM computer ORDER BY Price")
        elif msg == 'Sort by Price Descending':
            msg = "Sorted by Price Descending"
            data = conn_obj.execute("SELECT * FROM computer ORDER BY Price DESC")
        elif msg == 'Sort by Rating':
            msg = "Sorted by Rating"
            data = conn_obj.execute("SELECT * FROM computer ORDER BY Rating DESC")
        elif msg == 'PriceFilter':
            if request.form['MaxPrice'] != '':
                data_query = data_query.filter(Computer.Price < int(request.form['MaxPrice']))
            if request.form['MinPrice'] != '':
                data_query = data_query.filter(Computer.Price > int(request.form['MinPrice']))
            data = data_query.all()
        elif msg == 'RatingFilter':
            if request.form['MaxRating'] != '':
                data_query = data_query.filter(Computer.Rating < int(request.form['MaxRating']))
            if request.form['MinRating'] != '':
                data_query = data_query.filter(Computer.Rating > int(request.form['MinRating']))
            data = data_query.all()
        elif msg == "Searching is done":
            # data = data_query.filter(Computer.Title.ilike(f"%{request.form['SearchQuery']}%")).all()
            data = list(filter(lambda x: request.form['SearchQuery'].lower().replace(" ", "") in (x.Title+x.SiteName).lower().replace(" ", ""), data))
        elif msg == "Refreshed":
            pass
        else: #more info
            for k,v in request.form.to_dict(flat=False).items():
                item_page(k)

        return render_template("index.html", data=data, message=msg)
    data = Computer.query.all()
    return render_template("index.html", data=data)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        msg = ""
        # hangi POST ile istek geldigini anlamak icin try-except yapisi
        try:
            request.form['Add']
            msg = 'Add'
        except exceptions.BadRequestKeyError:
            try:
                request.form['Update']
                msg = 'Update'
            except exceptions.BadRequestKeyError:
                msg = 'Remove'

        # istege gore islemler
        if msg == 'Add':
            print("Add button")
            item = {
                    'Title':request.form['Title'],
                    'Price':request.form['Price'],
                    'Rating':request.form['Rating'],
                    'Ram':request.form['Ram'],
                    'ScreenSize':request.form['ScreenSize'],
                    'SiteName':request.form['SiteName'],
                    'Url':request.form['Url'],
                    }
            add_item_to_db(item)
        elif msg == 'Update':
            if type(request.form['value']) == str:
                value = request.form['value'].replace("\"", "")
            else:
                value = request.form['value']
            update_item_from_db(is_item_in_db(request.form['Title']), {request.form['key']:value})
            print("Update button")
        else:
            remove_item_from_db(request.form['Title'])
            print("Remove button")
    return render_template("admin.html")




@app.route("/<query>", methods=["GET", "POST"])
def item_page(query):
    if query != 'favicon.ico' and query != 'Refreshed':
        table_data = []
        items = Computer.query.all()
        item = items[[x.Title.replace("\"", "") for x in items].index(query.replace("\"", ""))]

        # scraping product info table according to siteName
        response = requests.get(item.Url, headers=headers)      # data for a page
        if item.SiteName == "HepsiBurada":
            soup = BeautifulSoup(response.content, 'html.parser')
            table_data.append(soup.find('div', {'id':'productTechSpecContainer'}))
        elif item.SiteName == "N11":
            soup = BeautifulSoup(response.content, 'html.parser')
            table_data.append(soup.find('div', {'class':'unf-prop', 'id':'unf-prop'}))
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            table_data.append(soup.find('ul', {'class':'detail-attr-container'}))

        return render_template('item_page_html.html', item=item, table_data=table_data)
    return render_template('item_page_html.html', item=[], table_data=[])


from app.flask_cli import create_database
