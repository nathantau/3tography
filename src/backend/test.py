# import psycopg2
# conn = psycopg2.connect("dbname=nathan user=nathan")
# cur = conn.cursor()
# # cur.execute("select * from users;")
# # print(cur.fetchall())
# try:
#     cur.execute("insert into users values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#     ("sam","$2b$12$bm5fBwc.DKLPbVuMQgDRK.VrUYT779b2.AXrXwvQeZeCRYn5a0n8S",[],[],"","","","",""))
#     conn.commit()

# except Exception as e:
#     print('error!!!!!!!')
#     print(e)

try:
    raise Exception(100,200)
except Exception as e:
    print(e[0])