import re

import pandas as pd

person = {}
race = []
diabetese = {"249", "250", "250.01", "250.1", "250.11", "250.12", "250.13", "250.2", "250.21", "250.22", "250.23",
             "250.3", "250.31", "250.32", "250.33", "250.4", "250.41", "250.42", "250.43", "250.5", "250.51", "250.52",
             "250.53", "250.6", "250.7", "250.8", "250.81", "250.82", "250.83", "250.9", "250.91", "250.92", "250.93"}

diabeteseType1 = {"250.01", "250.11", "250.13", "250.21", "250.23", "250.31", "250.33", "250.41", "250.43", "250.51",
                  "250.53", "250.81", "250.83", "250.91", "250.93"}

diabeteseType2 = {"249", "250", "250.1", "250.12", "250.2", "250.22", "250.3", "250.32", "250.4", "250.42", "250.5",
                  "250.52", "250.6", "250.7", "250.8", "250.82", "250.9", "250.92"}


# This class is used to clean the data.
class Cleaning:

    def __init__(self):
        self.dropped = 0
        with open("data.csv", "r") as f:
            self.data = pd.read_csv(f)

    def setDiabeteseTwo(self):
        print("Gather Diabetese Two data")
        self.data["Type2"] = False
        for i, row in self.data.iterrows():
            self.data.at[i, "Type2"] = ((row["diag_1"] in diabeteseType2) or (row["diag_2"] in diabeteseType2) or (
                    row["diag_3"] in diabeteseType2))

    def setDiabeteseOne(self):
        print("Gather Diabetese One data")
        self.data["Type1"] = False
        for i, row in self.data.iterrows():
            self.data.at[i, "Type1"] = ((row["diag_1"] in diabeteseType1) or (row["diag_2"] in diabeteseType1) or (
                    row["diag_3"] in diabeteseType1))

    def setDiabetesBool(self):
        print("Set Diabetese")
        self.data["Diabetes"] = False
        for i, row in self.data.iterrows():
            self.data.at[i, "Diabetes"] = ((row["diag_1"] in diabetese) or (row["diag_2"] in diabetese) or (
                    row["diag_3"] in diabetese))

    def removeDiagnose(self):
        print("Remove Diagnose field")
        self.data.drop('diag_1', axis=1, inplace=True)
        self.data.drop('diag_2', axis=1, inplace=True)
        self.data.drop('diag_3', axis=1, inplace=True)

    def dropIfNoDiabetes(self):
        print("Drop unintressting cases")
        prev = ""
        ok = False
        count = 0
        todrop = []
        okish = set()
        for i, row in self.data.iterrows():
            if row["Diabetes"]:
                okish.add(row["patient_nbr"])
        for i, row in self.data.iterrows():
            if not (row["patient_nbr"] in okish):
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} unintressting cases".format(count))
        self.dropped += count

    def repairKeyWord(self, keyword):
        pass

    def removeAllEmpty(self):
        pass

    def removeAdmissionType_6_8(self):
        print("Drop unknown Admission Type")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["admission_type_id"] == 6 or row["admission_type_id"] == 8:
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} unknown admission".format(count))
        self.dropped += count

    def discharge_disposition_id_18_25_26(self):
        pass

    def repair_speciality(self):
        self.data.drop('diag_1', axis=1, inplace=True)

    def removeUnknownSex(self):
        print("Drop unknown sex")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["gender"] != "Femal" or row["gender"] != "Male":
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} unknown sex".format(count))
        self.dropped += count

    def remove_examide(self):
        self.data.drop('examide', axis=1, inplace=True)

    def remove_citoglipton(self):
        self.data.drop('citoglipton', axis=1, inplace=True)

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
        self.sort()
        self.repairKeyWord("weight")
        self.repairKeyWord("race")
        self.repairKeyWord("payer_code")
        self.print_format()

    def sort(self):
        self.data.sort_values(by=["patient_nbr", "encounter_id"], ignore_index=True, ascending=True, inplace=True)
        print(self.data)
        with open("final.csv", "w", newline='') as f:
            self.data.to_csv(f, index=False)

    def countQ(self):
        for y in range(1, 9):
            q = dict()
            for i, row in self.data.iterrows():
                if row["admission_type_id"] == y:
                    if not row["medical_specialty"] in q:
                        q[row["medical_specialty"]] = 0
                    q[row["medical_specialty"]] += 1
            print(q)

    def dataAvailable(self):
        print(len(self.data))


c = Cleaning()
c.setDiabeteseOne()
c.setDiabeteseTwo()
c.setDiabetesBool()
c.removeDiagnose()
c.dataAvailable()
c.dropIfNoDiabetes()
c.dataAvailable()
c.countQ()
