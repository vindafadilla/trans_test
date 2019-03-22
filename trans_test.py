#!C:/Users/asus/AppData/Local/Programs/Python/Python37/python.exe
import mysql.connector
from mysql.connector import Error
import json
import cgitb
import cgi


def html_show():
    cgitb.enable()
    form = cgi.FieldStorage()
    lister = ['a', 'b', 'c']

    html_list = ''
    for value in lister:
        html_list += '<option value={0}>{0}</option>'.format(value)

    html = """Content-type: text/html\n

    <html>
    <head>
    </head>
    <body>
    <select>
       {}
    </select>
    </body>
    </html>
    """.format(html_list)
    print(html)


def html_handle(data_lulusan, total_all, tahun):
    title = "<h3>Data Divisi</h3>"
    table_prefix="<div><table border=1>"
    thead = "<thead><tr><th rowspan=2>No</th><th rowspan=2>Divisi</th><th colspan=7>"+str(tahun-1)+"</th><th colspan=7>"+str(tahun)+"</th></tr><tr><th>SD</th><th>SMP</th><th>SMA</th><th>DIP</th><th>S1</th><th>S2</th><th>S3</th><th>SD</th><th>SMP</th><th>SMA</th><th>DIP</th><th>S1</th><th>S2</th><th>S3</th></tr></thead>"
    tbody_prefix = "<tbody>"
    tbody_sufix="</tbody>"
    tfoot_prefix="<tfoot><tr>"
    tfoot_sufix="</tr></tfoot>"
    table_sufix="</table></div>"

    table_html = title+table_prefix+thead+tbody_prefix

    for i in range(len(data_lulusan)):
        table_html+="<tr>"
        table_html+="<td>"+str(i+1)+"</td>"
        for j in range(len(data_lulusan[i])):
            table_html+="<td>"+str(data_lulusan[i][j])+"</td>"
        table_html+="</tr>"

    table_html+=tbody_sufix+tfoot_prefix+"<td colspan=2 style='text-align:center;'><strong>Total</strong></td>"

    for i in range(len(total_all)):
        table_html+="<td>"+str(total_all[i])+"</td>"

    table_html+=tfoot_sufix+table_sufix
    # print(table_html)
    send_to_file = str(tahun) + '.txt'
    if send_to_file:
        # Writing JSON data
        with open(send_to_file, 'w') as f:
            json.dump([table_html], f)

def total_tahun(mycursor,index):
    # print(index)
    sql_select_total = "select SUM(`SD`),SUM(`SMP`),SUM(`SMA`), SUM(`D1`+`D2`+`D3`) as dip, SUM(`S1`), SUM(`S2`), SUM(`S3`) FROM data_lulus where tahun='"+str(index)+"'"

    mycursor.execute(sql_select_total)
    tambah=[]
    for row in mycursor.fetchall():
        tambah = [int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])]

    return tambah

def sort_tahun(mydb,index):
    # print(mydb, index)
    sql_select_divisi = "select distinct divisi from data_lulus where tahun='"+str(index-1)+"' or tahun='"+str(index)+"'"
    mycursor = mydb.cursor()
    mycursor.execute(sql_select_divisi)

    divisiArr = []

    for row in mycursor.fetchall():
        divisiArr.append(row[0])

    # print(divisiArr)

    data_lulus = []
    total_all =[]

    for i in range(len(divisiArr)):
        data_ = [divisiArr[i]]
        sql_select_data = "select `SD`,`SMP`,`SMA`, (`D1`+`D2`+`D3`) as dip, `S1`, `S2`, `S3` FROM data_lulus where (tahun='"+str(index-1)+"' or tahun='"+str(index)+"') and `divisi`="+" '"+divisiArr[i]+"'"
        # print(sql_select_data)
        mycursor.execute(sql_select_data)
        for row in mycursor.fetchall():
            tambah = [row[0],row[1],row[2],row[3],row[4],row[5],row[6]]
            data_.extend(tambah)
        data_lulus.append(data_)

    for i in range(index-1,index+1):
        if(i>2013 & i<2020):
            total_all.extend(total_tahun(mycursor, i))

    # print(data_lulus,total_all)
    html_handle(data_lulus, total_all, index)

if __name__ == '__main__':
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="data_perusahaan"
        )

        for i in range(2014,2020):
            sort_tahun(mydb,i)

        html_show()
    except Error as e:
        print("Error while connecting to MySQL", e)