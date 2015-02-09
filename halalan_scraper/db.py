import MySQLdb as mysql
import MySQLdb.cursors

from halalan_scraper.settings import HOST, USER, PASSWORD, DATABASE

class Db:
  def __init__(self):
    self.db = mysql.connect(HOST, USER, PASSWORD, DATABASE,
      use_unicode=True, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)

    self.cursor = self.db.cursor()

  def insert(self, item):
    query = """INSERT INTO articles (article_id, title, article, date) VALUES (%s, %s, %s, %s)"""

    self.cursor.execute(query, (item['article_id'], item['title'], item['article'], item['date']))

    id = self.cursor.lastrowid

    self.db.commit()
    self.db.close()

    return {'id': id}

  def isExisting(self, article_id):
    query = """SELECT * FROM articles WHERE article_id = %s"""

    self.cursor.execute(query, [article_id])
    self.db.close()

    res = self.cursor.fetchone()

    return res != None