import pymysql

available_users = []
users = []
psws = []
db = pymysql.connect("localhost", "root", "200035", "rdh")
cursor = db.cursor()
# cursor.execute("insert into users (username, password) values ('public', 'public')")
# cursor.execute("insert into users (username, password) values ('lihan', '123456')")

user = "'lihan'"
sql = "select password from users where username = " + user
print(sql)
cursor.execute(sql)
# result = cursor.fetchone()
# print(type(result[0]))
print(cursor.fetchone()[0])

# result = cursor.execute("select * from users where username = 'lihan1'")
# print(result)

# print(users)
# print(psws)



# db.commit()
# user1 = 'zhang'
# psw1 = '123456'
#
# sql = "insert into users (username, password) values ('" + user1 + "', " + "'" + psw1 + "')"
# cursor.execute(sql)
# db.commit()
# print(sql)