import pymysql
import sys

class MySQL():
	wherex = ''
	orderx = ''
	limitx = ''
	on = 0

	def __init__(self, *args, **kwargs):
		_config = {
			'host': 'localhost',
			'user': 'root',
			'passwd': None,
			'db': None,
			'table': '',
			'cursor': 'dict',
			'charset': 'utf8'
		}

		if len(args) == 1:
			kwargs = args[0]
		elif len(kwargs) > 0:
			pass
		else:
			print('传参有误！')
			sys.exit()

		for key in kwargs:
			if key in _config:
				_config[key] = kwargs[key]
			else:
				print('异常配置项：%s' % key)
				sys.exit()

		globals().update(_config)

		self.conn = pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=db, charset=charset)
		self.select_cursor(cursor)
		self.table = table

	# show the status of the current connection
	def status(self):
		# select the current database being used
		result = self.sql('SELECT DATABASE()')
		db = list(result[0].values())[0]
		if len(self.table) == 0:
			table = 'Null'
		else:
			table = self.table
		print('db:' + db, 'table:' + table, 'cursor:' + self.cursor)

	def select_cursor(self, cursor='dict'):
		if cursor == 'dict':
			self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
		else:
			self.cursor = self.conn.cursor()
		return self

	def select_db(self, db='', cursor='dict'):
		self.select_cursor(cursor)
		self.conn.select_db(db)
		return self

	def select_table(self, table='', db=''):
		if len(db) > 0:
			self.select_db(db)
		self.table = table
		return self

	def execute(self, sql):
		if (self.on):
			print(sql)
			self.on = 0
			sys.exit()

		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	# show the sql
	def sql(self, on=1):
		self.on = on
		return self

	def count(self, data={}, table=''):
		if (len(table) == 0):
			table = self.table

		count = 0
		if (len(data) == 0):
			query = "SELECT COUNT(*) count FROM %s" % (table)

		if (self.on):
			print(query)
			self.on = 0
			sys.exit()

		self.cursor.execute(query)
		result = self.cursor.fetchall()
		count = result[0]['count']

		return count

	def where(self, condition=''):
		if (type(condition) is str and len(condition) > 0):
			self.wherex = " WHERE %s" % condition

		if (type(condition) is dict and len(condition) > 0):
			items = []
			for key in condition:
				v = condition[key]
				key = "`%s`" % key
				if type(v) is str:
					if (v.lower() == 'null'):
						item = "%s IS Null" % key
					else:
						v = self.conn.escape_string(v)
						item = "%s = '%s'" % (key, v)
				else:
					item = "%s = %s" % (key, v)
				items.append(item)
			condition = (' AND ').join(items)
			self.wherex = " WHERE %s" % condition

		return self

	def order(self, field='id'):
		self.orderx = " ORDER BY `%s`" % field
		return self

	def limit(self, limit):
		if type(limit) is int:
			self.limitx = " LIMIT %s" % str(limit)
		elif type(limit) is list:
			limit = ', '.join(map(str, limit))
			self.limitx = " LIMIT %s" % limit
		return self

	def select(self, fields='', table=''):
		if (len(table) == 0):
			table = self.table

		if (len(fields) == 0):
			query = "SELECT * FROM `%s`" % table
		else:
			query = "SELECT %s FROM `%s`" % (fields, table)

		query += self.wherex + self.orderx + self.limitx

		if (self.on):
			print(query)
			self.on = 0
			sys.exit()

		self.cursor.execute(query)
		result = self.cursor.fetchall()

		self.wherex = ''
		self.orderx = ''
		self.limitx = ''

		return result

	def insert(self, data={}, table=''):
		if len(table) == 0:
			table = self.table

		fields = []
		values = []
		for key in data:
			fields.append("`%s`" % key)
			v = data[key]
			if type(v) is str:
				v = self.conn.escape_string(v)
			values.append("'%s'" % v)

		fields = ', '.join(fields)
		values = ', '.join(values)

		query = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, fields, values)

		if (self.on):
			print(query)
			self.on = 0
			sys.exit()

		self.cursor.execute(query)
		self.conn.commit()

	def update(self, data={}, table=''):
		if len(self.wherex) == 0:
			print('没有设置where()更新条件，禁止UPDATE操作！')
			sys.exit()
		if len(table) == 0:
			table = self.table

		fields = []
		for key in data:
			v = data[key]
			if type(v) is str:
				v = self.conn.escape_string(v)
				if (v.lower() == 'null'):
					fields.append("`%s` = Null" % (key))
				else:
					fields.append("`%s` = '%s'" % (key, v))
			elif type(v) is int:
				fields.append("`%s` = %d" % (key, v))
			else:
				print('字典内的value异常！！！')
				sys.exit()

		fields = ', '.join(fields)

		query = "UPDATE `%s` SET %s%s" % (table, fields, self.wherex)

		if (self.on):
			print(query)
			self.on = 0
			sys.exit()

		self.cursor.execute(query)
		self.conn.commit()

	def delete(self, data={}, table=''):
		if (len(self.wherex)==0):
			print('没有设置where()删除条件，禁止DELETE操作！')
			sys.exit()
		if len(table)==0:
			table = self.table

		query = "DELETE FROM `%s`%s" % (table, self.wherex)

		if (self.on):
			print(query)
			self.on = 0
			sys.exit()

		self.cursor.execute(query)
		self.conn.commit()

