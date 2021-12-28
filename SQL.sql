CREATE TABLE temp (
    ruleID varchar(6),
    CFD int,
    gejalaID varchar(5),
    penyakitID varchar(5),
    PRIMARY KEY (ruleID)
);

CREATE TABLE pasien (
    pasienID varchar(6),
    rekamMedID varchar(6),
    pasienNama varchar(20),
    pasienGender int,
    umur int,
    PRIMARY KEY (pasienID)
);

CREATE TABLE rekammed (
    rekamID varchar(255),
    pasienID varchar(255),
    penyakitID varchar(255),
    gejalaID varchar(255),
    CFP float,
    penyakitDia varchar(255),
    PRIMARY KEY (rekamID)
);

DROP PROCEDURE IF EXISTS insertRowsToRules;
DELIMITER //
CREATE PROCEDURE insertRowsToRules()   
BEGIN
DECLARE i INT DEFAULT 1; 
WHILE (i <= 6) DO
    INSERT INTO rules()
    SET i = i+1;
END WHILE;
END;
//  
DELIMITER ;

INSERT INTO rules(gejalaID)
SELECT gejalaID
FROM gejala

DROP keluhan;

CREATE TABLE tempG 
AS (
    SELECT rules.gejalaID,rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD
    FROM keluhan
    INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc
    WHERE keluhan.CFU != "0" and rules.CFD != "0"
    ORDER BY keluhan.gejalaDesc
);

DROP TABLE tempg;
select count(*) from penyakit;
select count(*) from keluhan;
select * FROM keluhan;
select * FROM keluhan1;

SELECT rules.gejalaID,rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD, (keluhan.CFU*rules.CFD) as CFCOMBI
FROM keluhan
INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc
WHERE keluhan.CFU != "0" and rules.CFD != "0"
ORDER BY keluhan.gejalaDesc;

SELECT CFU, try_convert(float,[CFU]) as [Varchar to float]
FROM keluhan 

select 0 + CFU from keluhan;
select cast(CFU AS DECIMAL(10,2)) as 'CFU' from keluhan;

UPDATE keluhan SET CFU = CAST(CFU AS DECIMAL(10,6));

UPDATE keluhan1 SET CFCOMBI = CFU * CFD;

SELECT gejalaID,GROUP_CONCAT(penyakitID)
FROM rules
GROUP BY gejalaID;

SELECT penyakitNama,gejalaDesc, CFCOMBI FROM keluhan1 GROUP BY penyakitNama;

select tableExistsOrNot("gejala");

SELECT * FROM keluhan1 GROUP BY penyakitNama;
SELECT penyakitNama FROM keluhan1 GROUP BY penyakitNama;

DROP PROCEDURE IF EXISTS coba;
DELIMITER //
CREATE PROCEDURE coba()   
BEGIN
DECLARE i INT DEFAULT 1; 
WHILE (i <= COUNT(*)) DO
    INSERT INTO rules()
    SET i = i+1;
END WHILE;
END;
//  
DELIMITER ;
truncate temp;

CREATE TABLE temp AS (SELECT rules.gejalaID, rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD, keluhan.CFU*rules.CFD as CFCOMBI FROM keluhan INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc WHERE keluhan.CFU != '0' AND rules.CFD != '0' ORDER BY keluhan.gejalaDesc)

INSERT INTO temp (gejalaID, penyakitID, gejalaDesc, PenyakitNama, CFU, CFD, CFCOMBI)
SELECT rules.gejalaID,rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD, (keluhan.CFU*rules.CFD) as CFCOMBI
FROM keluhan
INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc
WHERE keluhan.CFU != "0" and rules.CFD != "0"
ORDER BY keluhan.gejalaDesc;

INSERT INTO rekammed(penyakitID,gejalaID,CFU,penyakitDia) FROM keluhan1

UPDATE temp
SET     = #Table2.address,
       phone2 = #Table2.phone
FROM   #Table2
WHERE  #Table2.gender = #Table1.gender
       AND #Table2.birthdate = #Table1.birthdate 

SELECT *
FROM rekammed
GROUP BY gejalaDesc;

SELECT MAX(CFU),GROUP_CONCAT(penyakitDia) FROM rekammed;
SELECT * FROM rekammed;

#PAKE YANG INI
CREATE TABLE rekammed2 AS(
SELECT gejalaDesc, MAX(CFU) as 'CFU MAX', MIN(CFU) as 'CFU MIN', count(gejalaDesc) from rekammed group by gejalaDesc )

INSERT INTO keluhan1 (gejalaID, penyakitID, gejalaDesc, PenyakitNama, CFU, CFD, CFCOMBI) 
SELECT rules.gejalaID,rules.penyakitID, keluhan.gejalaDesc, rules.penyakitNama, keluhan.CFU, rules.CFD, (keluhan.CFU*rules.CFD) as CFCOMBI 
FROM keluhan INNER JOIN rules ON keluhan.gejalaDesc=rules.gejalaDesc 
WHERE keluhan.CFU != '0' and rules.CFD != '0' AND NOT EXISTS (SELECT * FROM keluhan1) 
ORDER BY keluhan.gejalaDesc

