from pymongo import MongoClient
from get_transform_details import *
from get_data import *


if __name__ == '__main__':
    # Ingest data from GITHub and upload to MongoDB
    client = MongoClient('host.docker.internal', 27017)
    db = client['EMIS']
    collection_patient = db['Patient_data_FHIR']

    # GET details from GIT
    get_data_from_git(collection_patient)

    print("\n=============USER DETAILS=========================================")
    # Get an individual's personal details
    user = find_user("Aaron697", "Dickens475",  collection_patient)
    print(user.to_string())

    print("\n=============USERS FROM SAME CITY==================================")
    # Get all users from a same state
    user_by_city = get_all_user_by_city('Boston', collection_patient)
    print(user_by_city.to_string())
    print(" Total records - ", len(user_by_city))

    print("\n=============DIAGNOSTIC REPORT OF A USER===========================")
    # Get a user's diagnostic report
    user_diag_report = get_user_diagnostic_report("Aaron697", "Dickens475", collection_patient)
    print(user_diag_report[10:16].to_string())
    print(" Total records - ", len(user_diag_report))

    print("\n=============CLAIM DETAILS OF A USER===========================")
    # Get a user's claim details
    user_claim_report, agg_report = get_user_claim_report("Aaron697", "Dickens475", collection_patient)
    print(user_claim_report[10:16].to_string())
    print(" Total records - ", len(user_claim_report))
    print(" Total claim amount - ", round(agg_report.get('Total'), 4))
    print(" Average claim amount - ", round(agg_report.get('Average'), 4))
    # client.close()

    print("\n=============USER ANALYTICS===========================")
    user_group_report = count_based_on_gender(collection_patient)
    print(user_group_report.to_string())
    user_city_report = count_based_on_city(collection_patient)
    print(user_city_report[0:11].to_string())

