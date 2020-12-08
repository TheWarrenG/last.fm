import os
import sys
import sqlite3


def die_with_usage():
    """ HELP MENU """
    print('demo_similars_db.py')
    print('  by T. Bertin-Mahieux (2011) tb2332@columbia.edu')
    print('')
    print('Shows how to use the SQLite database made from similar')
    print('tracks in the Last.fm dataset.')
    print('')
    print('USAGE:')
    print('  ./demo_similars_db.py <similars.db>')
    sys.exit(0)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        die_with_usage()

    # param
    dbfile = sys.argv[1]

    # sanity check
    if not os.path.isfile(dbfile):
        print('ERROR: db file %s does not exist?' % dbfile)
        die_with_usage()

    # open connection
    conn = sqlite3.connect(dbfile)

    # EXAMPLE 1
    print('************** DEMO 1 **************')
    tid = 'TREDTHC128F92D42F0'
    print('We get all similar songs (with value) to %s' % tid)
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    print(data)
    print('(total number of similar tracks: %d)' % (len(data.split(','))/2))

    # EXAMPLE 2
    print('************** DEMO 2 **************')
    tid = 'TRCXCLD128F93127D3'
    print('We get all songs which consider %s as similar' % tid)
    sql = "SELECT target FROM similars_dest WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    print(data)
    print('(total number of track where %s is similar: %d)' % (tid,
                                                               len(data.split(','))/2))

    # EXAMPLE 3
    print('************** DEMO 3 **************')
    print('We count the number of songs with at least one known similar')
    sql = "SELECT DISTINCT tid FROM similars_src"
    res = conn.execute(sql)
    cnt = len(res.fetchall())
    print('Found %d such tracks' % cnt)

    # EXAMPLE 4
    print('************** DEMO 4 **************')
    print('We count the number of unique songs who are considered similar to some other one')
    sql = "SELECT DISTINCT tid FROM similars_dest"
    res = conn.execute(sql)
    cnt = len(res.fetchall())
    print('Found %d such tracks' % cnt)

    # EXAMPLE 5
    print('************** DEMO 5 **************')
    tid = 'TRPYHPC128F930F9B0'
    print('We get similars to %s and order them by similarity value' % tid)

    sql = "SELECT target FROM similars_dest WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    data_unpacked = []
    for idx, d in enumerate(data.split(',')):
        if idx % 2 == 0:
            pair = [d]
        else:
            pair.append(float(d))
            data_unpacked.append(pair)
    # sort
    data_unpacked = sorted(data_unpacked, key=lambda x: x[1], reverse=True)
    for k in range(10):
        print(data_unpacked[k])
    print('...')
    print('(total number of pairs with such similarity value: %s' % len(data_unpacked))
    
    # close connection
    conn.close()
    