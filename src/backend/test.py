# import psycopg2
# conn = psycopg2.connect("dbname=nathan user=nathan")
# cur = conn.cursor()
# cur.execute('''
#         UPDATE users
#         SET following = array_append(following, '{}')
#         WHERE username = '{}'
# ''')
# # # print(cur.fetchall())
# # try:
# #     cur.execute("insert into users values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
# #     ("sam","$2b$12$bm5fBwc.DKLPbVuMQgDRK.VrUYT779b2.AXrXwvQeZeCRYn5a0n8S",[],[],"","","","",""))
# #     conn.commit()

# # except Exception as e:
# #     print('error!!!!!!!')
# #     print(e)

# # try:
# #     raise Exception(100,200)
# # except Exception as e:
# #     print(e[0])

# from helpers import pg


from helpers import pg, users
# print(users.test())
# print(users.get_user('nate'))
# users.set_follow('nate','test1')
# username, column, value, is_array=False
# print(users.update_user('nate', 'following', 'test1', True))

username1 = 'nate'

cur, conn = pg.create_connection()
# cur.execute(
#     f'SELECT username FROM users WHERE username LIKE \'{username}%\''
# )
# print(cur.fetchall())
# pg.close_connection(cur, conn)

# print(users.set_unfollow('nate', 'test'))

user = users.get_user(username1)

# user['following'].remove('a')

# cur.execute(
#     f'UPDATE users SET following = %s WHERE username = \'{username1}\'',
#     (user['following'], )
# )

# conn.commit()


user['following'].remove('test3')
cur.execute(
    f'UPDATE users SET following = %s WHERE username = \'{username1}\'',
    (user['following'], )
)
conn.commit()
pg.close_connection(cur, conn)