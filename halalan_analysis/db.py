import MySQLdb as mysql
import MySQLdb.cursors

from settings import HOST, USER, PASSWORD, DATABASE

class Db:
  def __init__(self):
    self.db = mysql.connect(HOST, USER, PASSWORD, DATABASE,
      use_unicode=True, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
    
    self.cursor = self.db.cursor()

  def getArticlesWithNullSentiment(self):
    query = """SELECT * FROM articles where sentiment is NULL"""

    self.cursor.execute(query)
    self.db.close()

    results = self.cursor.fetchall()

    return results