# coding: utf-8
import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect("dbname='db' user='user' password='passwd'")
    conn.autocommit = True  # You should set "globally" here or, on each SQL DDL command, do conn.commit()
except:
    print "I am unable to connect to the database."


try:
    POPULATE_TABLE = False

    cursor = conn.cursor()

    if POPULATE_TABLE:
        sql = 'DELETE FROM temp_table'
        cursor.execute(sql)

        sql = """copy
        temp_table
        from
        'D:\\temp\\spreadsheet.csv'
        DELIMITERS ';' CSV HEADER ENCODING 'Latin1';
        """
        cursor.execute(sql)

    # cursor = conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)

    sql = 'SELECT * FROM temp_table'
    cursor.execute(sql)
    row_count = 0
    for row in cursor:
        row_count += 1
        print "row: %s    %s\n" % (row_count, repr(row))

except Exception, e:
    print e.message
