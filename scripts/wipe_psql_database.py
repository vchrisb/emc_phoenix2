import psycopg2
import sys
import os
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Drop all tables from PostgreSQL Database. Connection string is specified in os variable "DATABASE_URL"')
parser.add_argument('--force', help='Force execution', action="store_true")
parser.add_argument('--dropschema', help='wipe by dropping schema', action="store_true")

args = parser.parse_args()

try:
    database_url = os.environ['DATABASE_URL']
    result = urlparse(database_url)
    database_name = result.path[1:]
except:
    raise SystemExit("Error: ", sys.exc_info()[1])

if not args.force:
    choice = None
    while choice not in ('y', 'n'):
        choice = input('Do you really want to wipe the database: "%s"? (y/n)' %(database_name))

    if choice == 'n':
        raise SystemExit("aborted by user input")

# Connect to database
try:
    conn = psycopg2.connect(database_url)
    conn.set_isolation_level(0)
    cur = conn.cursor()
except:
    print("Error while connecting to database!")
    raise SystemExit("Error: ", sys.exc_info()[1])

# Drop all tables from a given database
try:
    if args.dropschema:
        cur.execute("DROP SCHEMA public CASCADE")
        cur.execute("CREATE SCHEMA public")
        cur.execute("GRANT ALL ON SCHEMA public TO postgres")
        cur.execute("GRANT ALL ON SCHEMA public TO public")
        cur.execute("COMMENT ON SCHEMA public IS 'standard public schema'")
    else:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name")
        rows = cur.fetchall()
        for row in rows:
            print ("dropping table: %s" %(row[0]))
            cur.execute("DROP TABLE " + row[0] + " CASCADE")
    cur.close()
    conn.close()
    print('Wiped database: %s' %(database_name))
except:
    print("Error while executing database queries!")
    raise SystemExit("Error: ", sys.exc_info()[1])
