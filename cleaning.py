import pandas as pd

with open("data.csv", "r") as f:
    data = pd.read_csv(f)

person = {}
race = []
diabetese = {"249", "250", "251", "253", "258", "259", "261", "270", "271", "272", "275", "276", "285", "336", "337",
             "340", "345", "353", "354", "355", "357", "358", "362", "364", "366", "378", "443", "536", "581", "583",
             "588", "646", "652", "655", "674", "707", "709", "711", "713", "716", "730", "731", "751", "759", "775",
             "785", "787", "790", "962", "V12", "V18", "V65", "V77"}

diabeteseType1 = {}

diabeteseType2 = {}


class cleaning():

    def __init__(self):
        with open("data.csv", "r") as f:
            self.data = pd.read_csv(f)

    def setDiabeteseTwo(self):
        pass

    def setDiabeteseOne(self):
        pass

    def setDiabetesBool(self):
        pass

    def removeDiagnose(self):
        pass

    def dropIfDiagnose1abscent(self):
        # TODO add self var that does the total removed and print how many has been removed here
        pass

    def repairKeyWord(self, keyword):
        pass

    def removeAllEmpty(self):
        pass

    def removeAdmissionType_6_8(self):
        pass

    def discharge_disposition_id_18_25_26(self):
        pass

    def repair_speciality(self):
        pass

    def removeUnknownSex(self):
        pass

    def remove_examide(self):
        pass

    def remove_citoglipton(self):
        pass

    def remove_admission_source_id_9_20_21(self):
        pass

    def add_patient_exist_2(self):
        pass

    def save_data(self):
        pass

    def verifyChangeCorrect(self):
        pass

    def print_format(self):
        for col in self.data:
            print("{}:\t{}".format(col, self.data[col].unique()))

    def create_file_of_value(self):
        pass

    def run_cleaning(self):
        self.repairKeyWord("weight")
        self.repairKeyWord("race")
        self.repairKeyWord("payer_code")
        self.print_format()

    def check_max(self):
        parent = {}
        max = 0
        maxP = 0
        for i,row in self.data.iterrows():
            p = row["patient_nbr"]
            if p in parent:
                parent[p].append(p)
                if len(parent[p]) > 2:
                    print(p)
                if len(parent[p]) > max:
                    max = len(parent[p])
                    maxP = p
            else:
                parent[p] = []

            print(maxP)
            print(max)

    def yeet(self):
        for i,row in self.data.iterrows():
            if row["patient_nbr"] == 88785891:
                print(row)





c = cleaning()
c.print_format()
c.yeet()