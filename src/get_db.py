import pyodbc

def get_db_fn(db_name):    
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=SERVER_IP;'
                        'Database=' + db_name + ';'
                        'UID=USER_NAME;'
                        'PWD=PASSWORD;')    
    cursor = conn.cursor()
    return conn, cursor