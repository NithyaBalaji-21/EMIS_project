import pandas as pd

filter_patient = {
    "entry": {
        "$arrayElemAt": [
            {
                "$filter": {
                    "input": "$entry",
                    "cond": {"$eq": ["$$this.request.url", "Patient"]}
                }
            }
            , 0
        ]
    }
}
user_profile_query = {
    "entry.resource.name": 1,
    "entry.resource.telecom": 1,
    "entry.resource.address": 1,
    "entry.resource.gender": 1,
    "entry.resource.birthDate": 1,
    "entry.resource.maritalStatus": 1,
}
filter_diagnosticReport_encounter = {
    "$addFields": {
        "entry": {
            "$filter": {
                "input": "$entry",
                "cond": {"$or": [
                    {"$eq": ["$$this.request.url", "DiagnosticReport"]},
                    {"$eq": ["$$this.request.url", "Encounter"]}
                ]
                }
            }
        }
    }
}
filter_patient_claiming = {
    "$addFields": {
        "entry": {
            "$filter": {
                "input": "$entry",
                "cond": {"$or": [
                    {"$eq": ["$$this.request.url", "Claim"]},
                    {"$eq": ["$$this.request.url", "Encounter"]}
                ]
                }
            }
        }
    }
}

claim_total_avg = {
    "$project": {
        "Total": {"$sum": "$entry.resource.total.value"},
        "Average": {"$avg": "$entry.resource.total.value"},
    }
}
count_by_gender = {
    "$group": {
        "_id": "$entry.resource.gender",
        "Count": {"$sum": 1},
    }
}


def get_patient_details(patient_sam):
    prof_col_names = ["Name", "Family_name", "Prefix", "DOB", "DOD", "Gender", "Address", "City",
                      "State", "Country", "PostalCode", "Marital_Status", "Telecom"]

    final = pd.DataFrame(columns=prof_col_names)
    temp = []

    for i in patient_sam:
        ext = i.get('entry')
        if ext.get('resource'):
            resource = ext.get('resource')
            patient_new_df = pd.DataFrame(columns=prof_col_names)

            if resource.get('address') is not None:
                add = resource.get('address')[0]
                patient_new_df.Address = add.get('line')
                patient_new_df.City = add.get('city')
                patient_new_df.State = add.get('state')
                patient_new_df.Country = add.get('country')
                patient_new_df.PostalCode = add.get('postalCode')
            if resource.get('name') is not None:
                j = resource.get('name')[0]
                patient_new_df.Name = j.get('given')[0]
                patient_new_df.Family_name = j.get('family')
                patient_new_df.Prefix = j.get('prefix')
                patient_new_df.DOB = resource.get('birthDate')
                patient_new_df.DOD = resource.get('deceasedDateTime')
                patient_new_df.Marital_Status = resource.get('maritalStatus').get('coding')[0].get('display')
                patient_new_df.Gender = resource.get('gender')
                patient_new_df.Telecom = str(resource.get('telecom')[0].get('value'))

                temp.append(patient_new_df)

    for df in temp:
        final = final.append(df, ignore_index=True)

    return final


def find_user(name, last_name, collection_patient):
    query_name = {
        'entry.resource.name.given': {'$eq': name},
        'entry.resource.name.family': {'$eq': last_name}, }

    patient_sam = collection_patient.aggregate([
        {
            "$match": query_name
        },
        {
            "$addFields": filter_patient
        },
        {
            "$project": user_profile_query
        },
    ])
    details = get_patient_details(patient_sam)
    return details


def get_all_user_by_city(city, collection_patient):
    query_country = {
        'entry.resource.address.0.city': {'$eq': city}
    }

    multiple_patient_sam = collection_patient.aggregate([
        {
            "$match": query_country
        },
        {
            "$addFields": filter_patient
        },
        {
            "$project": user_profile_query
        },
    ])
    return get_patient_details(multiple_patient_sam)


