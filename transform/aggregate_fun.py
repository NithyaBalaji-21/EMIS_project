# Filter only Patient details
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

# Filter only DiagnosticReport and encounter details
filter_diagnosticReport_encounter = {
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

# Filter only DiagnosticReport
filter_diagnosticReport = {
    "entry": {
        "$arrayElemAt": [
            {
                "$filter": {
                    "input": "$entry",
                    "cond": {"$eq": ["$$this.request.url", "DiagnosticReport"]}
                }
            }
            , 0
        ]
    }
}

# Filter Claim details
filter_patient_claiming = {
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
user_profile_query = {
    "entry.resource.name": 1,
    "entry.resource.telecom": 1,
    "entry.resource.address": 1,
    "entry.resource.gender": 1,
    "entry.resource.birthDate": 1,
    "entry.resource.maritalStatus": 1,
}

diagnostic_report_query = {
    "entry.resource.resourceType": 1,
    "entry.resource.name.given": 1,
    "entry.resource.name.family": 1,
    "entry.resource.status": 1,
    "entry.resource.category": 1,
    "entry.resource.effectiveDateTime": 1,
    "entry.resource.performer": 1,
    "entry.resource.issued": 1,
    "entry.resource.encounter": 1,
    "entry.resource.subject": 1,
    "entry.resource.serviceProvider": 1,
}
