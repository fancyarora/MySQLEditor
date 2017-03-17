#!/Python27/python
import MySQLdb
import cgi

print "Content-type: text/html"
print
print "<html><head><title>BDM Lab Assignment</title>"
print ""
print "</head><body>"
print "<h1> Online MySQL Editor </h1>"
print "<style> table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}"
print "td, th {border: 1px solid #000000;text-align: left;padding: 8px;}"
print "th {background-color: #4682B4;}"
print "tr:nth-child(even) {background-color: #dddddd;}"
print "tr:nth-child(odd) {background-color: #ADD8E6;}</style>"
print ""

db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="fancy",  # your username
                     passwd="",  # your password
                     db="fancy")  # name of the data base


print '<form method="post" action="test16.py">'
print '<div class="w3-container">'
print '  <div class="w3-row">'
print '    <div class="w3-col l10">'
print '      <div style="padding:15px;padding-bottom:40px;margin-bottom:40px;background-color:#f1f1f1;box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">'
print '      <h3>Input the Query:</h3>'
print '		 <form method="post" action="test18.py">'
print '	     <p><textarea name="query" wrap="logical" style="font-size:12pt;height:150px;width:1300px;"/></textarea></p>'
print '		 <p><input type="submit" value = "Submit"/></p>'
print "		 </form>"
print '		 </div>'
print '	   </div>'
print '	 </div>'
print '</div>'
print "</form>"
print "</body></html>"

def create_html(data):
    html = '<table><tr>'
    for i in cur.description:
        html += '<th>' + str(i[0]) + '</th>'
    html += '</tr>'
    for item in data:
        html += '<tr>'
        for i in range(len(cur.description)):
            html += '<td>' + str(item[i]) + '</td>'
        html += '</tr>'
    html += '</table>'
    print html

form = cgi.FieldStorage()
if form.getvalue("query"):
    query = form.getvalue("query")

cur = db.cursor()
line = ''

for char in query:
    line += char

words = line.split(";")

for i in range(len(words)):
    if "select" or "show" in words[i].lower():
        data = []
        try:
            cur.execute(words[i])
            # print all the first cell of all the rows
            for row in cur.fetchall():
                data.append(row)
            # print data
            print '<div style="padding:15px;padding-bottom:40px;margin-bottom:40px;background-color:#f1f1f1;box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">'
            print '<h3>Result for the \"' + words[i] + '\" query:</h3>'
            create_html(data)
            print '</div>'
        except:
            print '<div style="padding:15px;padding-bottom:40px;margin-bottom:40px;background-color:#f1f1f1;box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">'
            print "<h3>Query: \"" + words[i] +  "\" failed to execute</h3>"
            print '</div>'
    elif words[i] == "":
        continue
    else:
        try:
            cur.execute(words[i])
            db.commit()
            print '<div style="padding:15px;padding-bottom:40px;margin-bottom:40px;background-color:#f1f1f1;box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">'
            print "<h3>Query: \"" + words[i] + "\" executed successfully</h3>"
            print '</div>'
        except:
            db.rollback()
            print '<div style="padding:15px;padding-bottom:40px;margin-bottom:40px;background-color:#f1f1f1;box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">'
            print "<h3>Query: \"" + words[i] +  "\" failed to execute</h3>"
            print '</div>'
db.close()