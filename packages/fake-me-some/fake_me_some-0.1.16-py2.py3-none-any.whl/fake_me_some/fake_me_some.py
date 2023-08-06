import string
import yaml
import argparse
import os
import shutil
import sys
import pprint
import logging as lg
from py_dbutils.rdbms import postgres
import pyarrow
import random
from faker import Faker
import re
from collections import OrderedDict

lg.basicConfig()
logging = lg.getLogger('fake-me-some')
 
 


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def set_log_level(debug_level):
    if debug_level == 'DEBUG':
        logging.setLevel(lg.DEBUG)
    if debug_level == 'INFO':
        logging.setLevel(lg.INFO)
    if debug_level == 'WARN':
        logging.setLevel(lg.WARN)
    if debug_level == 'ERROR':
        logging.setLevel(lg.ERROR)
# run through the yaml and replace embedded params


def pre_process_yaml(yaml_file):
    # yaml_file = os.path.abspath(yaml_file)
    yaml_data = None
    with open(yaml_file, "r") as f:
        yaml_data = yaml.safe_load((f))

    source_db = yaml_data['db']['connection']
    src_db = None
    if source_db['type'] == 'POSTGRES':
        src_db = postgres.DB(host=source_db['host'],
                             port=source_db['port'],
                             dbname=source_db['db'],
                             schema=source_db['schema'],
                             userid=source_db['userid'],
                             pwd=os.environ.get(source_db['password_envir_var'], None))
    else:
        print('Error Non Supported Database: {}'.format(source_db['type']))
        sys.exit(1)

    return yaml_data, src_db


fake = Faker()
fake.add_provider('providers.lorem.sentence')
fake.add_provider('providers.lorem.words')
fake.add_provider('providers.lorem.word')
sentence = getattr(fake, 'sentence')
words = getattr(fake, 'words')
word = getattr(fake, 'word')
random_num = random.SystemRandom()


def random_char_generator(str_size=1):
    string_word = 'need to implement random char generator'
    return string_word


def random_string_generator(str_size, num_words=1):

    #allowed_chars = chars = string.ascii_letters + string.punctuation

    string_word = words(1)
    string_word = ' '.join(string_word)
    if len(string_word) > str_size:
        string_word = string_word[:str_size]
    return string_word


def dump_yaml_to_file(tables, outfile):

    def custom_dump_yaml(ordered_data, output_filename):
        #DB or Tables

        for i in ordered_data:

            output_filename.write(f"{i}:\n")
            # Tables names
            for j in ordered_data[i]:

                output_filename.write(f"  {j}:\n")
                for k in ordered_data[i][j]:

                    output_filename.write(
                        f"    {k}: {ordered_data[i][j][k]}\n")

    # dump_ordered_yaml(tables,outfile)
    custom_dump_yaml(tables, outfile)

# function to derive a function to generate data and return that function to be called later


def fake_data(data_type):

    dynamic_module_path = "faker.{}"
    module = None
    func_name = None
    if len(data_type.split('.')) > 1:
        module = data_type.split('.')[0]
        func_name = data_type.split('.')[-1]
    else:
        if len(data_type.split(',')) > 1:
            return random_string_generator
        else:
            return random_string_generator
    if module is not None:

        dynamic_module_path = dynamic_module_path.format(module)

        module = __import__(dynamic_module_path)

        fake = Faker()
        fake.add_provider(module)
        func_name = getattr(fake, func_name)

        return func_name

    raise Exception("Fake Function Not found")


