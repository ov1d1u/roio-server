from base64 import b64encode

from storm.locals import *

database = create_database("sqlite:roio.sqlite")
store = Store(database)

class User(object):
	__storm_table__ = "users"

	id = Int(primary=True)
	username = Unicode()
	password = Unicode()
	email = Unicode()
	real_name = Unicode()
	session_key = Unicode()
	last_timestamp = Unicode()

	def __init__(self, username, password, email, real_name):
		self.username = unicode(username)
		self.password = unicode(password)
		self.email = unicode(email)
		self.real_name = unicode(real_name)

	def save(self):
		store.add(self)
		store.flush()
		store.commit()

	@classmethod
	def auth(self, username, password):
		user = store.find(User, User.username == unicode(username), User.password == unicode(password)).one()
		return user

	@classmethod
	def get_by_email(self, email):
		user = store.find(User, User.email == unicode(email)).one()
		return user

class Message(object):
	__storm_table__ = "messages"

	id = Int(primary=True)
	message = Unicode()
	timestamp = DateTime()

	def __init__(self, message):
		self.message = unicode(message)

	def save(self):
		store.add(self)
		store.flush()
		store.commit()

	@classmethod
	def get_latest(self):
		message = store.find(Message).order_by(Desc(Message.timestamp))
		if message.count():
			return message[0]
		else:
			return Message('')

class Category(object):
	__storm_table__ = "content_categs"

	id = Int(primary=True)
	icon = RawStr()
	name = Unicode()
	priority = Int()

	@classmethod
	def get(self):
		categories = {}
		db_categories = store.find(Category).order_by(Desc(Category.priority))
		for c in db_categories:
			categories[c.id] = {
				'name': c.name,
				'icon': b64encode(c.icon)
			}
		return categories

if __name__ == '__main__':
	print 'Running as __main___, so creating db structure'
	statements = [
	"""
	CREATE TABLE IF NOT EXISTS "users"
		("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE  DEFAULT 0, 
		"username" VARCHAR NOT NULL  UNIQUE ,
		"password" VARCHAR NOT NULL , 
		"email" VARCHAR NOT NULL ,
		"real_name" VARCHAR,
		"session_key" VARCHAR,
		"last_timestamp" NUMERIC);""",
	"""CREATE  TABLE IF NOT EXISTS "messages"
		("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE ,
		"message" TEXT NOT NULL ,
		"timestamp" DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP);
	""",
	"""CREATE  TABLE IF NOT EXISTS "content_categs"
		("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , 
		"icon" BLOB NOT NULL ,
		"name" VARCHAR NOT NULL ,
		"priority" INTEGER DEFAULT 0);
	"""
	]
	for sql in statements:
		store.execute(sql)
	store.flush()
	store.commit()