from flask import Flask, g, flash, render_template, url_for, request, session, redirect,jsonify
from random import shuffle
import pandas as pd
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader,Template
import MySQLdb.cursors
import re
import math


app = Flask(__name__)
app.config["SECRET_KEY"] = "thisisMysecretkey"

# config DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'essks'
mysql = MySQL(app)

#LOGIN LOGOUT REGISTER#

@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for('index'))
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['userID']
            session['username'] = account['username']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM penyakit")
            penyakit= cur.fetchall()
            cur.execute("SELECT * FROM gejala")
            gejala= cur.fetchall()
            cur.execute("SELECT * FROM rules")
            rules= cur.fetchall()
            cur.execute("SELECT * FROM rekammed")
            rm = cur.fetchall()
            cur.close()
            return render_template('index.html', msg = msg, username = username,p=penyakit,g=gejala,r=rules,rm = rm)
        else:
            msg = "WRONG USERNAME/PASSWORD"
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#=====PAGES======#

@app.route("/index")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penyakit")
    penyakit= cur.fetchall()
    cur.execute("SELECT * FROM gejala")
    gejala= cur.fetchall()
    cur.execute("SELECT * FROM rules")
    rules= cur.fetchall()
    cur.execute("SELECT * FROM rekammed")
    rm = cur.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template('index.html',p=penyakit,g=gejala,r=rules,rm = rm,username=session['username']) 
    else:
        return render_template('index.html',p=penyakit,g=gejala,r=rules,rm = rm)

@app.route("/keluhan")
def keluhan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM keluhan")
    keluhan = cur.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template('keluhan.html',data=keluhan, username=session['username']) 
    return render_template('keluhan.html',data=keluhan)

@app.route("/iniDiagnosis", methods=["GET","POST"])
def iniDiagnosis():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM keluhan")
    k = cur.fetchall()
    # Keluhan1 adalah table temp. (tidak ke save di mySQL, tapi value ke store di jinja)
    cur.execute("INSERT INTO keluhan1 (gejalaID, penyakitID, gejalaDesc, PenyakitNama, CFU, CFD, CFCOMBI) SELECT rules.gejalaID,rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD, (keluhan.CFU*rules.CFD) as CFCOMBI FROM keluhan INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc WHERE keluhan.CFU != '0' and rules.CFD != '0' AND NOT EXISTS (SELECT * FROM keluhan1) ORDER BY keluhan.gejalaDesc") 
    cur.execute("SELECT * from keluhan1")
    keluhan = cur.fetchall()
    cur.execute("SELECT penyakitNama,GROUP_CONCAT(gejalaDesc), GROUP_CONCAT(CFU*CFD) FROM keluhan1 GROUP BY penyakitNama;")
    keluhann = cur.fetchall()
    cur.execute("SELECT penyakitNama FROM keluhan1 GROUP BY penyakitNama")
    keluhannn = cur.fetchall()
    # cur.execute("INSERT INTO rekammed2 (gejalaDesc,CFUMAX,CFUMIN,totGejala) SELECT gejalaDesc, MAX(CFU), MIN(CFU), count(gejalaDesc) FROM rekammed WHERE NOT EXISTS (SELECT * FROM rekammed2) GROUP BY rekammed.gejalaDesc;")
    cur.close()
    if 'loggedin' in session:
        return render_template('inidiagnosisnya.html',data=keluhan,dataa=keluhann,dataaa=keluhannn,datak = k, username=session['username']) 
    return render_template('inidiagnosisnya.html',data=keluhan,dataa=keluhann,dataaa=keluhannn,datak = k)


@app.route("/infogejala")
def infogejala():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gejala")
    gejala = cur.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template('infogejala.html',username=session['username'], data=gejala)
    return render_template('infogejala.html', data = gejala)

@app.route("/infopenyakit")
def infopenyakit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM penyakit")
    penyakit = cur.fetchall()
    cur.close()
    if 'loggedin' in session:
        return render_template('infopenyakit.html',username=session['username'], data=penyakit)
    return render_template('infopenyakit.html', data=penyakit)