def map_fake_functions(root, yaml_data):
    import copy

    tables = copy.deepcopy(yaml_data[root])

    for tbl in tables.keys():

        t = tables[tbl]
        if t is not None:
            for col in t.keys():
                column_type = t[col] 
                if str(column_type).startswith('providers.'):
                    xx = fake_data(column_type)
                    t[col] = xx 

                elif (str(column_type).upper().startswith('NUMERIC')
                        or str(column_type).upper().startswith('DOUBLE')
                        or str(column_type).upper().startswith('MONEY')

                      ):

                    def rnd_float(start=0, end_max=sys.maxsize):
                        key_num = round(random.random(), 2)
                        return key_num
                    t[col] = rnd_float
                elif str(column_type).upper() == ('DATE'):
                    import datetime
                    def rnd_time():

                        return datetime.datetime.now().strftime("%Y-%m-%d")
                    t[col] = rnd_time
                elif str(column_type).upper().startswith('TIMESTAMP') or str(column_type).upper().startswith('DATETIME'):
                    import datetime

                    def rnd_time():
                        return datetime.datetime.now()
                    t[col] = rnd_time
                elif str(column_type).upper().startswith('VARCHAR') or str(column_type).upper().startswith('CHAR') or str(column_type).upper().startswith('TEXT'):

                    # get the len between parentasis
                    str_len = 0

                    try:
                        str_len = int(
                            re.search(r'\((.*?)\)', str(column_type).upper()).group(1))

                        def rnd_str(int_len=str_len):

                            return random_string_generator(int_len, int(int_len/6)+1)

                        t[col] = rnd_str
                    except:
                        logging.info("Not lenth specified assumes text")
                        fake = Faker()
                        fake.add_provider('providers.lorem.sentence')
                        sentence = getattr(fake, 'sentence')

                        def rnd_lorem():
                            return sentence()
                        t[col] = rnd_lorem

                elif str(column_type).upper() in ['BIGINT', 'INT', 'INTEGER']:

                    def rnd_int(start=0, end_max=sys.maxsize):

                        return random_num.randint(0, 65045)
                    t[col] = rnd_int
                elif str(column_type).upper() in ['SMALLINT']:

                    def rnd_int(start=0, end_max=sys.maxsize):

                        return random_num.randint(0, 255)
                    t[col] = rnd_int
                elif str(column_type).upper().startswith('BIT') or str(column_type).upper().startswith('BOOL'):

                    def rnd_bit(start=0, end_max=sys.maxsize):
                        return str(random.getrandbits(1))
                    t[col] = rnd_bit
                else:
                    raise Exception(
                        "Uknown type {}-{}".format(col, str(column_type)))

    return tables
# leave what's already in the yaml file there and add in what's new


def merge_dict_file(tables, file, yaml_data):

    root = 'Tables'
    has_root = False
    file_yaml = None
    db = yaml_data['db']
    with open(file, 'r') as stream:
        file_yaml = ordered_load(stream, yaml.SafeLoader)
        #file_yaml = yaml.safe_load((outfile))

        # usage example:
        ordered_load(stream, yaml.SafeLoader)
        try:
            if file_yaml.get(root, None):
                has_root = True
        except:
            has_root = False

    if not has_root:
        with open(file, 'a') as outfile:
            [dump_yaml_to_file(tables, outfile)]

    else:
        # loop through every tables found in DB
        for tbl in tables[root].keys():
            t = tables[root][tbl]
            # check to see if table is in yaml file
            # if not add everything in
            file_yaml_tbl = file_yaml[root].get(tbl, None)
            if file_yaml_tbl is None:
                print("addding to yaml ", tbl)
                file_yaml[root][tbl] = t

            else:
                # since table exist loop through each column
                for col in t.keys():
                    # if column doesn't exist in yaml add the column
                    if file_yaml[root][tbl].get(col, None) is None:
                        file_yaml[root][tbl][col] = t[col]

        if file_yaml.get('db', None) is None:
            file_yaml['db'] = db
        with open(file, 'w') as outfile:

            dump_yaml_to_file(file_yaml, outfile)


def generate_yaml_from_db(db_conn, file_fqn, yaml_data):

    fqn = os.path.abspath(file_fqn)
    table_list = db_conn.get_all_tables()
    tbl = {}

    i = 0
    for t in table_list:

        if t.startswith(db_conn.schema+'.'):
            i += 1
            cols = get_table_column_types(db_conn, t)
            # order_dict=OrderedDict

            tbl[str(t).split(".")[-1]] = cols
    if i == 0:
        raise Exception(f"Not tables found in schema: {db_conn.schema}")
    tables = {"Tables": tbl}

    if not os.path.isfile(fqn):
        with open(fqn, 'w') as outfile:

            dump_yaml_to_file(tables, outfile)
    merge_dict_file(tables, fqn, yaml_data)


