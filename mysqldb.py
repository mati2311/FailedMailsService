from datetime import date, datetime
from multiprocessing import connection
from sqlite3 import connect
import pymysql

from models.mail import Mail

# from models.mail import Mail

class SqlConection:
    #database connection
    conn = pymysql.connect(host="localhost",user="root",password="",database="failedmailsdb" )
    
    def insertMail(self, mail:Mail):
        try:
            
            
            cursor = self.conn.cursor()
            sql = "INSERT IGNORE INTO `mails` (`Id`, `gmail_id`, `ReceptionDate`, `To`, `Subject`, `CreateDate`, `UpdateDate`, `Body`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = ( mail.id,mail.gmailId,mail.receptionDate, mail.to, mail.subject, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),datetime.now().strftime('%Y-%m-%d %H:%M:%S'),mail.body)
            cursor.execute(sql,val)
            self.conn.commit()
            print(cursor.rowcount, "record inserted.")
        except Exception as e:
            print("EXCEPTION: ",e)
            pass

    def listMails(self):
        try:
            cursor = self.conn.cursor()
            
            sql = "SELECT * FROM `mails`"
            cursor.execute(sql)
            self.conn.commit()
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

            return json_data
        except Exception as e:
            print("EXCEPTION: ",e)
            pass

        pass
            