@app.route("/basispengetahuan")
def basispengetahuan():
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM rules")
    rules = curr.fetchall()
    curr.close()
    if 'loggedin' in session:
        return render_template('basispengetahuan.html',username=session['username'], data=rules)
    return render_template('basispengetahuan.html', data=rules)
    
@app.route("/tambahgejala")
def tambahgejala():
    return render_template('tambahgejala.html')


@app.route("/knn")
def knn():
    if 'loggedin' in session:
        cur = mysql.connect.cursor()
        cur.execute("SELECT * from keluhan")
        c = cur.fetchall()
        cur.execute("SELECT pasienNama, GROUP_CONCAT(gejalaDesc), penyakitDia FROM rekammed GROUP BY pasienNama ORDER BY RAND() LIMIT 5;")
        rm = cur.fetchall()
        cur.execute("INSERT INTO rekammed2 (gejalaDesc,CFUMAX,CFUMIN,totGejala) SELECT gejalaDesc, MAX(CFU), MIN(CFU), count(gejalaDesc) FROM rekammed WHERE NOT EXISTS (SELECT * FROM rekammed2) GROUP BY rekammed.gejalaDesc")
        cur.execute("SELECT * FROM rekammed2")
        dm = cur.fetchall()
        cur.execute("SELECT pasienNama FROM pasien GROUP BY pasienNama")
        pasien = cur.fetchall()
        cur.execute("INSERT INTO keluhan3 (gejalaDesc, CFU,CFUMAX,CFUMIN,NORM) SELECT keluhan.gejalaDesc, keluhan.CFU, rekammed2.CFUMAX,rekammed2.CFUMIN, ((keluhan.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM' from keluhan LEFT JOIN rekammed2 ON rekammed2.gejalaDesc = keluhan.gejalaDesc WHERE NOT EXISTS (SELECT * FROM keluhan3)")
        cur.execute("SELECT * FROM keluhan3")
        k3 = cur.fetchall()
        cur.execute("INSERT INTO rekammed3 (pasienNama,gejalaDesc,CFU,CFUMAX,CFUMIN,NORM,penyakitDia) SELECT rekammed.pasienNama,rekammed2.gejalaDesc, rekammed.CFU,rekammed2.CFUMAX,rekammed2.CFUMIN, ((rekammed.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM', rekammed.penyakitDia FROM rekammed LEFT JOIN rekammed2 ON rekammed2.gejalaDesc = rekammed.gejalaDesc WHERE NOT EXISTS (SELECT * FROM rekammed3) ORDER BY rekammed.pasienNama")
        cur.execute("SELECT * FROM rekammed3")
        r3 = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('knn.html',data=rm,datamm=dm,pasien=pasien,k3=k3,r3=r3,c=c,username=session['username'])
    return redirect(url_for('login'))


@app.route("/tambahpenyakit")
def tambahpenyakit():
    return render_template('tambahpenyakit.html')


@app.route("/diagnosispenyakit")
def diagnosispenyakit():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gejala")
    gejala = cur.fetchall()
    cur.execute("select * from keluhan;")
    keluhan = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if 'loggedin' in session:
        return render_template('diagnosispenyakit.html', data = gejala, datak = keluhan, username=session['username']) 
    return render_template('diagnosispenyakit.html', data = gejala, datak = keluhan)

@app.route("/tentang")
def tentang():
    if 'loggedin' in session:
        return render_template('tentang.html',username=session['username']) 
    else:
        return render_template('tentang.html')
        
@app.route("/k")
def k():
    if 'loggedin' in session:
        return render_template('k.html',username=session['username'])
    return redirect(url_for('login'))
    

