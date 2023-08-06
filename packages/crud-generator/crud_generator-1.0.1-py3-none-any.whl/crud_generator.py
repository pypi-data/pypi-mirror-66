# Author: Harsh Goyal
# Date: 20-04-2020


def generate_crud(table_name, attributes):
    file = open('crud_{}.py'.format(table_name), 'w')
    attr_list = attributes.split(",")
    attributes_str = ""
    for i in attr_list:
        attributes_str += i
        attributes_str += ','
    attributes_str = attributes_str[:-1]
    print(attributes_str)
    function_string_connection = """def create_conn():
    pass
    #Enter your connection code
    #Example: for postgresql
    #conn = psycopg2.connect(database = "testdb", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
    #then return conn
    """

    print(function_string_connection)

    function_string_create = """def create_{0}(values):
    attr_list = values.split(\",\")
    attributes_str = \"\"
    for i in attr_list:
        attributes_str += \"\\\'\" + i + \"\\\'\"
        attributes_str += \',\'
    attributes_str = attributes_str[:-1]
    print(attributes_str)
    conn = create_conn()
    cur = conn.cursor()
    sql = \"insert into {0}({1}) values({2}{3});\".format(attributes_str)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    """.format(table_name, attributes_str, '{', '}')
    print(function_string_create)

    function_string_read = """def read_{0}(condition=\"1=1\"):
    conn = create_conn()
    cur = conn.cursor()
    sql = \"select * from {0} where {1}{2};\".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    rows = cur.fetchall()
    data_dictionary = {1}{2}
    indices = 0
    for row in rows:
        data_dictionary[indices] = list(row)
        indices += 1
    conn.commit()
    conn.close()
    return data_dictionary
    """.format(table_name, '{', '}')
    print(function_string_read)

    function_string_update = """def update_{0}(values, condition=\"1=1\"):
    conn = create_conn()
    cur = conn.cursor()
    sql = \"update {0} set {2}{3} where {2}{3};\".format(values, condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
    """.format(table_name, attributes_str, '{', '}')
    print(function_string_update)

    function_string_delete = """def delete_{0}(condition=\"1=1\"):
    conn = create_conn()
    cur = conn.cursor()
    sql = \"delete from  {0}  where {1}{2};\".format(condition)
    print(sql)
    try:
        cur.execute(sql)
    except:
        print("Something Went wrong")
    conn.commit()
    conn.close()
""".format(table_name, '{', '}')

    print(function_string_delete)
    file.write(function_string_connection)
    file.write("\n\n")
    file.write(function_string_create)
    file.write("\n\n")
    file.write(function_string_read)
    file.write("\n\n")
    file.write(function_string_update)
    file.write("\n\n")
    file.write(function_string_delete)
    file.close()

    return 1


