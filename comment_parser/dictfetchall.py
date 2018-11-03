def dictfetch(cursor, arraysize = 1000):
    "Return all rows from a cursor as a dict"    
    columns = [col[0] for col in cursor.description]
    
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        yield [
            dict(zip(columns, row))
            for row in results
        ]    