SELECT * from rekammed where penyakitDia = 'Periodontitis' group by pasienNama


#SELECT 20 DATA TESTING RANDOM
DROP TABLE testing
CREATE TABLE testing as ( SELECT pasienNama, GROUP_CONCAT(gejalaDesc), penyakitDia FROM rekammed group by pasienNama ORDER BY RAND() LIMIT 20 )

# RESET SEMENTARA
TRUNCATE rekammed2;
TRUNCATE keluhan3;
TRUNCATE rekammed3;

DROP TABLE ktest
CREATE TABLE ktest as (SELECT testing.pasienNama,rekammed.gejalaDesc, rekammed.CFU, testing.penyakitDia 
FROM testing
LEFT JOIN rekammed
ON rekammed.pasienNama = testing.pasienNama)

####DATA TRAIN SEMENTARA ####

INSERT INTO rekammed2 (gejalaDesc,CFUMAX,CFUMIN,totGejala) 
SELECT gejalaDesc, MAX(CFU), MIN(CFU), count(gejalaDesc) 
FROM rekammed 
WHERE NOT EXISTS (SELECT * FROM rekammed2) 
GROUP BY rekammed.gejalaDesc;

#data testing yg normalized 
INSERT INTO keluhan3 (pasienNama, gejalaDesc, CFU,CFUMAX,CFUMIN,NORM)
SELECT ktest.pasienNama, ktest.gejalaDesc, ktest.CFU, rekammed2.CFUMAX,rekammed2.CFUMIN, ((ktest.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM'
from ktest
INNER JOIN rekammed2
ON rekammed2.gejalaDesc = ktest.gejalaDesc
WHERE NOT EXISTS (SELECT * FROM keluhan3);

#data training yg normalized 
INSERT INTO rekammed3 (pasienNama,gejalaDesc,CFU,CFUMAX,CFUMIN,NORM,penyakitDia) 
SELECT rekammed.pasienNama,rekammed2.gejalaDesc, rekammed.CFU,rekammed2.CFUMAX,rekammed2.CFUMIN, ((rekammed.CFU-rekammed2.CFUMIN)/(rekammed2.CFUMAX-rekammed2.CFUMIN)) AS 'NORM', rekammed.penyakitDia
FROM rekammed
INNER JOIN rekammed2
ON rekammed2.gejalaDesc = rekammed.gejalaDesc
WHERE NOT EXISTS (SELECT * FROM rekammed3)
ORDER BY rekammed.rekamID;

UPDATE rekammed3 SET NORM = '0' where NORM is NULL;
####


SELECT gejalaDesc, MAX(CFU) as 'CFU MAX', MIN(CFU) as 'CFU MIN',  from keluhan group by gejalaDesc;
SELECT * FROM rekammed WHERE pasienNama = 'Jamila';

DELETE FROM pasien WHERE pasienNama = 'Jamila'

SELECT * FROM rekammed3
ORDER BY RAND()
LIMIT 10

#UPDATE DATA PASIEN
UPDATE rekammed SET pasienNama = 'Pasien 50' where pasienNama = 'Januar';
UPDATE pasien SET pasienNama = 'Pasien 50' where pasienNama = 'Januar';
SELECT * FROM rekammed Group by pasienNama order by rekamID;


#SPLIT DATA RANDOM
WITH TEMP
(
  SELECT rekamID AS ROW_ID,RAND() as RANDOM_VALUE, R.*
  FROM rekammed R
  ORDER BY RANDOM_VALUE
)

SELECT 'Training',T.* FROM TEMP T
WHERE ROW_ID =< 375
UNION
SELECT 'Test',T.* FROM TEMP T
WHERE ROW_ID > 375

SELECT pasienNama,gejalaDesc,CFU,penyakitDia FROM rekammed WHERE rekamID > 324

INSERT INTO rekammed2 (gejalaDesc,CFUMAX,CFUMIN,totGejala) SELECT gejalaDesc, MAX(CFU), MIN(CFU), count(gejalaDesc) FROM rekammed GROUP BY rekammed.gejalaDesc

SELECT * FROM rules where penyakitNama = 'Abses Gigi' and gejalaDesc = 'Demam'

SELECT * FROM rekammed3 where pasienNama = 'Ayana';

SELECT rekammed.pasienNama,gejala.gejalaID, rekammed.gejalaDesc, rekammed.CFU, rekammed.penyakitDia 
FROM rekammed 
INNER JOIN gejala
ON gejala.gejalaDesc = rekammed.gejalaDesc

SELECT rekammed.pasienNama,gejala.gejalaID,rekammed.gejalaDesc, rekammed.CFU, rekammed.penyakitDia, penyakit.penyakitID
FROM rekammed
JOIN gejala
ON gejala.gejalaDesc = rekammed.gejalaDesc
JOIN penyakit
ON penyakit.penyakitNama = rekammed.penyakitDia;
