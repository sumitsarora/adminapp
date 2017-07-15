from flask import Blueprint, request, render_template,jsonify,json,Flask
import config
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, IMAGES
#import MySQLdb
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import sys
from time import time
from app import app
from datetime import datetime
import xlrd
from app.ws.level import Level
from app.ws.service import Service
import requests
import os

ws = Blueprint("ws", __name__, url_prefix="/ws")
#db = MySQLdb.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_DB)

#upload configuration
base_path = os.getcwd()
#dest=os.path.join(base_path,'''app/static''')
dest = os.path.dirname(__file__)
pcatalog=UploadSet('pcatalog',DOCUMENTS)
app.config['UPLOADED_PCATALOG_DEST']=dest
configure_uploads(app,pcatalog)

#cors enable
CORS(app)

#mysql configuartion production
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_HOST'] = config.MYSQL_HOST
mysql = MySQL(app)

@ws.route('/',methods=['GET'])
def hello():
    return render_template('ws/index.html')#jsonify({'message':'It Works!'})

@cross_origin()
@ws.route('/lang',methods=['GET'])
def lang():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM level''')
    rows = cur.fetchall()
    column = [t[0] for t in cur.description]
    myjsonArr=[]
    levelObjArr=[]
    for row in rows:
        myjson = {column[0]: row[0], column[1]: row[1], column[2]: row[2], column[3]: row[3], column[4]: row[4], column[5]: row[5], column[6]: row[6], column[7]: row[7],
        column[8]:row[8],column[9]:row[9],column[10]:row[10]}
        levelObj=Level(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        #print("levelObj ",levelObj.toString())
        myjsonArr.append(myjson)
        levelObjArr.append(levelObj)
        myresult = json.dumps(myjsonArr, indent=4)
        #print("myjsonArr size ",len(myjsonArr))

        #calling service behaviour to construct jsonforated response
    service=Service()
    result=service.constructJsonResponse(levelObjArr)
    #rv = cur.fetchall()
    #return jsonify({'languages':rv})
    return jsonify({"products":result})
    #return render_template('resultset.html',output=result)
    #return jsonify({'languages':languages})

@ws.route('/result',methods=['GET'])
def resultset():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM level''')
    rows = cur.fetchall()
    column = [t[0] for t in cur.description]
    myjsonArr=[]
    levelObjArr=[]
    for row in rows:
        myjson = {column[0]: row[0], column[1]: row[1], column[2]: row[2], column[3]: row[3], column[4]: row[4], column[5]: row[5], column[6]: row[6], column[7]: row[7],column[8]:row[8]}
        levelObj=Level(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        #print("levelObj ",levelObj.toString())
        myjsonArr.append(myjson)
        levelObjArr.append(levelObj)
        myresult = json.dumps(myjsonArr, indent=4)
        #print("myjsonArr size ",len(myjsonArr))

        #calling service behaviour to construct jsonforated response
    service=Service()
    result=service.constructJsonResponse(levelObjArr)

    format=request.args.get('display')
    #print('************************format***************',format)
    #rv = cur.fetchall()
    if format=='pretty':
        return jsonify({'catalog':result})
    #return jsonify({"products":result})
    return render_template('ws/resultset.html',output=result)
    #return jsonify({'languages':languages})

@ws.route('/lang/<string:name>',methods=['GET'])
def returnObj(name):
    for item in languages:
        if item['name']==name:
            return jsonify({'language':item})

@ws.route('/lang',methods=['POST'])
def addObject():
    try:
        language={'name':request.json['name']}
    except Exception as e:
        return jsonify({"error":e})

    languages.append(language)
    return jsonify({'languages':languages})

@ws.route('/import',methods=['GET'])
def excelImport():
    #read excel file
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'pcatalog.xls')
    book=xlrd.open_workbook(filename)
    sheet=book.sheet_by_name("source")

    #start:clear table before inserting
    cur = mysql.connection.cursor()
    query='''delete from level'''
    cur.execute(query)
    #mysql.connection.commit()
    #end:clear table before inserting

    cur = mysql.connection.cursor()
    query='''insert into level(level1,level2,level3,level4,level5,ptitle,pimg,pprice,pdesc,pstatus) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    #for loop to iterate each row in sheet
    for r in range(1,sheet.nrows):
        level1=sheet.cell(r,0).value
        level2=sheet.cell(r,1).value
        level3=sheet.cell(r,2).value
        level4=sheet.cell(r,3).value
        level5=sheet.cell(r,4).value
        ptitle=sheet.cell(r,5).value
        pimg=sheet.cell(r,6).value
        pprice=sheet.cell(r,7).value
        pdesc=sheet.cell(r,8).value
        pstatus=sheet.cell(r,9).value

        #assign values to placeholder
        values=(level1,level2,level3,level4,level5,ptitle,pimg,pprice,pdesc,pstatus)
        #execute query
        cur.execute(query,values)

    mysql.connection.commit()
        #print result
    columns=str(sheet.ncols)
    rows=str(sheet.nrows)
    result=str("I have imported "+columns+" columns and "+rows+" rows successfully")
    return  render_template('ws/import.html',output=result)
    #print("I have imported "+columns+" columns and "+rows+" rows successfully")

@ws.route('/upload',methods=['GET','POST'])
def upload():

    if request.method=='POST' and 'user_file' in request.files:
        try:
            if request.files['user_file'].filename == '':
                return render_template('ws/upload.html',output="No selected file")

            filename = os.path.join(dest, 'pcatalog.xls')
            os.rename(filename,filename+'_'+str(time()))
            filename=pcatalog.save(request.files['user_file'])
            return render_template('ws/upload.html',output=filename+ ' file uploaded successfully on the server')
        except ValueError:
            return render_template('ws/upload.html')

    return render_template('ws/upload.html')


@ws.route('/search',methods=['GET','POST'])
#cross_origin()
def searchProduct():
    if request.method=='POST':
        searchText=request.form.get('searchText')
        display=request.form.get('format')

        #return render_template('/productItem/'+searchText)
        flag='search'
        myresult=[]
        myresult=productItem(searchText,flag)

        if display=='pretty':
            return jsonify({"product":myresult})
        if myresult=='':
            myresult='No matching result found'
            return render_template('ws/search.html',output=myresult)
        else:
            return render_template('ws/resultset.html',output=myresult)
    return render_template('ws/search.html')

@ws.route('/productItem/<string:req>',methods=['GET'])
#cross_origin()
def productItem(req,flag=None):
    #print('request from angular app###############################',req)

    #initial query string
    SQLexpression='SELECT * FROM level '

    reqParam=req.split('$')
    rval=''
    if len(reqParam)>1:
        #print ('if condition')
        SQLexpression+='where '

        #start:assign value to different leveel based on input $ split
        if len(reqParam)==2:
            SQLexpression+='level1='+'\''+replaceSpecialChar(reqParam[0])+'\''+' and level2='+'\''+replaceSpecialChar(reqParam[1])+'\''
        if len(reqParam)==3:
            SQLexpression+='level1='+'\''+replaceSpecialChar(reqParam[0])+'\''+' and level2='+'\''+replaceSpecialChar(reqParam[1])+'\''+' and level3='+'\''+replaceSpecialChar(reqParam[2])+'\''
        if len(reqParam)==4:
            SQLexpression+='level1='+'\''+replaceSpecialChar(reqParam[0])+'\''+' and level2='+'\''+replaceSpecialChar(reqParam[1])+'\''+' and level3='+'\''+replaceSpecialChar(reqParam[2])+'\''+' and level4='+'\''+replaceSpecialChar(reqParam[3])+'\''
        #end:assign value to different leveel based on input $ split

        #rval='\''+reqParam[1]+'\''
        #print('*************SQLexpression*******************',SQLexpression)
        #SQLexpression+=reqParam[0]+'='+rval
        myresult=dbQuery(SQLexpression)
        print('request from angular app###############################',SQLexpression,'myresult++++++++++++++++')
    else:
        #free text search
        #print('search for free text',req)
        level='level'
        myresult=''
        for i in range(1,6):
            rval=replaceSpecialChar(reqParam[0])
            myresult=''
            SQLexpressionTmp=SQLexpression
            level+=str(i)
            rval='\''+rval+'\''
            SQLexpressionTmp+='where '
            SQLexpressionTmp+=level+'='+rval
            myresult=dbQuery(SQLexpressionTmp)
            if len(myresult)>0:
                break
            level='level'

    if flag=='search':
        return myresult

    #print('#########myresult#################',myresult)
    #return jsonify({"product":myresult})
    return jsonify({"product":myresult})
    #return render_template('resultset.html',output=myresult)

def dbQuery(SQLexpression):

        myresult=''
        cur = mysql.connection.cursor()
        cur.execute(SQLexpression)
        rows = cur.fetchall()
        column = [t[0] for t in cur.description]
        myjsonArr=[]
        levelObjArr=[]

        for row in rows:
            myjson = {column[0]: row[0], column[1]: row[1], column[2]: row[2], column[3]: row[3], column[4]: row[4], column[5]: row[5], column[6]: row[6], column[7]: row[7]
            ,column[8]:row[8],column[9]:row[9],column[10]:row[10]}
            #print('myjson ',myjson)
            myjsonArr.append(myjson)
            myresult = json.dumps(myjsonArr, indent=4)

        return myjsonArr

def replaceSpecialChar(req):
    print('before replaceSpecialChar',req)
    req=req.replace('~','/')
    print('replaceSpecialChar',req)
    return req
