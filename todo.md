# TODO
## Remove 1 len
### removed examide
### removed citoglipton

### removed troglitazone
Steady or No
## Diag 1 2 3
combine these into 1 filed : "Diabetes" if in 1 or 2 or 3 diabete then set field to true. Take them from
## Verify if change
## Remove empty sex
Here the sex can not be repaired and the data are not intressting.

E.G of removed: Here they don't have race,age,weigth. Also unique

encounter_id                      257364294
patient_nbr                        78119847
race                                      ?
gender                      Unknown/Invalid
age                                 [70-80)
weight                                    ?
admission_type_id                         1
discharge_disposition_id                 22
admission_source_id                       7
time_in_hospital                          8
payer_code                               CP
medical_specialty                         ?
num_lab_procedures                       59
num_procedures                            2
num_medications                          21
number_outpatient                         0
number_emergency                          0
number_inpatient                          0
diag_1                                  850
diag_2                                  805
diag_3                                  808
number_diagnoses                          9
max_glu_serum                          None
A1Cresult                              None
metformin                            Steady
repaglinide                              No
nateglinide                              No
chlorpropamide                           No
glimepiride                              No
acetohexamide                            No
glipizide                                No
glyburide                                No
tolbutamide                              No
pioglitazone                             No
rosiglitazone                        Steady
acarbose                                 No
miglitol                                 No
troglitazone                             No
tolazamide                               No
examide                                  No
citoglipton                              No
insulin                                  No
glyburide-metformin                      No
glipizide-metformin                      No
glimepiride-pioglitazone                 No
metformin-rosiglitazone                  No
metformin-pioglitazone                   No
change                                   Ch
diabetesMed                             Yes
readmitted                               NO


### Heavy emergency crash
encounter_id                      226864668
patient_nbr                        60524946
race                                      ?
gender                      Unknown/Invalid
age                                 [60-70)
weight                                    ?
admission_type_id                         1
discharge_disposition_id                  1
admission_source_id                       7
time_in_hospital                          1
payer_code                               CP
medical_specialty                         ?
num_lab_procedures                       38
num_procedures                            1
num_medications                           6
number_outpatient                         0
number_emergency                          0
number_inpatient                          0
diag_1                                  808
diag_2                                  873
diag_3                                 E813
number_diagnoses                          5
max_glu_serum                          None
A1Cresult                              None
metformin                                No
repaglinide                              No
nateglinide                              No
chlorpropamide                           No
glimepiride                              No
acetohexamide                            No
glipizide                                No
glyburide                                No
tolbutamide                              No
pioglitazone                             No
rosiglitazone                            No
acarbose                                 No
miglitol                                 No
troglitazone                             No
tolazamide                               No
examide                                  No
citoglipton                              No
insulin                                  No
glyburide-metformin                      No
glipizide-metformin                      No
glimepiride-pioglitazone                 No
metformin-rosiglitazone                  No
metformin-pioglitazone                   No
change                                   No
diabetesMed                              No
readmitted                               NO

# Repairing of data
## Race
144/2271
##

# Creation of new field
## Diabetes Bool
Based on ICD-10-CM skipped this as all data related to car accident
Based on ICD-9-CM
### Type 1 or Type 2
## Ignored
H40 Glaucoma ==> No H spoted in the possible colums (from database)
E916 Struck accidently by falling object (from codebase)



# TO REMOVE
## encounter_id
## time in hospital
## payer code
## num lab procedures
## num procedures
## num outpatient
## number emergency
## number inpatient
## number diagnoses

## number of times


# Clustering @Filip
# Data anaylze based on the number of admission and on conditions on the dataset.