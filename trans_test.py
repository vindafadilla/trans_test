#!C:/Users/asus/AppData/Local/Programs/Python/Python37/python.exe

##---------------Library--------------------##

# Run in xampp
# https://stackoverflow.com/questions/42704846/running-python-scripts-with-xampp

# Install mysql-connector:
#     pip install mysql - connector
# Install simplejson:
#     pip install simplejson
# cgi (default)
import mysql.connector
from mysql.connector import Error
import json
import cgi
import cgitb

##---------------Module to format html and save it into a txt file--------------------##
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
    send_to_file = str(tahun) + '.txt'
    if send_to_file:
        # Writing JSON data
        with open(send_to_file, 'w') as f:
            json.dump([table_html], f)

##---------------Module to add data into an array--------------------##
def list_data_tahun(mycursor,index, divisi):
    tambah = []
    sql_select_data = "select SUM(`SD`),SUM(`SMP`),SUM(`SMA`), SUM(`D1`+`D2`+`D3`) as dip, SUM(`S1`), SUM(`S2`), SUM(`S3`) FROM data_lulus where tahun='" + str(index) + "'"

    if divisi!=None:
        sql_select_data+=" and `divisi`='"+divisi+"'"

    mycursor.execute(sql_select_data)
    data_hasil = mycursor.fetchall()

    for row in data_hasil:
        if row[0] is not None:
            tambah = [int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])]
        else:
            tambah=[0,0,0,0,0,0,0]

    return tambah

##---------------Module to add data per year--------------------##
def sort_tahun(mycursor,index):
    divisiArr = []
    data_lulus = []
    total_all =[]

    sql_select_divisi = "select distinct divisi from data_lulus where tahun='"+str(index-1)+"' or tahun='"+str(index)+"'"
    mycursor.execute(sql_select_divisi)

    for row in mycursor.fetchall():
        divisiArr.append(row[0])

    for i in range(len(divisiArr)):
        data_ = [divisiArr[i]]
        data_.extend(list_data_tahun(mycursor, index-1, divisiArr[i]))
        data_.extend(list_data_tahun(mycursor, index, divisiArr[i]))
        data_lulus.append(data_)
    total_all.extend(list_data_tahun(mycursor, index-1, None))
    total_all.extend(list_data_tahun(mycursor, index, None))

    html_handle(data_lulus, total_all, index)

##---------------Main Module--------------------##
if __name__ == '__main__':
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="data_perusahaan"
        )
        mycursor = mydb.cursor()

        for i in range(2014,2020):
            sort_tahun(mycursor,i)

        cgitb.enable()
        print ("Content-type: text/html\n\n")
        form = cgi.FieldStorage()
        # Get data from fields
        if form.getvalue('dropdown'):
            subject = form.getvalue('dropdown')
            html_file = subject + '.txt'
            f = open(html_file, 'r')
            content = f.read().replace('["','').replace('"]','')
            print (content)
            f.close()
        else:
            subject = "Not entered"

    except Error as e:
        print("Error while connecting to MySQL", e)