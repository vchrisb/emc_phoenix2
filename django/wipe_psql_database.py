import psycopg2
import sys
import os
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Drop all tables from PostgreSQL Database. Connection string is specified in os variable "DATABASE_URL"')
parser.add_argument('--force', help='Force execution', action="store_true")

args = parser.parse_args()

if not args.force:
    choice = None
    while choice not in ('y', 'n'):
        choice = input('Do you really want to wipe the database? (y/n)')

    if choice == 'n':
        raise SystemExit("aborted by user input")

# Connect to database
try:
    database_url = os.environ['DATABASE_URL']
    result = urlparse(database_url)
    database_name = result.path[1:]
    conn = psycopg2.connect(database_url)
    conn.set_isolation_level(0)
    cur = conn.cursor()
except:
    print("Error while connecting to database!")
    raise SystemExit("Error: ", sys.exc_info()[1])

# Drop all tables from a given database
try:
    cur.execute("DROP SCHEMA public CASCADE")
    cur.execute("CREATE SCHEMA public")
    cur.execute("GRANT ALL ON SCHEMA public TO postgres")
    cur.execute("GRANT ALL ON SCHEMA public TO public")
    cur.execute("COMMENT ON SCHEMA public IS 'standard public schema'")
    cur.close()
    conn.close()
    print('Wiped database: %s' %(database_name))
except:
    print("Error while executing database queries!")
    raise SystemExit("Error: ", sys.exc_info()[1])