[]


def generate_yaml_from_db_suggest(db_conn, file_fqn, yaml_data):
    faker_list = []
    faker_file = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "provider.yml")
    with open(faker_file, "r") as f:
        faker_list = yaml.safe_load(f)
   

    fqn = os.path.abspath(file_fqn)
    table_list = db_conn.get_all_tables()
    tbl = {}

    for t in table_list:
        if t.startswith(db_conn.schema+'.'):

            cols = match_name_to_type(db_conn, t, None, faker_list)

            tbl[str(t).split(".")[-1]] = cols
    tables = {"Tables": tbl}

    if os.path.isfile(fqn):
        print("File Already Exists Merging Updates")
        merge_dict_file(tables, fqn, yaml_data)
    else:
        with open(fqn, 'w') as outfile:
            dump_yaml_to_file(tables, outfile)
        merge_dict_file(tables, fqn, yaml_data)


def parse_cli_args(yamlfile=None):
    parser = argparse.ArgumentParser(prog='fake_me_some', usage="""%(prog)s [options]
    MAKE A config.yaml like this if you don't have one:
    db:
    connection: 
        db: postgres
        host: pgdb
        port: 5432
        type: 'POSTGRES'
        schema: "test"
        userid: 'docker'
        password_envir_var: PGPASSWORD """)
    print("---------------------",yamlfile)
    if yamlfile is None:
        require_yaml=True
    else:
        require_yaml=False
    parser.add_argument('--y','--yaml', required=require_yaml,default=yamlfile,
                        help='path to yaml file')
    parser.add_argument('--of','--outfile', default=None,
                        help='new configuration yaml file to dump to with table description')
    parser.add_argument('--rows', default=10,
                        help='Number of Rows to Fake')
    parser.add_argument('--o', default='CSV',
                        help='output data to CSV, DB, PARQUET')
    parser.add_argument('--d','--dir',default=None,
                        help='output_directory')
    parser.add_argument('--ll', default='INFO',
                        help='Logging mode: DEBUG INFO WARN ERROR')
    args = parser.parse_args()
    
    return args


def fake_some_data_parquet(file_path, table, num_rows):
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    # make row for each
    rows = []
    for _ in range(num_rows):
        row = []
        for col in table.keys():
            data = table[col]()
            row.append(data)
        rows.append(row)
    header = [col for col in table.keys()]

    df = pd.DataFrame.from_records(rows, columns=header)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path)


def fake_some_data_db(table_name, table, num_rows, db_conn):
    import pandas as pd
    # make row for each
    rows = []
    logging.info("Faking Table: {} - {} Rows".format(table_name, num_rows))
    for _ in range(num_rows):
        row = []
        for col in table.keys():
            data = table[col]()
            row.append(data)
        rows.append(row)
    header = [col for col in table.keys()]

    pd = pd.DataFrame.from_records(rows, columns=header)
    engine = db_conn.connect_SqlAlchemy()

    pd.to_sql(table_name, engine, if_exists='append',
              index=False, schema=db_conn.schema)


def match_name_to_type(db, table_name, trg_schema=None, faker_list=[]):
    from Levenshtein import ratio

    import sqlalchemy

    if trg_schema is None:
        schema = db.schema
    else:
        schema = trg_schema
    con = db.connect_SqlAlchemy()
    schema_meta = sqlalchemy.MetaData(bind=con,
                                      schema=schema)
    schema_meta.reflect()
    table = sqlalchemy.Table(table_name.split(
        '.')[-1], schema_meta, schema=schema, autoload=True, autoload_with=con)
    cols = {}

    for col in table.columns:
        closes_distance = 0.0
        match_name = None
        try:  # if string , varchar text..etc
 
            for provider in faker_list:
                # print(type(provider),provider)
                for fake in faker_list[provider]:

                    r = ratio(fake, str(col).split('.')[-1])

                    r1 = ratio(provider.split(".")
                               [-1]+"_"+fake, str(col).split('.')[-1])
                    if r1 > r:
                        r = r1
                    if r > closes_distance:
                        closes_distance = r
                        match_name = provider+"."+fake

                if closes_distance == 1:
                    break
        except Exception as e:
            if not str(col.type).upper() in ['BIGINT', 'INT', 'SMALLINT', 'INTEGER']:
                print(" Number field found ", col.type, col)
                print("\t\t", e)
            match_name = col.type

        cols[str(col).split('.')[-1]] = str(match_name).split('(')[0]

    return cols


