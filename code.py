#!/Python27/python
import MySQLdb
import cgi

print "Content-type: text/html"
print
print "<html><head><title>BDM Lab Assignment</title>"
print ""
print "</head><body>"
print "<h1><font color='white'><marquee> Online MySQL Editor </marquee></h1>"
print "<style> table {border: 2px solid#f1f1f1}"
print "th {border: 1px solid #f1f1f1;text-align: left;padding: 8px;width: 100px;;text-transform: uppercase;}"
print "tr, td {border: 1px solid #000000;text-align: left;padding: 8px;width: 100px;}"
print "ta {border: 1px solid #f1f1f1;background-color:#dddddd;text-align: left;padding: 8px;width: 100%;}"
print "th {background-color: #4682B4;}"
print "tr:nth-child(even) {background-color: #dddddd;}"
print "tr:nth-child(odd) {background-color: #ADD8E6;}"
print ".button {background-color: #4CAF50;border: none;color: white;padding: 15px 32px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px;margin: 4px 2px;cursor: pointer;}"
print "body {background: url('http://news.rutgers.edu/sites/medrel/files/inline-img/highres/RBSfront-entrance-sign_highres.jpg')"
print "no-repeat center center fixed;"
print "background-size: 1680px 640px;"
print "}</style>"
print ""

db = MySQLdb.connect(host="localhost",  # Hostname
                     user="fancy",  # Username
                     passwd="mysql",  # Password
                     db="stock_market")  # Schema


print '<form method="post" action="code.py">'
print "      <h2><font color='white'>Input the Query:</h2>"
print '	     <p><textarea name="query" wrap="logical" style="font-size:12pt;height:150px;width:1310px;background-color:#f1f1f1"/></textarea></p>'
print '	     <p><input type="submit" class="button" value="Submit >>"></p>'
print "	     </form>"
print "</form>"
print "</body></html>"

def create_table(data):
    table = '<table><tr>'
    for i in cur.description:
        table += '<th>' + str(i[0]) + '</th>'
    table += '</tr>'
    if cur.rowcount <> 0:
        for item in data:
            table += '<tr>'
            for i in range(len(cur.description)):
                table += '<td>' + str(item[i]) + '</td>'
            table += '</tr>'
    else:
        table += '<tr><td>' + 'NULL' + '</td></tr>'
    table += '</table>'
    print table

form = cgi.FieldStorage()
if form.getvalue("query"):
    query = form.getvalue("query")

cur = db.cursor()
line = ''

for char in query:
    line += char

words = line.split(";")
words[-1] = words[-1].strip()

if words[-1] == "":
    words.pop(-1)

for i in range(len(words)):
    try:
        cur.execute(words[i])
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        db.rollback()
        print "<p><ta><font color='black'><font size='5'>Query \" " + words[i] +  " \" failed to execute.</font></ta></p>"
        print "<p><ta><font color='black'><font size='5'>"
        print e
        print '</font></ta></p>'

    rows = cur.fetchall()
    
    if not rows and cur.rowcount <> 0:
        db.commit()
        print "<p><ta><font color='black'><font size='5'>Query \" " + words[i] + " \" executed successfully.</font></ta></p>"
    elif not rows and cur.rowcount == 0:
        print "<p><ta><font color='black'><font size='5'> 0 rows affected </font></ta></p>"
    elif rows:
        # print all the first cell of all the rows
        data = []
        for row in rows:
            data.append(row)
            # print data
        print "<p><ta><font color='black'><font size='5'>Result for query \" " + words[i] + " \" :</font></ta></p>"
        create_table(data)

db.close()
