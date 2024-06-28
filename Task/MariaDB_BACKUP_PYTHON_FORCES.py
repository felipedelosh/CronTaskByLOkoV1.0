#expresion_cron=0 * * * *
"""
FelipedelosH

This script is create to generate a Backup of maria DB the credentials in os "ENVIROMENT VARS"

NOTE: the BK it´s only provated in one project "FACIRES".

Based on standard backup system:
command: mysqldump --opt --events --routines --triggers --default-character-set=utf8 -u root --password=XYZ facires  > BK-DATE.sql

NOTE: you need install mysql conector: pip install mysql-connector-python
"""
import mysql.connector
import os
from datetime import datetime

def getFormatedTime():
    date = datetime.now()
    return f"{date.year}-{date.month}-{date.day}-{date.hour}.{date.minute}.{date.second}"

def eraseStrangerCharacters(txt):
    if "\n" in txt:
        _arr = str(txt).splitlines()
        _formated_txt = "\\n\\r".join(_arr)
        _formated_txt = _formated_txt.replace("\\n\\r\\n\\r", "\\n\\r")
        return _formated_txt
    

    if "\'" in txt:
        _formated_txt = txt.replace("'", "\\'")
        return _formated_txt

    return txt

# Internal vars
_PATH_ = str(os.path.dirname(os.path.abspath(__file__)))
#_MARIA_DB_LOCAL_MACHINE_PATH = "C:\Program Files\MariaDB 11.3\bin"
_STATUS_COMMAND_ = True
_BK_FILENAME = f"BK-{getFormatedTime()}"
_SQL_FINAL_DATA_ = ""


# TO GENERATE A SQL ITEMS
_DB_TABLES_ = {} # key is name of table and data is sql to create.
_DB_TABLES_INSERTING = {} # key is the name of table and the data is the SQL to insert
_DB_STATISTICS_ = {} # Save all metadata of process
_DROP_TABLE_ = "DROP TABLE IF EXISTS `XYZ`;"
_LOCK_TABLE_ = "LOCK TABLES `XYZ` WRITE;"
_CREATE_TABLE_ = """
CREATE TABLE `XYZ` (
`ATRIBBS`
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish2_ci;
"""
_UNLOCK_TABLES = "UNLOCK TABLES;"
_PK_ = "PRIMARY KEY (`XYZ`)"

# Get database config values
DATABASE_URL = os.getenv("DATABASE_URL") 
DATABASE_NAME = str(DATABASE_URL).split("/")[-1]
if "?" in DATABASE_NAME:
    DATABASE_NAME = DATABASE_NAME.split("?")[0]
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