def get_user_diagnostic_report_imp(patient_sam):
    prof_col_names = ["Name", "Issue_Date", "Performer", "Effective_from", "Status", "Category_Notes",
                      "Service_provider"]

    final = pd.DataFrame(columns=prof_col_names)
    temp = []

    for i in patient_sam:
        for ext in i.get('entry'):
            if ext.get('resource'):
                resource = ext.get('resource')
                patient_new_df = pd.DataFrame([[]])
                if resource.get('resourceType') == "Encounter":
                    name = resource.get("subject").get("display")
                    ser_pro = resource.get("serviceProvider").get("display")
                if resource.get('resourceType') == "DiagnosticReport":
                    patient_new_df["Issue_Date"] = resource.get('issued')[0:10]
                    patient_new_df["Performer"] = resource.get('performer')[0].get("display")
                    patient_new_df["Effective_from"] = resource.get('effectiveDateTime')[0:10]
                    patient_new_df["Status"] = resource.get('status')
                    patient_new_df["Category_Notes"] = str(resource.get('category')[0].get('coding')[0].get("display"))
                    temp.append(patient_new_df)
                if name is not None and ser_pro is not None:
                    patient_new_df["Name"] = name
                    patient_new_df["Service_provider"] = ser_pro

    for df in temp:
        final = final.append(df, ignore_index=True)

    return final


def get_user_diagnostic_report(name, last_name, collection_patient):
    query_name = {
        "$match": {
            'entry.resource.name.given': {'$eq': name},
            'entry.resource.name.family': {'$eq': last_name},
        }
    }
    patient_sam = collection_patient.aggregate([
        query_name,
        filter_diagnosticReport_encounter,
    ])

    report = get_user_diagnostic_report_imp(patient_sam)
    return report


# GET USER'S CLAIM AMOUNT
def get_user_claim_report(name, last_name, collection_patient):
    query_name = {
        "$match": {
            'entry.resource.name.given': {'$eq': name},
            'entry.resource.name.family': {'$eq': last_name},
        }
    }

    patient_sam = collection_patient.aggregate([
        query_name,
        filter_patient_claiming,
    ])
    agg_report = collection_patient.aggregate([
        query_name,
        filter_patient_claiming,
        claim_total_avg,
    ])
    agg_details = list(agg_report)[0]
    report = get_user_claim_report_imp(patient_sam)
    return report, agg_details


def get_user_claim_report_imp(patient_sam):
    prof_col_names = ["Name", "Billable_period", "Priority", "Insurance", "Total", "Currency"]

    final = pd.DataFrame(columns=prof_col_names)
    temp = []
    for i in patient_sam:
        for ext in i.get('entry'):
            if ext.get('resource'):

                resource = ext.get('resource')
                patient_new_df = pd.DataFrame([[]])
                if resource.get('resourceType') == "Encounter":
                    name = resource.get("subject").get("display")

                if resource.get('resourceType') == "Claim":
                    patient_new_df["Billable_period"] = resource.get("billablePeriod").get('start')[
                                                        0:10] + " to " + resource.get("billablePeriod").get('end')[0:10]
                    patient_new_df["Priority"] = resource.get("priority").get("coding")[0].get('code')
                    patient_new_df["Insurance"] = resource.get("insurance")[0].get("coverage").get('display')
                    patient_new_df["Total"] = resource.get("total").get("value")
                    patient_new_df["Currency"] = resource.get("total").get("currency")
                    patient_new_df["Name"] = name

                    temp.append(patient_new_df)

    for df in temp:
        final = final.append(df, ignore_index=True)

    return final


def count_based_on_gender(collection_patient):
    gender_group = collection_patient.aggregate([
        count_by_gender,
    ])
    agg_details = list(gender_group)
    temp = []
    for i in agg_details:
        df = dict()
        df["Gender"] = i.get('_id')[0]
        df["Count"] = i.get('Count')
        temp.append(df)

    final = pd.DataFrame(columns=["Gender", "Count"])
    for i in temp:
        final = final.append(i, ignore_index=True)
    return final


def count_based_on_city(collection_patient):
    city_group = collection_patient.aggregate([
        {
            "$group": {
                "_id": "$entry.resource.address.city",
                "Count": {"$sum": 1},
            }
        }
    ])

    agg_details = list(city_group)

    temp = []
    for i in agg_details:
        df = dict()
        city = i.get('_id')[0]
        df["City"] = city[0]
        df["Count"] = int(i.get('Count'))
        temp.append(df)
    temp.sort(key=lambda x: x['Count'], reverse=True)

    final = pd.DataFrame(columns=["City", "Count"])
    for i in temp:
        final = final.append(i, ignore_index=True)
    return final
