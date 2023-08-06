
class textlib:
    if __name__ == "__main__":
        import csv
        chardict = {}

        def newchar(self, name):
            global chardict
            if not isinstance(name, str):
                print('TextLib error in \'newchar()\' statement can only pass the name as a string!')
            else:
                chardict[name] = {'Name': name}

        def charadd(self, atributename, value, charactername):
            if not isinstance(atributename, str) or not isinstance(charactername, str) or not isinstance(value, str):
                print(
                    'TextLib error in \'charadd()\' statement both the atributename, value, and charactername must be a string!')
            else:
                chardict[charactername][atributename] = value

        def atributevalue(self, charactername, atributename):
            if not isinstance(atributename, str) or not isinstance(charactername, str):
                print(
                    'TextLib error in \'atributevalue()\' statement both the atributename and charactername must be a string!')
            else:
                returnvar = chardict[charactername][atributename]
                return returnvar

        def savechar(self, charname, file):
            thatdict = chardict[charname]
            w = csv.writer(open(file, "w"))
            for key, val in thatdict.items():
                w.writerow([key, val])

        def loadchar(self, file):
            charname = 'None'
            w = csv.reader(open(file, "r"))
            for key, val in w:
                if key == 'Name':
                    charname = val
                    chardict[charname] = {}
                    chardict[charname][key] = val
                else:
                    chardict[charname][key] = val