@app.route("/riwayatpasien")
def riwayatpasien():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT pasienNama, GROUP_CONCAT(gejalaDesc), penyakitDia FROM rekammed GROUP BY pasienNama ORDER BY rekamID;")
        rm = cur.fetchall()
        cur.close()
        return render_template('riwayatpasien.html',data=rm,username=session['username'])
    return redirect(url_for('login'))

@app.route("/riwayatpasien2")
def riwayatpasien2():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM gejala")
        gejala = cur.fetchall()
        cur.execute("SELECT * FROM ex")
        ex = cur.fetchall()
        cur.close()
        return render_template('riwayatpasien2.html', gejala=gejala, data = ex,username=session['username'])
    return redirect(url_for('login'))


@app.route("/knnA")
def knnA():
    cur = mysql.connect.cursor()
    # Untuk bikin database testing
    # cur.execute("CREATE TABLE testing AS (SELECT pasienNama, GROUP_CONCAT(gejalaDesc), penyakitDia FROM rekammed GROUP BY pasienNama ORDER BY RAND() LIMIT 20)")
    cur.execute("SELECT * FROM testing")
    rm = cur.fetchall()
    # cur.execute("INSERT INTO rekammed2 (gejalaDesc,CFUMAX,CFUMIN,totGejala) SELECT gejalaDesc, MAX(CFU), MIN(CFU), count(gejalaDesc) FROM rekammed WHERE NOT EXISTS (SELECT * FROM rekammed2) GROUP BY rekammed.gejalaDesc")
    cur.execute("SELECT * FROM rekammed2")
    dm = cur.fetchall()
    cur.execute("SELECT pasienNama FROM pasien")
    pasien = cur.fetchall()
    # cur.execute("INSERT INTO keluhan3 (gejalaDesc, CFU,CFUMAX,CFUMIN,NORM) SELECT keluhan.gejalaDesc, keluhan.CFU, rekammed2.CFUMAX,rekammed2.CFUMIN, ((keluhan.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM' from keluhan LEFT JOIN rekammed2 ON rekammed2.gejalaDesc = keluhan.gejalaDesc WHERE NOT EXISTS (SELECT * FROM keluhan3)")
    cur.execute("SELECT * FROM keluhan3")
    k3 = cur.fetchall()
    # cur.execute("INSERT INTO rekammed3 (pasienNama,gejalaDesc,CFU,CFUMAX,CFUMIN,NORM,penyakitDia) SELECT rekammed.pasienNama,rekammed2.gejalaDesc, rekammed.CFU,rekammed2.CFUMAX,rekammed2.CFUMIN, ((rekammed.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM', rekammed.penyakitDia FROM rekammed LEFT JOIN rekammed2 ON rekammed2.gejalaDesc = rekammed.gejalaDesc WHERE NOT EXISTS (SELECT * FROM rekammed3) ORDER BY rekammed.pasienNama")
    # cur.execute("UPDATE rekammed3 SET NORM = '0' where NORM is NULL;")
    cur.execute("SELECT * FROM rekammed3")
    r3 = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('knnA.html',data=rm,datamm=dm,pasien=pasien,k3=k3,r3=r3,username=session['username'])

@app.route('/dataset')
def dataset():
	items = ReadData('rekammed.txt')
	items = pd.DataFrame(items)
	return render_template('dataset.html',items=items.to_html(classes='table table-striped table-hover table-bordered table-sm table-responsive-sm'))


