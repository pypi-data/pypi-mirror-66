import pyodbc
import itertools
import collections

extract_query = """
SELECT
    s.name AS schema_name
  , t.name AS entity_name
  , c.name AS attribute_name
  , TYPE_NAME(system_type_id) AS type_name
  , CASE
        WHEN max_length = -1 THEN
            'MAX' 
        WHEN TYPE_NAME(system_type_id) IN ('NVARCHAR', 'NCHAR') THEN
            CAST(max_length/2 AS NVARCHAR(100))
        ELSE
            CAST(max_length AS NVARCHAR(100))
    END AS max_length
  , precision
  , scale
  , c.is_nullable
FROM sys.columns AS c
INNER JOIN sys.tables AS t
  ON t.object_id = c.object_id
INNER JOIN sys.schemas AS s
  ON s.schema_id = t.schema_id
ORDER BY 
    s.name
  , t.name
  , c.column_id
"""

extract_query = """
SELECT
    TABLE_SCHEMA AS schema_name
  , TABLE_NAME AS table_name
  , COLUMN_NAME AS attribute_name
  , LOWER(DATA_TYPE) AS type_name
  , CASE CHARACTER_MAXIMUM_LENGTH 
        WHEN -1 THEN 'MAX'
        ELSE CAST(CHARACTER_MAXIMUM_LENGTH AS NVARCHAR(100))
    END AS max_length
  , NUMERIC_PRECISION AS precision
  , NUMERIC_SCALE AS scale
  , CASE IS_NULLABLE
        WHEN 'YES' THEN 1
        WHEN 'NO' THEN 0
    END AS is_nullable
FROM INFORMATION_SCHEMA.COLUMNS
"""


# Mappings af sys-schema-attributter til datatyper
type_formats = {
    "bit": "BIT",
    "int": "INT",
    "bigint": "BIGINT",
    "smallint": "SMALLINT",
    "tinyint": "TINYINT",
    "float": "FLOAT",
    "real": "REAL",
    "decimal": "DECIMAL({precision},{scale})",
    "numeric": "NUMERIC({precision},{scale})",
    "money": "MONEY",
    "date": "DATE",
    "datetime": "DATETIME",
    "datetime2": "DATETIME2({max_length})",
    "time": "TIME({precision})",
    "nvarchar": "NVARCHAR({max_length})",
    "varchar": "VARCHAR({max_length})",
    "nchar": "NCHAR({max_length})",
    "char": "CHAR({max_length})",
    "ntext": "NTEXT",
    "uniqueidentifier": "UNIQUEIDENTIFIER",
    "timestamp": "TIMESTAMP",
    "image": "IMAGE",
    "binary": "BINARY({max_length})",
    "varbinary": "VARBINARY({max_length})",
}


# Hent alle tabeller fra en database-forbindelse
def from_connection(conn):
    # conn = pyodbc.connect(connection_string, autocommit=True)
    cursor = conn.cursor()
    cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.execute(extract_query)
    attributes = cursor.fetchall()

    for (schema_name, entity_name), entity_attributes in itertools.groupby(attributes, lambda row: row[0:2]):
        entity_dict = collections.ordereddict({
            "schema": schema_name,
            "name": entity_name,
            "tags": [],
            "attributes": [],
        })

        for _, _, attribute_name, type_name, max_length, precision, scale, is_nullable in entity_attributes:
            attribute_dict = collections.OrderedDict()
            entity_dict["attributes"].append(attribute_dict)
            attribute_dict["name"] = attribute_name
            attribute_dict["data_type"] = type_formats[type_name].format(max_length=max_length, precision=precision, scale=scale)
            attribute_dict["is_nullable"] = bool(is_nullable)
            attribute_dict["tags"] = []
        yield entity_dict

def from_dump(path, sep="\t"):
    attributes = []
    for line in open(path):
        attributes.append(line.split(sep))
    for (schema_name, entity_name), entity_attributes in itertools.groupby(attributes, lambda row: row[0:2]):

        entity_dict = collections.OrderedDict({
            "schema": schema_name,
            "name": entity_name,
            "tags": [],
            "attributes": [],
        })

        for _, _, attribute_name, type_name, max_length, precision, scale, is_nullable in entity_attributes:
            attribute_dict = collections.OrderedDict()
            entity_dict["attributes"].append(attribute_dict)
            attribute_dict["name"] = attribute_name
            attribute_dict["data_type"] = type_formats[type_name].format(max_length=max_length, precision=precision, scale=scale)
            attribute_dict["is_nullable"] = bool(is_nullable)
            attribute_dict["tags"] = []
        yield entity_dict

# Forbind til en database og hent alle tabeller
def from_connection_string(conn_str):
    with pyodbc.connect(conn_str) as conn:
        for entity in from_connection(conn):
            yield entity

# Her starter den interessante del af koden:
# En connection string til den database, vi skal trække ud fra
# (den skal rettes til en rigtig connection string
# som I kan finde i Azure portalen for SQL Database)

