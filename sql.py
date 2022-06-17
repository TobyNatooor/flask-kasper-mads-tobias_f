import sqlite3
import os
import hashlib

class SqlClass:
    def __init__(self, databasePath):
        self.databasePath = databasePath

    def registerUser(self, username, tlf, email, password):
        salt = os.urandom(32)
        password_enc = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        connect = sqlite3.connect(self.databasePath)
        connect.execute("""INSERT INTO Brugere (Navn, TLF, Email, Kode, Salt) VALUES (?,?,?,?,?);""", (username, tlf, email, password_enc, salt))
        connect.commit()
        connect.close()

    def isCorrectPassword(self, username, enterdpassword):
        connect = sqlite3.connect(self.databasePath)
        password = connect.execute(f'SELECT Kode FROM Brugere WHERE Navn = "{username}"').fetchone()[0]
        salt = connect.execute(f'SELECT salt FROM Brugere WHERE Navn = "{username}"').fetchone()[0]
        new_key = hashlib.pbkdf2_hmac('sha256', enterdpassword.encode('utf-8'), salt, 100000)
        connect.commit()
        connect.close()
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
                "imagePath": train[2],
                
                })
        connect.commit()
        connect.close()
        return trainData

    def addToCart(self, trainID):
        connect = sqlite3.connect(self.databasePath)
        connect.execute(f'INSERT INTO Køb (trainID) VALUES ({trainID})')
        connect.commit()
        connect.close()

    def getTrainDataByID(self, trainID):
        connect = sqlite3.connect(self.databasePath)
        trainData = connect.execute(f'SELECT * FROM Tog WHERE TID = {trainID}').fetchall()
        trainDataDict = {
            "name": trainData[0][0],
            "price": trainData[0][3],
            "image": trainData[0][2],
            "id": trainData[0][1],
        }
        connect.commit()
        connect.close()
        return trainDataDict
    
    def getCart(self):
        connect = sqlite3.connect(self.databasePath)
        trainIDs = connect.execute(f'SELECT * FROM Køb').fetchall()
        connect.commit()
        connect.close()
        return trainIDs
    
    def deleteCartItemById(self, id):
        connect = sqlite3.connect(self.databasePath)
        connect.execute(f'DELETE FROM Køb WHERE trainID={id};')
        connect.commit()
        connect.close()
        
    def addReview(self, name, text, trainID):
        connect = sqlite3.connect(self.databasePath)
        connect.execute(f'INSERT INTO Reviews (name, text, trainID) VALUES (?, ?, ?)', (name, text, trainID))
        connect.commit()
        connect.close()
        
    def getTrainReviews(self, trainID):
        connect = sqlite3.connect(self.databasePath)
        trainReviews = connect.execute(f'SELECT * FROM Reviews WHERE trainID = {trainID}').fetchall()
        trainReviewsDict = []
        for trainReview in trainReviews:
            trainReviewsDict.append({
                "name": trainReview[1],
                "text": trainReview[2],
                "trainID": trainReview[3],
            })
        connect.commit()
        connect.close()
        return trainReviewsDict