@app.route('/sakti', methods=['GET','POST'])
def sakti():
    GP01 = 0 
    GP02 = 0 
    GP03 = 0 
    GP04 = 0 
    GP05 = 0 
    GP06 = 0 
    GP07 = 0 
    GP08 = 0 
    GP09 = 0 
    GP10 = 0 
    GP11 = 0 
    GP12 = 0 
    GP13 = 0 
    GP14 = 0 
    GP15 = 0 
    GP16 = 0 
    GP17 = 0 
    GP18 = 0 
    GP19 = 0 
    GP20 = 0 
    GP21 = 0 
    GP22 = 0 
    GP23 = 0 
    GP24 = 0 
    GP25 = 0 
    GP26 = 0 
    GP27 = 0 
    GP28 = 0
    
    cur = mysql.connect.cursor()
    
    #template data testing
    newItem = {'GP01': 0 ,'GP02': 0,'GP03': 0,'GP04': 0,'GP05': 0,'GP06': 0,'GP07': 0,'GP08': 0,'GP09': 0,'GP10': 0,'GP11': 0,'GP12': 0,'GP13': 0,'GP14': 0,'GP15': 0,'GP16': 0,'GP17': 0,'GP18': 0,'GP19': 0,'GP20': 0,'GP21': 0,'GP22': 0,'GP23': 0,'GP24': 0,'GP25': 0,'GP26': 0,'GP27': 0,'GP28': 0}

    cur.execute("SELECT keluhan.gejalaDesc, keluhan.CFU, gejala.gejalaID from keluhan inner join gejala ON gejala.gejalaDesc = keluhan.gejalaDesc")
    c = cur.fetchall()

    cur.execute("SELECT gejala.gejalaID, keluhan.CFU from keluhan inner join gejala on gejala.gejalaDesc = keluhan.gejalaDesc")
    da = cur.fetchall()
    for dar in da:
        if dar[0] == "GP01":
            GP01 = float(dar[1])
        elif dar[0] == "GP02":
            GP02 = float(dar[1])
        elif dar[0] == "GP03":
            GP03 = float(dar[1])
        elif dar[0] == "GP04":
            GP04 = float(dar[1])
        elif dar[0] == "GP05":
            GP05 = float(dar[1])
        elif dar[0] == "GP06":
            GP06 = float(dar[1])
        elif dar[0] == "GP07":
            GP07 = float(dar[1])
        elif dar[0] == "GP08":
            GP08 = float(dar[1])
        elif dar[0] == "GP09":
            GP09 = float(dar[1])
        elif dar[0] == "GP10":
            GP10 = float(dar[1])
        elif dar[0] == "GP11":
            GP11 = float(dar[1])
        elif dar[0] == "GP12":
            GP12 = float(dar[1])
        elif dar[0] == "GP13":
            GP13 = float(dar[1])
        elif dar[0] == "GP14":
            GP14 = float(dar[1])
        elif dar[0] == "GP15":
            GP15 = float(dar[1])
        elif dar[0] == "GP16":
            GP16 = float(dar[1])
        elif dar[0] == "GP17":
            GP17 = float(dar[1])
        elif dar[0] == "GP18":
            GP18 = float(dar[1])
        elif dar[0] == "GP19":
            GP19 = float(dar[1])
        elif dar[0] == "GP20":
            GP20 = float(dar[1])
        elif dar[0] == "GP21":
            GP21 = float(dar[1])
        elif dar[0] == "GP22":
            GP22 = float(dar[1])
        elif dar[0] == "GP23":
            GP23 = float(dar[1])
        elif dar[0] == "GP24":
            GP24 = float(dar[1])
        elif dar[0] == "GP25":
            GP25 = float(dar[1])
        elif dar[0] == "GP26":
            GP26 = float(dar[1])
        elif dar[0] == "GP27":
            GP27 = float(dar[1])
        elif dar[0] == "GP28":
            GP28 = float(dar[1])
         
    items = ReadData('rekammed.txt')
    
    # data testing
    newItem = {'GP01': GP01 ,'GP02': GP02,'GP03': GP03, 'GP04': GP04,'GP05': GP05,'GP06': GP06,'GP07': GP07,'GP08': GP08,'GP09': GP09,'GP10': GP10,'GP11': GP11,'GP12': GP12,'GP13': GP13,'GP14': GP14,'GP15': GP15,'GP16': GP16,'GP17':GP17,'GP18': GP18,'GP19': GP19,'GP20': GP20,'GP21': GP21,'GP22': GP22,'GP23': GP23,'GP24': GP24,'GP25': GP25,'GP26': GP26,'GP27': GP27,'GP28': GP28}
        
    k = 6
    accuracy2, maxi, count, neighbors = Classify(newItem, k, items)
    skor = pd.DataFrame(neighbors, columns = ['Skor Euclidean' , 'Diagnosis'])
    keputusan = pd.DataFrame(list(count.items()), columns=['Diagnosis', 'Jumlah Kemunculan'])
    
    mysql.connection.commit()
    if 'loggedin' in session:
        return render_template('sakti.html', keputusan=keputusan.to_html(classes='table table-striped table-hover table-bordered table-sm table-responsive-sm'), skor=skor.to_html(classes='table table-striped table-hover table-bordered table-sm table-responsive-sm'), ni=newItem, data=c, evaluat=accuracy2, items=items, k=k,username=session['username'])      
    return render_template('sakti.html', keputusan=keputusan.to_html(classes='table table-striped table-hover table-bordered table-sm table-responsive-sm'), skor=skor.to_html(classes='table table-striped table-hover table-bordered table-sm table-responsive-sm'), ni=newItem, data=c, evaluat=accuracy2, items=items, k=k)


