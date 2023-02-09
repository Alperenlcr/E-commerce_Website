# Web Scrapping E-commerce Website with Flask
In order to gain practical experience building web applications from scratch, this project was developed. The task is to develop a web application that allows users to find computer products from different sellers in one website and decide easily with useful functionalities.

## Project Benefits
This project should improves:
- Your ability to translate text into code, and to turn requirements into a finished product.
- Your proficiency in following predefined requirements with attention to detail, ensuring a complete end-to-end execution.
- Your creative approach to tackling vague requirements.
- Your ability to hack, organize, document, test, structure, and write code efficiently.
- Your skill in utilizing existing resources to swiftly develop the application.

## Development Stacks
- Python3
- MySQL
- Flask
- HTML
- Flask sqlalchemy
- Beautifulsoup4
- Venv(optional)

## Project Overview
- Web Scraping: The products in the laptop category will be obtained from the Trendyol, N11, and Hepsiburada websites.
- Database: The data collected from the websites will be stored in a MySQL database, utilizing Flask SQLAlchemy for the connection. The database will include tables and functions to support listing, searching, filtering, and referencing other sites, as well as a "more info" page. An administrative page will also be provided for adding, deleting, and updating records within the database.
- Duplicate checking will be implemented to avoid storing identical records


## How to Run
- Python 3.7.4 is recommended.
1. install and extract project
2. open project with your IDE like vscode
3. Creating virtual environment (not necessary but recommended)
-  macOS/Linux
```
# You may need to run sudo apt-get install python3-venv first
$ python3 -m venv .venv
```
- Windows
```
# You can also use py -3 -m venv .venv
$ python -m venv .venv
```
4. Install dependencies
```
$ pip install -r requirements.txt
```
5. Install mySQL
6. Open mySQL SHELL and create database
```
Example:
\connect --mysql root@localhost
\sql
\Create database computer_db;
\show databases;
```
7. Connect by changing URI from /app/_\_init__.py
8. Run

## Project Final Result Screenshots
### Main Page
![main](https://user-images.githubusercontent.com/75525649/217823458-62238236-b86a-4070-b440-804cb0f6ad6f.png)

### More Info Page
![more_info](https://user-images.githubusercontent.com/75525649/217823474-9c868493-c147-4853-8333-7e250579a280.png)

### Admin Page
![admin](https://user-images.githubusercontent.com/75525649/217823448-f8ae9c24-5da5-4fe3-bb8d-15f3cb052400.png)