def get_table_column_types(db: postgres.DB, table_name, trg_schema=None):

    import sqlalchemy

    if trg_schema is None:
        schema = db.schema
    else:
        schema = trg_schema
    con = db.connect_SqlAlchemy()
    schema_meta = sqlalchemy.MetaData(bind=con,
                                      schema=schema)
    schema_meta.reflect()
    logging.info(" Current Table: {}".format(table_name))
    table = sqlalchemy.Table(table_name.split(
        '.')[-1], schema_meta, schema=schema, autoload=True, autoload_with=con)
    cols = OrderedDict()
    x, y = db.query(f"select * from {table_name} limit 1")

    ordered_column_list = [col for col in y]
    # print(ordered_column_list)

    for col in table.columns:
        col_length = None
        try:

            col_length = col.type.length

        except:

            pass
        str_type = str(col.type)
        order = 0
        found = False
        for i, ee in enumerate(ordered_column_list):

            if ee.name == col.name:
                order = i+1

        if i == 0:
            raise Exception("column not found")

        cols[order] = [str(col).split('.')[-1], str_type]
    cols2 = OrderedDict()

    for i, column in enumerate(cols):

        cols2[cols[column][0]] = cols[column][1]

    return (cols2)


def fake_some_data_csv(file_path, table, num_rows):

    # make row for each
    rows = []
    for _ in range(num_rows):
        row = []
        for col in table.keys():

            data = table[col]()
            row.append(data)
        rows.append(row)
    header = [col for col in table.keys()]
    import csv

    with open(file_path, 'w') as f:
        print("writing file: ", os.path.abspath(file_path))
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)


def main(yamlfile=None, p_output=None, p_generate=None, out_path=None):
    # process_list = []
    args = parse_cli_args(yamlfile)
    # multi process here for now
    # process_yaml(args.yaml, args.log_level)
    path = args.d
    if out_path is None:
        path = os.getcwd()
    else:
        path = os.path.abspath(out_path)
    yaml_file = args.y
    if not yamlfile is None:
        yaml_file = os.path.abspath(yamlfile)
    else:
        yaml_file = os.path.abspath(args.y)
    generate_yaml = p_generate or args.of
    output = p_output or args.o
    yaml_data = None

    with open(yaml_file) as f:
        #yaml_data = yaml.safe_load((f))
        yaml_data = ordered_load(f, yaml.SafeLoader)

    logging.info('Read YAML file: \n\t\t{}'.format(yaml_file))
    set_log_level(args.ll)
    yaml_dict, db_conn = pre_process_yaml(yaml_file)
    if generate_yaml is not None:

        if output == 'SUGGEST':

            generate_yaml_from_db_suggest(db_conn, generate_yaml, yaml_data)
        else:
            generate_yaml_from_db(db_conn, generate_yaml, yaml_data)
    else:
        # map each column to a faker function

        tables = map_fake_functions('Tables', yaml_dict)
        for table in tables.keys():

            t = tables[table]

            if t is not None:
                if output == 'CSV':
                    print("OUTPUT TO CSV:")
                    fake_some_data_csv(os.path.join(
                        path, table+'.csv'), t, int(args.rows))
                elif output == 'PARQUET':
                    fake_some_data_parquet(os.path.join(
                        path, table+'.parquet'), t, int(args.rows))
                elif output == 'DB':
                    print("OUTPUT TO DATABASE:")
                    fake_some_data_db(table, t, int(args.rows), db_conn)
                else:
                    print("unknow output so skipping table: {}".format(table))


if __name__ == '__main__':
    main()
