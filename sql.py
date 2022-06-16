import sqlite3
import os
import hashlib

class SqlClass:
    def __init__(self, databasePath):
        self.databasePath = databasePath

    def executeSQL(self, command, parameters=None, fetchone=False):
        connect = sqlite3.connect(self.databasePath)
        cursor = connect.cursor()
        if parameters != None:
            commandReturn = cursor.execute(command, parameters).fetchone()[0] if fetchone else cursor.execute(command, parameters)
        else:
            commandReturn = cursor.execute(command).fetchone()[0] if fetchone else cursor.execute(command)
        connect.commit()
        cursor.close()
        return commandReturn

    def registerUser(self, username, tlf, email, password):
        salt = os.urandom(32)
        password_enc = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.executeSQL("""INSERT INTO Brugere (Navn, TLF, Email, Kode, Salt) VALUES (?,?,?,?,?);""", (username, tlf, email, password_enc, salt))
        
    def isCorrectPassword(self, username, enterdpassword):
        password = self.executeSQL("SELECT Kode FROM Brugere WHERE Navn = ?", [username], fetchone=True)
        salt = self.executeSQL(f"SELECT salt FROM Brugere WHERE Navn = ?", [username], fetchone=True)
        new_key = hashlib.pbkdf2_hmac('sha256', enterdpassword.encode('utf-8'), salt, 100000)
        if password == new_key:
            return True
        else: 
            return False 

    def GetTrainData(self):
        connect = sqlite3.connect(self.databasePath)
        trains = connect.execute(f'SELECT * FROM Tog').fetchall()
        trainData = []
        for train in trains:
            trainData.append({
                "name": train[0],
                "ID": train[1], 
                "imagePath": train[2]
                })
        connect.commit()
        connect.close()
        return trainData

    def addToCart(self, trainID):
        self.executeSQL(f'INSERT INTO Køb (trainID) VALUES ({trainID})')

    def getTrainDataByID(self, trainID):
        connect = sqlite3.connect(self.databasePath)
        trainData = connect.execute(f'SELECT * FROM Tog WHERE TID = {trainID}').fetchall()
        connect.commit()
        connect.close()
        return trainData
    
    def getCart(self):
        connect = sqlite3.connect(self.databasePath)
        trainIDs = connect.execute(f'SELECT * FROM Køb').fetchall()
        connect.commit()
        connect.close()
        return trainIDs
    
    def deleteCartItemById(self, id):
        self.executeSQL(f'DELETE FROM Køb WHERE trainID={id};')
        
