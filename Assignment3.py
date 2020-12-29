from faker import Faker
import csv
fake = Faker()
import random
import mysql.connector

#enter your information here
db = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    database=""
)
myCursor = db.cursor()

def generateCompletedKeys(userID):
    '''generate values for completed keys Table'''
    completes = [userID]
    for i in range(0,24):
        completes.append(fake.random_int(min=0,max=1))
    return completes


def generateLogin(userID):
    '''generate values for login Table'''
    return [userID,fake.name(),fake.password()]


def generateProfile(userID):
    '''generate values for profile Table'''
    key = "ABCDEFG"
    return [userID,fake.word(),random.choice(key),fake.word(),fake.word(),fake.last_name()]


def generateScores(userID):
    '''generate values for scores Table'''
    key = "ABCDEF"
    return [userID,random.choice(key),fake.random_int(min=0,max=600)]

def generateThemes(userID):
    '''generate values for themes Table'''
    return [userID, fake.color(),fake.color()]

def generateData(filename, numTuples):
    Faker.seed(0)
    csv_file = open(filename, 'w',newline='')

    writer = csv.writer(csv_file)
    for x in range(0, numTuples):
        randL = random.sample(range(1,10000),numTuples)
        id = randL.pop()
        writer.writerow(generateCompletedKeys(id) + generateLogin(id) + generateProfile(id)+ generateScores(id)+ generateThemes(id))

def importData(filename):
    with open(filename) as importFile:
        csvReader = csv.reader(importFile)
        for r in csvReader:
            #insert to completed keys table
            keyStrings= r[:25]
            keys = [int(i) for i in keyStrings]
            completeKeysInsert = '''INSERT INTO CompletedKeys(UserID,AMajorCompleted,CMajorCompleted,DMajorCompleted,EMajorCompleted,
            FMajorCompleted,BMajorCompleted,EFlatMajorCompleted,GFlatMajorCompleted,BFlatMajorCompleted,DFlatMajorCompleted,\
            AFlatMajorCompleted,GMajorCompleted,DMinorCompleted,AMinorCompleted,FMinorCompleted,BMinorCompleted,CMinorCompleted,\
            EMinorCompleted,ASharpMinorCompleted,DSharpMinorCompleted,GSharpMinorCompleted,CSharpMinorCompleted,FSharpMinorCompleted,
            GMinorCompleted) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})'''.format(*keys)
            try:
                myCursor.execute(completeKeysInsert)
                db.commit()
            except mysql.connector.Error as error:
                print("Insert failed {}".format(error))

            #insert to login table
            loginInfo = r[25:28]
            loginInfo[0] = int(loginInfo[0])
            loginInsert = '''INSERT INTO Login(UserID,Username,Password) VALUES ({},'{}','{}')'''.format(*loginInfo)
            try:
                myCursor.execute(loginInsert)
                db.commit()
            except mysql.connector.Error as error:
                print("Insert failed {}".format(error))

            #insert to profile table
            profileInfo = r[28:34]
            profileInfo[0] = int(profileInfo[0])
            profileInsert = '''INSERT INTO Profile(UserID,CurrentPieces,CurrentKeys,CompletedPieces,FavoritePieces,FavoriteComposers) 
            VALUES ({},'{}','{}','{}','{}','{}')'''.format(*profileInfo)
            try:
                myCursor.execute(profileInsert)
                db.commit()
            except mysql.connector.Error as error:
                print("Insert failed {}".format(error))

            # insert to scores table
            scoreInfo = r[34:37]
            scoreInfo[0] = int(scoreInfo[0])
            scoreInfo[2] = int(scoreInfo[2])
            scoreInsert = "INSERT INTO Scores(UserID,Grade,`High Score`) VALUES ({},'{}',{})".format(*scoreInfo)
            try:
                myCursor.execute(scoreInsert)
                db.commit()
            except mysql.connector.Error as error:
                print("Insert failed {}".format(error))
                print(scoreInsert)
            #insert to theme table
            themeInfo = r[36:39]
            themeInfo[0] = int(themeInfo[0])
            themeInsert = '''INSERT INTO Themes(UserID,`First Color`,`Second Color`) VALUES ({},'{}','{}')'''.format(*themeInfo)
            try:
                myCursor.execute(themeInsert)
                db.commit()
            except mysql.connector.Error as error:
                print("Insert failed {}".format(error))




def userInput():
    while True:
        choice = input("Enter 1 to generate data to a csv file, enter 2 to choose a file to import from,enter 3 to exit ")
        if choice == "1":
            fileChoice = input("Enter filename to export to ")
            numTuples = input("Enter number of tuples for file ")
            if int(numTuples) < 1 or int(numTuples) > 1000:
                 print("Enter a reasonable number of tuples ")
                 continue
            generateData(fileChoice,int(numTuples))
        elif choice == "2":
            fileChoice = input("Enter filename to import from ")
            importData(fileChoice)
        elif choice == "3":
            break

def main():
    userInput()


if __name__ == '__main__':
    main()
