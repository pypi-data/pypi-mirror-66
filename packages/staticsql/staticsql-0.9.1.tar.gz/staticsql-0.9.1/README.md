# StaticSQL

A library for working with [StaticSQL](https://github.com/iteg-hq/staticsql) entity metadata files.

The library supports extracting metadata from CREATE TABLE statements and database connections
and reading and writing them to and from json files:

 - `from_connection(connection)`: read all entity definitions from a database source.
 - `from_sql(create_table (str))`: parse a CREATE TABLE statement and return the entity metadata.
 - `from_file(path)`: read entity definition from a json file.
 - `to_file([path], [name_pattern="{schema}.{name}.json"] [, folder="."])`: dump an entity definition to a json file.
