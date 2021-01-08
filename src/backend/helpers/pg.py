import subprocess

def drop_table(table_name):
    query_str = '''
        DROP TABLE {}
    '''.format(table_name)
    out, err = query(query_str)
    return out, err    

def dump():
    pass

def query(query_str):
    '''
    Performs the specified query.
    '''
    cmd = ['psql', '-Atc', '{}'.format(query_str)]
    query_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = query_proc.communicate()
    return parse_output(out), err

def parse_output(out):
    '''
    Parses output from psql console.
    '''
    out = out.decode('utf-8')
    rows = [row.split('|') for row in out.split('\n')]
    return set(rows)

