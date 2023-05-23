import pandas as pd

from src.get_db import get_db_fn  

from src.config_file import config_fn

def app():    
    
    (db_name, files, file_extension, file_path, prefix, *args) = config_fn()
    # client_details = clients[current_client]         
      
      
    for file_name in files:                  
        print(file_name+file_extension)
        
        #==>> Read Excel
        book = pd.ExcelFile(file_path+file_name+file_extension)
        sheets = book.sheet_names
        sheets_cnt = 0
        sheets_cnt = len(sheets)
        
        
                
        if (sheets_cnt != 0):
            
            conn, cursor = get_db_fn(db_name)
            
            
            #==>> iterate each workbook sheets, create a SQL Table for each of them and insert the data            
            for sheet in sheets:
                
                #==>> get current Sheet Data Frame and its columns
                # print('SheetName ==>> {}'.format(sheet))
                sheet_df = book.parse(sheet)             
                sheet_columns = sheet_df.columns
                            
                #==>> create table columns string to use in the insert STMT
                tbl_cols = "],[".join([str(i).replace(' ', '_').replace('#', 'Number')  for i in sheet_df.columns.tolist()])
                # tbl_cols = tbl_cols + '],[SourceName'
                # print(tbl_cols)
                
                # ==>> create table definition columns
                tbl_cols_definition = []            
                for column in sheet_columns:
                    tbl_cols_definition.append('[' + str(column).replace(' ', '_').replace('#', 'Number') + '] varchar(max)')           
                
                tbl_cols_definition.append('[SourceName] varchar(max)')
                # print(tbl_cols_definition)
                
                table_name = prefix + sheet + '_' + file_name
                
                drop_q= f"""drop table if exists [{table_name}]"""
                cursor.execute(drop_q)
                conn.commit()
                
                #==>> create table query
                create_table_query = f""" CREATE TABLE [{table_name}] ({tbl_cols_definition}) """    
                create_table_query = create_table_query.replace('([', '(').replace('])', ')').replace("'", '')
                # print(create_table_query)
                
                #==>> Hit DB to create the data table
                try:
                    cursor.execute(create_table_query)
                    conn.commit()       
                    
                    # print(f'Table {table_name} Created')
                except Exception as e:
                    print(f'Error Message (CREATE STMT) ==>> {e}')
                    
                #==>> Hit DB to add the ImportedDate column
                try:
                    alter_query = f"ALTER TABLE [{table_name}] ADD ImportedDate datetime DEFAULT GETDATE()"
                    cursor.execute(alter_query)
                    conn.commit()
                    # print(f'Table {table_name} Created')
                except Exception as e:
                    print(f'Error Message (ALTER STMT) ==>> {e}')  
                    
                                               
                # ==>> replace nan by zero (0) and insert each sheet_df record to SQL Table
                print('Importing data to SQL.....')
                sheet_df = sheet_df.fillna(0)            
                for index, row in sheet_df.iterrows():                               
                    # print(row)
                    insert_query = "INSERT INTO ["+ table_name +"] (["+ tbl_cols +"]) VALUES ("+ "?, "*(len(row)-1) + "?)"                    
                    try:                             
                        cursor.execute(insert_query, tuple(row))
                        conn.commit()  
                    except Exception as e:
                        print(row[0]) 
                        # print(f'Error Message (INSERT STMT) ==>> {e}')   
                
                # call sp to move data from table just created to PayRoll Table
                # cursor.execute(f"exec insert_HR_PayRoll_Table_sp '{table_name}'")
                # conn.commit()
                
                print('The SheetName:  "{0}" was loaded to SQL [{1}] Table.'.format(sheet, table_name))                
              
            
            try:                             
                source_name = file_name+file_extension                
                cursor.execute(f"update [{table_name}] set SourceName = '{source_name}'")
                conn.commit()  
            except Exception as e:
                print(f'Error Message (Update SOURCENAME STMT) ==>> {e}')                        
            
            
            # insert created table into the tracking table
            cursor.execute('INSERT INTO CreatedTablesByFileName (FileName, TableName, SheetName) VALUES (?, ?, ?)',(source_name, table_name, sheet,))
            conn.commit()
            
    
                        
            #close connection 
            cursor.close()
            conn.close()
        else: 
            print('Nothing to import to SQL')
    return