#=====FUNCTIONS=====#

@app.route('/hapusPenyakit/<string:id_data>', methods=["GET"])
def hapusPenyakit(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM penyakit WHERE penyakitID=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('infopenyakit'))

@app.route('/updatePenyakit', methods=["POST"])
def updatePenyakit():
    namaPenyakit = request.form['namaPenyakit']
    defPenyakit = request.form['definisPenyakit']
    solPenyakit = request.form['solusiPenyakit']
    pi1 = request.form['np1']
    pi2 = request.form['np2']
    pi3 = request.form['np3']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE penyakit SET penyakitNama=%s WHERE penyakitNama=%s", (namaPenyakit,pi1))
    cur.execute("UPDATE penyakit SET penyakitDefinisi=%s WHERE penyakitDefinisi=%s", (defPenyakit,pi2))
    cur.execute("UPDATE penyakit SET penyakitSolusi=%s WHERE penyakitSolusi=%s", (solPenyakit,pi3))
    mysql.connection.commit()
    return redirect(url_for('infopenyakit'))

@app.route('/hapusGejala/<string:id_data>', methods=["GET"])
def hapusGejala(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM gejala WHERE gejalaID=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('infogejala'))

@app.route('/hapusGejalaExt/<string:id_data>', methods=["GET"])
def hapusGejalaExt(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM keluhan WHERE keluhanID=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('keluhan'))

@app.route('/updateGejala', methods=["POST"])
def updateGejala():
    gejala = request.form['gejala']
    pi1 = request.form['np1']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE gejala SET gejalaDesc=%s WHERE gejalaDesc=%s", (gejala,pi1))
    mysql.connection.commit()
    return redirect(url_for('infogejala'))

@app.route("/hapusRekamMedis")
def hapusRekamMedis():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE keluhan")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('diagnosispenyakit'))

