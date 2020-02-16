#!/usr/bin/python3
from __future__ import annotations
import typing
import datetime
import edgedb
import argparse
import os
import time
cmd_args = argparse.ArgumentParser(
        prog="edbc",
        description="A tool for lazy people to work with EdgeDB.",
        usage="""%(prog) [option] 
                Help: [-h] 
                Update: [-u] <schema>.file
                JSON Download: [-fd] <schema>.file
                Execute: [-x] <DDL>.file
                Download: [-fd] <schema>.edgeql
                DSN: [--dsn] 'edgedb://user:password@host:port/database'"""
)

man_string = """
Setup:
------
Try supplying a DSN connection string to your shell environment.
This can be accomplished by running:

    `export EDGEDB_DSN_PATH='/home/user/my_edgedb_dsn.txt'`

where /home/user/my_edgedb_dsn.txt is the path to a file containing
your DSN connection string. The connection string in that file should
resemble:

    edgedb://user:password@host:port/database

to be interpreted correctly by this tool. Alternatively, you could
supply the '--dsn=<Your EdgeDB DSN>' argument, but be advised
that this is could store a password in a history file. To increase
security, you can change permissions on the dsn file to require 
root-level read access and run this tool as root by running

    `sudo su`
    
then

    `edbc [options] <args>`

to protect public users on your system from seeing plaintext passwords
in your history file(s).

Examples
--------

1.) `edbc -u some_new_schema_def_file.edgeql`
Pushes a new schema to the EdgeDB instance at the provided DSN
and overwrites the current database schema with a new one.

2.) `edbc -fd <schema def file>`
Downloads all elements from the edgedb server and saves them locally
as a JSON file by extracting property, type, and link names from the
file and structures sequential blocking calls to request all objects
of each type, then update a dictionary of the returned values.

3.) `edbc -x <data def file>`
Executes all statements contained in the data definition file
against the server. This file can include statements directly against
the server.


[Maybe Future Feature]
----------------------
4.) `edbc -uj <json file> -f <current schema def file>`
Reads in both the JSON and schema definition files to push new objects
from the JSON to the database where the newly created records
will match as many fields as possible to current schema.

5.) `edbc -m <old schema> <new schema>`
Migrates current objects from the old schema to the new one. This is a
dangerous operation and should not be used lightly, since it will
drop all attributes and types from current objects if they are not in the
new schema file. 
Likewise, any required fields present in the new schema file which are not
available in the old schema will give migrated objects a default value of
an empty set (`{}`).

"""
# Prints man string
cmd_args.add_argument('-h', help=man_string)

# Assigns the'f' key to the value of the file
cmd_args.add_argument('-f', action='store')

#
cmd_args.add_argument()
cmd_args.add_argument()

class EdgeDBClientAPIException(Exception):
    _dsn_missing = "Missing environment variable string `$EDGEDB_DSN_PATH` of the form /<path>/<to>/<file> which contains the DSN connection string resembling 'edgedb://user:password@host:port/database?option=value'. Please export the value and re-run this tool. Otherwise, use the more insecure option of supplying the DSN connection string directly as an argument to this command line tool with the `--dsn` option."
    _connection_failed = "Could not reach the EdgeDB instance at the address you provided."
    def __init__(self, err_message):
        self.err = err_message
    def __raise__(self):
        print(self.err)
        return self

def load_dsn(_dsn_str="") -> str:
    try:
        assert _dsn_str == ""
        try:
            _dsn_str_file = os.environ.get('EDGEDB_DSN_PATH')
            assert _dsn_str_file is not None
            with open(_dsn_str_file, 'r') as f:
                _dsn_str = f.read()
            return _dsn_str
        except AssertionError:
            err = EdgedBClientAPIException(_dsn_missing)
            raise err
    except AssertionError:
        return _dsn_str

            
