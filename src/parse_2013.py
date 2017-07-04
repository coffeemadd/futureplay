# https://stackoverflow.com/questions/27584405/how-to-import-a-mysqldump-into-pandas

from StringIO import StringIO
import re
import pandas as pd

def read_dump(dump_filename, target_table):
    sio = StringIO()
    count = 0
    fast_forward = True
    with open(dump_filename, 'rb') as f:
        for line in f:
            line = line.strip()
            if line.lower().startswith('insert') and target_table in line:
                fast_forward = False
            if fast_forward:
                continue
            data = re.findall('\([^\)]*\)', line)
            try:
                newline = data[0]

                ### updated this part
                newlines = re.sub('\),\(', '),\n(', newline)
                for newline in newlines.split('\n'):
                    newline = newline.strip(' ()')
                    newline = newline.replace('`', '')
                    newline = newline.replace(', ', '_ ')

                    sio.write(newline)
                    sio.write("\n")
            except IndexError:
                print newline
                pass
    sio.pos = 0
    return sio


people_table = read_dump('../data/2013/fixed_cb_people.sql', 'cb_people')
df_people = pd.read_csv(people_table, header=None, error_bad_lines=False)
df_people.columns = ['id', 'object_id', 'first_name', 'last_name', 'birthplace', 'affiliation_name']