@app.route('/resetDataTesting/<string:id_data>', methods=["GET,POST"])
def resetDataTesting(id_data):
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE testing AS (SELECT pasienNama, GROUP_CONCAT(gejalaDesc), penyakitDia FROM rekammed GROUP BY pasienNama ORDER BY RAND() LIMIT %s", (id_data))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('knnA'))

@app.route("/simpanPilihanGejala", methods=["POST"])
def simpanPilihanGejala():
    gejalaChoosen = request.form["gejalaChoosen"]
    gejalanya = request.form["gejalaApaIni"]
    if 'radioName' not in request.form:
        print('Error: The form is empty')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO keluhan(gejalaDesc, CFU) VALUES(%s,%s)",(gejalanya, gejalaChoosen))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('diagnosispenyakit'))

@app.route("/simpanFormPenyakit", methods=["POST"])
def simpanFormPenyakit():
    idPenyakit = request.form["idPenyakit"]
    namaPenyakit = request.form["namaPenyakit"]
    definisPenyakit = request.form["definisPenyakit"]
    solusiPenyakit = request.form["solusiPenyakit"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO penyakit(penyakitID,penyakitNama,penyakitSolusi,penyakitDefinisi) VALUES(%s,%s,%s,%s)", (idPenyakit,namaPenyakit,definisPenyakit,solusiPenyakit))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('infopenyakit'))

@app.route("/simpanFormGejala", methods=["POST"])
def simpanFormGejala():
    kodeGejala = request.form["kodeGejala"]
    namaGejala = request.form["namaGejala"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO gejala(gejalaID,gejalaDesc) VALUES(%s,%s)", (kodeGejala,namaGejala))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('infogejala'))

@app.route("/simpanRekamMedis", methods=["POST"])
def simpanRekamMedis():
    namaPasien = request.form["namaPasien"]
    umurPasien = request.form["umurPasien"]
    genderPasien = request.form["genderPasien"]
    np2 = request.form["np2"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pasien(pasienNama,pasienGender,pasienUmur) VALUES(%s,%s,%s)", (namaPasien,genderPasien,umurPasien))
    cur.execute("INSERT INTO rekammed(gejalaDesc,CFU,rmTEMP) SELECT gejalaDesc,CFU,'1' FROM keluhan")
    cur.execute("UPDATE rekammed SET pasienNama=%s WHERE rmTEMP=%s",(namaPasien,'1'))
    cur.execute("UPDATE rekammed SET penyakitDia=%s WHERE rmTEMP=%s",(np2,'1'))
    cur.execute("UPDATE rekammed SET rmTEMP = '0'")
    cur.execute("TRUNCATE keluhan")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('diagnosispenyakit'))

def ReadData(fileName):
	#dataset
	f = open(fileName, 'r')
	lines = f.read().splitlines()
	f.close()

	#feature
	features = lines[0].split(',')[:-1]

	#list
	items = []
	for i in range(1, len(lines)):
		line = lines[i].split(',')
		itemFeatures = {'Class': line[-1]}
		#Iterate feature
		for j in range(len(features)):
			# Get the feature at index j
			f = features[j]
			# Convert feature value to float
			v = float(line[j])
			# Add feature value to dict
			itemFeatures[f] = v
		#Append temp dict to items
		items.append(itemFeatures)
	#shuffle(items) 
	return items


def EuclideanDistance(x,y):
	S=0
	for key in x.keys():
		S += math.pow(x[key]-y[key], 2)
	return math.sqrt(S)

def CalculateNeighborsClass(neighbors,k):
	count = {}
	for i in range(k):
		if neighbors[i][1] not in count:
			count[neighbors[i][1]] = 1
		else:
			count[neighbors[i][1]] += 1
	return count

def FindMax(Dict):
	maximum = -1
	classification = ''

	for key in Dict.keys():
		if Dict[key] > maximum:
			maximum = Dict[key]
			classification = key
	return classification, maximum

def Classify(nItem, k, Items):
	if (k > len(Items)):
		return "k larger than list length"

	neighbors = []
	distance2 =  []
	for item in Items:
		#Find Euclidean Distance
		distance = EuclideanDistance(nItem, item)
		distance2.append(distance)
		#Update neigbors
		neigbors = UpdateNeighbors(neighbors,item,distance,k)
	#Count number each class
	count = CalculateNeighborsClass(neighbors, k)
	#find the max in count / class with the most appearances
	klas,maxi = FindMax(count)

	return klas, maxi, count, neighbors

def UpdateNeighbors(neighbors,item,distance,k):
	if len(neighbors) < k:
		neighbors.append([distance, item['Class']])
		neighbors = sorted(neighbors)
	else:
		if neighbors[-1][0] > distance:
			neighbors[-1] = [distance, item['Class']]
			neighbors = sorted(neighbors)
	return neighbors


##############################################################################################################

if __name__ == "__main__":
    app.run(debug=True)