import mysql.connector, sys
import config


 
cnx = mysql.connector.connect(user=config.MYSQL_USER, password=config.MYSQL_PASS, host=config.MYSQL_HOST, database=config.MYSQL_DATABASE)
cursor = cnx.cursor()


query = ("SELECT schedule_id, payer_id, payee_id, amount, category_id, status FROM schedule WHERE schedule_date = CURDATE() AND status = 'scheduled' ORDER BY schedule_id")
cursor.execute(query)
rows = cursor.fetchall()

for (schedule_id, payer_id, payee_id, amount, category_id, status) in rows:
    print(schedule_id, payer_id, payee_id, amount, category_id, status, file=sys.stderr)

    payer_query = ("SELECT balance FROM account WHERE user_id = %s")
    cursor.execute(payer_query, (payer_id, ))
    (balance,) = cursor.fetchone()

    if balance >= amount:
        try:
            insert_payment = ("INSERT INTO payment (payer_id, payee_id, amount, category_id, payment_time) VALUES(%s, %s, %s, %s, NOW())")
            cursor.execute(insert_payment, (payer_id, payee_id, amount, category_id))
            payment_id = cursor.lastrowid

            update_payer_balance = ("UPDATE account SET balance = balance - %s WHERE user_id = %s")
            cursor.execute(update_payer_balance, (amount, payer_id))

            update_payee_balance = ("UPDATE account SET balance = balance + %s WHERE user_id = %s")
            cursor.execute(update_payee_balance, (amount, payee_id))
            
            update_schedule = ("UPDATE schedule SET status = 'complete' WHERE schedule_id = %s")
            cursor.execute(update_schedule, (schedule_id, ))

            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()
            
            update_schedule = ("UPDATE schedule SET status = 'failed' WHERE schedule_id = %s")
            cursor.execute(update_schedule, (schedule_id, ))
            cnx.commit()
    else:
        try:
            update_schedule = ("UPDATE schedule SET status = 'nofund' WHERE schedule_id = %s")
            cursor.execute(update_schedule, (schedule_id, ))
            cnx.commit()
        except mysql.connector.Error as error:
            cnx.rollback()

cursor.close()
cnx.close()

