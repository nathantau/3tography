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


from helpers import users
print(users.test())
# print(users.get_user('nate'))
# users.set_follow('nate','a')