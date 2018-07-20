import jsondiff
import psycopg2
import json
from pprint import pprint


def get_schema(cur):
    table_name = ''
    tables = dict()
    for column in cur.fetchall():
        if column[0] != table_name:
            table_name = column[0]
            tables[table_name] = dict()
        tables[table_name][column[1]] = column[2] + ' ' + str(column[3])
    return tables


conn9 = psycopg2.connect(host='localhost', port='5432', database='json', user='postgres', password='111111')
conn_bad = psycopg2.connect(host='localhost', port='5432', database='json_bad', user='postgres', password='111111')
cur9 = conn9.cursor()
cur_bad = conn_bad.cursor()

query = "SELECT table_name, column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_schema = 'public'"

cur9.execute(query)
tables9 = get_schema(cur9)
conn9.close()

cur_bad.execute(query)
tables_bad = get_schema(cur_bad)
conn_bad.close()


with open('table_bad.json', 'w') as f:
    f.write(json.dumps(tables_bad, indent=4))

with open('table9.json', 'w') as f:
    f.write(json.dumps(tables9, indent=4))

table9 = dict(json.load(open('table9.json')))
table_bad = dict(json.load(open('table_bad.json')))

aaa= jsondiff.diff(table9, table_bad,syntax='symmetric')
pprint(aaa)
#print(jsondiff.diff(table_bad, table9,syntax='symmetric'))

#print(cur9.fetchall())

#print(json.dumps(tables9, indent=4))


template = {"atast":{
                'id':'integer',
                'time':'datetime'
            },
            "softwareversion":{
                'id':'integer',
                'name':'varchar(100)',
's':'a'
            }
}

cust = {"softwareversion":{
                 'id':'integer',
                    's':'a',
                 'name':'varchar(10)'
             },
"atast":{
                'id':'integer',
                'time':'int'
            }

}

#print(jsondiff.diff(json.dumps(template),json.dumps(cust)))
# template['atast']['anme'] = 'abc'
# print(template['atast']['id'])

''
z={'aa':'1','bb':'2'}
x={'aa':'10','cc':'3'}

pprint(jsondiff.diff(z,x,syntax='symmetric'))

pprint(jsondiff.diff(z,x,syntax='explicit'))
