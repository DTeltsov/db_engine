def serialize_dbs(dbs):
    json_data = [{'name': i['name']} for i in dbs['dbs']]
    return json_data


def serialize_db(db):
    json_data = {'db_name': db.name}
    json_data['tables'] = []
    for table in db.tables:
        table_dict = {'table_name': table.table_name}
        json_data['tables'].append(table_dict)
    return json_data


def serialize_table(table):
    json_data = {
            'table_name': table.table_name,
            'columns': [column.__dict__ for column in table.columns],
            'rows': [{'pk': i, 'data': row} for i, row in enumerate(table.rows)]
        }
    return json_data
