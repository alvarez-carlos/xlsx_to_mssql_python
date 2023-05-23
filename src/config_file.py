#.............................. <<REPLACE WITH YOU DATA>> <<START>>
db_name = 'DN_NAME' #replace based on you need
file_path='FILES PARENT FOLDER PATH' #replace based on you need
files = [
    'mappingA',
    'mappingB'] #files name without extension. #replace based on you need

file_extension = '.xlsx' #replace based on you need
prefix = 'yf_' #replace based on you need
#.............................. <<REPLACE WITH YOU DATA>> <<END>>
   

def config_fn():
    return (db_name, files, file_extension, file_path, prefix,)


##........................ <<SQL QUERY TO CREATE TRACKING TABLE>>
# create table CreatedTablesByFileName 
# (
# 	ID int not null primary key identity,
# 	[FileName] varchar(max),
# 	SheetName varchar(max),
# 	TableName varchar(max),
# 	CreateDate datetime default(getdate()),
# 	CreateUserName varchar(max) default(system_user)
# )

# delete from CreatedTablesByFileName 

# select * 
# from CreatedTablesByFileName 

# insert into CreatedTablesByFileName (FileName, TableName) values ('FileZ', 'Table1'), ('FileZ', 'Table2'), ('FileZ', 'Table3')



#...................... <<insert to HR Payroll SP>>
# create proc insert_HR_PayRoll_Table_sp @tableName varchar(max) as
	
# 	-- insert_HR_PayRoll_Table_sp  'yf_insumos_mappingB'

# 	declare @dynamicQuery  varchar(max)= ' insert into HR_PayRoll_Table (campo1, campo2, campo3) select valueForCampo1, valueForCampo2, valueForCampo3 from ['+ @tableName +']'
# 	-- exec (@dynamicQuery)
# 	print ((@dynamicQuery))