# Get database key conection
db_config = {
    'user': DATABASE_USERNAME,
    'password': DATABASE_PASSWORD,
    'host': 'localhost',
    'database': DATABASE_NAME
}

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Key names of tables and construct create table(...)
    for iterTableName in tables:
        _table_name = iterTableName[0]
        _DB_TABLES_[_table_name] = ""
        _DB_STATISTICS_[_table_name] = {
            "total_cols" : 0,
            "total_regs" : 0
        }
        

        #print(_table_name)
        cursor_table_info = connection.cursor()
        cursor_table_info.execute(f"DESCRIBE {_table_name}")
        table_description = cursor_table_info.fetchall()

        _arrRestrictionPK = []
        _arrRestrictionFK = []
        _arrRestrictionUNI = []
        _attrib = ""

        for j in table_description:
            _attrib_name = j[0]
            _attrib_type = j[1]

            _DB_STATISTICS_[_table_name]["total_cols"] = len(table_description)

            #Special case JSON longtext
            if _attrib_type == "longtext":
                _attrib =  _attrib + f"  `{_attrib_name}` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`{_attrib_name}`)),\n"
                continue

            _NULL_STATUS = j[2]
            _attrib_null_status = ""
            if _NULL_STATUS == "NO":
                _attrib_null_status = "NOT NULL"
            else:
                _attrib_null_status = "DEFAULT NULL"
            _attrib_PK = j[3]
            
            if _attrib_PK == "PRI":
                _arrRestrictionPK.append(_attrib_name)
            elif _attrib_PK == "FK":
                _arrRestrictionFK.append(_attrib_name)
            elif _attrib_PK == "UNI":
                _arrRestrictionUNI.append(_attrib_name)

            
            _attrib =  _attrib + f"  `{_attrib_name}` {_attrib_type} {_attrib_null_status},\n"

        _TABLE_STRUCTURE = _CREATE_TABLE_.replace("`XYZ`", f"`{_table_name}`")

        # UPDATE PRIMARY KEY
        if len(_arrRestrictionPK) > 0:
            _KEYS = ""
            for iterPK in _arrRestrictionPK:
                _KEYS = _KEYS + f"`{iterPK}`, "
            #Erase last comma and space
            _KEYS = _KEYS[0:-2]
            _PK = _PK_.replace("`XYZ`", _KEYS)
            _attrib = _attrib + "  " + _PK
        else:
            _attrib = _attrib[0:-2] # Erase last comma and break line if not have primary key


        _TABLE_STRUCTURE = _TABLE_STRUCTURE.replace("`ATRIBBS`", _attrib)

        # Save insert in the table
        _DB_TABLES_[_table_name] = _TABLE_STRUCTURE

    cursor_table_info.close()
    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(f"Error al realizar la copia de seguridad: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()



# LOAD DATABASE DATA
try:
    connection = mysql.connector.connect(**db_config)
    
    for iterTableName in _DB_TABLES_:
        cursor = connection.cursor()
        _SQL = f"select * from {iterTableName}"
        cursor.execute(_SQL)

        data = cursor.fetchall()

        if len(data) > 0:
            _DATA_INSERT = f"INSERT INTO `{iterTableName}` VALUES\n"

            for iterRow in data:
                _export_data = ""
                for iterData in iterRow:
                    if iterData == '': # Not info
                        _export_data = _export_data + f"'',"
                        continue

                    if not iterData: # Null data
                        _export_data = _export_data + f"NULL,"
                        continue
                    
                    if not isinstance(iterData, str): # Number or date

                        if ":" in str(iterData) or "-" in str(iterData):
                            _export_data = _export_data + f"'{iterData}',"
                            continue
                        
                        _export_data = _export_data + f"{iterData},"
                        continue

                    if '"' in iterData: # Format Json
                        _json_format = iterData.replace('"', '\\\"')
                        _export_data = _export_data + f"'{_json_format}',"
                        continue
                    

                    _export_data = _export_data + f"'{eraseStrangerCharacters(iterData)}',"
                    # END for iterData

                # Erase last comma with extract all row data
                _export_data = _export_data[0:-1]
                _DATA_INSERT = _DATA_INSERT + f"({_export_data}),\n"

            # Save all registers
            # Erase last comma to save final inserting sentence and put ;
            _DATA_INSERT = _DATA_INSERT[0:-2] + ";"
            _DB_TABLES_INSERTING[iterTableName] = _DATA_INSERT

    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print(f"Error al realizar la copia de seguridad: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()


# Generate a Backup FILE
for iterTableName in _DB_TABLES_:
    # DROP TABLE
    _SQL_FINAL_DATA_ = _SQL_FINAL_DATA_ + f"{_DROP_TABLE_.replace("`XYZ`",f"`{iterTableName}`")}\n"
    #Create TABLE
    _SQL_FINAL_DATA_ = _SQL_FINAL_DATA_ + _DB_TABLES_[iterTableName] + "\n"
    #Lock table to write information
    #_SQL_FINAL_DATA_ = _SQL_FINAL_DATA_ + f"{_LOCK_TABLE_.replace("`XYZ`", f"`{iterTableName}`")}\n\n"
    # If extist PUT the information
    try:
        if iterTableName in _DB_TABLES_INSERTING.keys():
            _SQL_FINAL_DATA_ = _SQL_FINAL_DATA_ + f"{_DB_TABLES_INSERTING[iterTableName]}\n"
    except:
        print("Error en: ", iterTableName)

    # Unlock Table
    #_SQL_FINAL_DATA_ = _SQL_FINAL_DATA_ + "UNLOCK TABLES;\n\n\n"


with open(f"{_BK_FILENAME}.sql", "w",  encoding="UTF-8") as f:
    f.write(_SQL_FINAL_DATA_)
