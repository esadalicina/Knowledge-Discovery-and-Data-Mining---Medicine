import pandas as pd

person = {}

diabetese = {"249", "250", "250.01", "250.1", "250.11", "250.12", "250.13", "250.2", "250.21", "250.22", "250.23",
             "250.3", "250.31", "250.32", "250.33", "250.4", "250.41", "250.42", "250.43", "250.5", "250.51", "250.52",
             "250.53", "250.6", "250.7", "250.8", "250.81", "250.82", "250.83", "250.9", "250.91", "250.92", "250.93"}

diabeteseType1 = {"250.01", "250.11", "250.13", "250.21", "250.23", "250.31", "250.33", "250.41", "250.43", "250.51",
                  "250.53", "250.81", "250.83", "250.91", "250.93"}

diabeteseType2 = {"249", "250", "250.1", "250.12", "250.2", "250.22", "250.3", "250.32", "250.4", "250.42", "250.5",
                  "250.52", "250.6", "250.7", "250.8", "250.82", "250.9", "250.92"}


# This class is used to clean the data.
def findWeight(group):
    weight = "?"
    for i in group:
        amt = i["weight"]
        if amt != "?":
            weight = amt
    return weight


def findRace(group):
    weight = "?"
    for i in group:
        amt = i["race"]
        if amt != "?":
            weight = amt
    return weight


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

    def repairKeyWord(self):
        tmpIndex = []
        tmpgroup = []
        lastID = 0
        weigthRepaired = 0
        notWeightRepaired = 0
        raceRepaired = 0
        notRaceRepaired = 0
        for i, row in self.data.iterrows():

            if row["patient_nbr"] != lastID:
                if len(tmpIndex) > 1:
                    weight = findWeight(tmpgroup)
                    race = findRace(tmpgroup)
                    changes = False
                    if weight == "?":
                        notWeightRepaired += len(tmpIndex)
                    else:
                        for tmpI in tmpIndex:
                            self.data.at[tmpI, 'weight'] = weight
                        weigthRepaired += len(tmpIndex)
                    if race == "?":
                        notRaceRepaired += len(tmpIndex)
                    else:
                        for tmpI in tmpIndex:
                            self.data.at[tmpI, "race"] = race
                        raceRepaired += len(tmpIndex)
                else:
                    notRaceRepaired += len(tmpIndex)
                    notWeightRepaired += len(tmpIndex)
                lastID = row["patient_nbr"]
                tmpIndex = []
                tmpgroup = []

            elif len(self.data) - 1 == i:
                if row["patient_nbr"] == lastID:
                    tmpIndex.append(i)
                    tmpgroup.append(row)
                    weight = findWeight(tmpgroup)
                    race = findRace(tmpgroup)
                    if weight == "?":
                        notWeightRepaired += len(tmpIndex)
                    else:
                        for tmpI in tmpIndex:
                            self.data.at[tmpI, 'weight'] = weight
                        weigthRepaired += len(tmpIndex)
                    if race == "?":
                        notRaceRepaired += len(tmpIndex)
                    else:
                        for tmpI in tmpIndex:
                            self.data.at[tmpI, "race"] = race
                        raceRepaired += len(tmpIndex)


                else:
                    notRaceRepaired += len(tmpIndex)
                    notWeightRepaired += len(tmpIndex)
            else:
                tmpIndex.append(i)
                tmpgroup.append(row)
        print("Race repaired {} could not repair {}\n\nWeight repaired {} could not repair {}".format(raceRepaired,
                                                                                                      notRaceRepaired,
                                                                                                      weigthRepaired,
                                                                                                      notWeightRepaired))

    def removeAllEmpty(self):
        print("Drop ? ")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["weight"] == "?" or row["race"] == "?":
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} empty weight and race".format(count))
        self.dropped += count
        print(self.dropped)
        print(len(self.data))

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
        print("Drop discharge disposition id")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["discharge_disposition_id"] == 18 or row["discharge_disposition_id"] == 25 or row[
                "discharge_disposition_id"] == 26:
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} discharge disposition".format(count))
        self.dropped += count

    def repair_speciality(self):
        speciality_repaired = 0
        for i, row in self.data.iterrows():
            if row["age"] == "[0-10)" and row["medical_specialty"] == "?":
                self.data.at[i, "medical_specialty"] = "Pediatrics"
                speciality_repaired += 1
        print("Repaired a total of {} speciality".format(speciality_repaired))

    def removeUnknownSex(self):
        print("Drop unknown sex")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["gender"] != "Female" and row["gender"] != "Male":
                print(row["gender"])
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
        print("Drop admission source")
        count = 0
        todrop = []
        for i, row in self.data.iterrows():
            if row["admission_type_id"] == 9 or row["admission_type_id"] == 20 and row["admission_type_id"] == 21:
                todrop.append(i)
                count += 1
        self.data.drop(todrop, inplace=True)
        print("Dropped {} unknown admission".format(count))
        self.dropped += count

    def print_format(self):
        for col in self.data:
            print("{}:\t{}".format(col, self.data[col].unique()))

    def create_file_of_value(self):
        with open("Cleaned.csv", "w") as f:
            self.data.to_csv(f, index=False,lineterminator='\n')

    def run_cleaning(self):
        self.sort()
        self.removeUnknownSex()
        self.remove_citoglipton()
        self.remove_examide()
        self.remove_payer_code()
        self.remove_encoutner_id()
        self.remove_time_in_hospital()
        self.remove_num_lab_procedures()
        self.setDiabeteseOne()
        self.setDiabeteseTwo()
        self.setDiabetesBool()
        self.dropIfNoDiabetes()
        self.removeDiagnose()
        self.repairKeyWord()
        self.repair_weight()
        self.repair_speciality()
        self.num_procedures()
        self.num_outpatient()
        self.num_emergency()
        self.num_inpatient()
        self.number_diagnoses()
        self.remove_admission_source_id_9_20_21()
        self.discharge_disposition_id_18_25_26()
        self.removeAdmissionType_6_8()
        self.removeAllEmpty()
        self.create_file_of_value()

    def sort(self):
        self.data.sort_values(by=["patient_nbr", "encounter_id"], ignore_index=True, ascending=True, inplace=True)

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

    def remove_payer_code(self):
        self.data.drop('payer_code', axis=1, inplace=True)

    def remove_encoutner_id(self):
        self.data.drop('encounter_id', axis=1, inplace=True)

    def remove_time_in_hospital(self):
        self.data.drop('time_in_hospital', axis=1, inplace=True)

    def remove_num_lab_procedures(self):
        self.data.drop('num_lab_procedures', axis=1, inplace=True)

    def num_outpatient(self):
        self.data.drop('number_outpatient', axis=1, inplace=True)

    def num_procedures(self):
        self.data.drop('num_procedures', axis=1, inplace=True)

    def num_inpatient(self):
        self.data.drop('number_inpatient', axis=1, inplace=True)

    def number_diagnoses(self):
        self.data.drop('number_diagnoses', axis=1, inplace=True)

    def num_emergency(self):
        self.data.drop('number_emergency', axis=1, inplace=True)

    def contradiction(self):
        ignore = False
        prev = True
        amt = 0
        id = 0
        for i, row in self.data.iterrows():
            if row["patient_nbr"] != id:
                id = row["patient_nbr"]
                ignore = False
                prev = row["Diabetes"]
                continue
            if ignore:
                continue
            if prev != row["Diabetes"]:
                amt += 1
                ignore = True
        print("Contradicting persons {} from a total of {}".format(amt, self.data["patient_nbr"].nunique()))

    def repair_weight(self):
        speciality_repaired = 0
        self.data["Weigth_averaged"] = False
        for i, row in self.data.iterrows():
            age = row["age"]
            sex = row["gender"]

            if sex == "Male" and age == "[0-10)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[0-25)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[10-20)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[20-30)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[30-40)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[75-100)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[40-50)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[75-100)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[50-60)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[75-100)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[60-70)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[70-80)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[80-90)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Male" and age == "[90-100)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[0-10)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[0-25)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[10-20)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[25-50)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[20-30)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[30-40)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[40-50)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[50-60)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[60-70)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[70-80)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[80-90)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            elif sex == "Female" and age == "[90-100)":
                self.data.at[i, "Weigth_averaged"] = True
                self.data.at[i, "weight"] = "[50-75)"
                speciality_repaired += 1
            else:
                print("Not found {}  {}".format(sex, age))

            if row["age"] == "[0-10)" and row["medical_specialty"] == "?":
                self.data.at[i, "medical_specialty"] = "Pediatrics"

        print("Averaged a total of {} Weigths".format(speciality_repaired))



c = Cleaning()
c.run_cleaning()
c.contradiction()
