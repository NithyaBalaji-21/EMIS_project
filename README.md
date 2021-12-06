# EMIS_project
 
## The Task
An external system / supplier is sending patient data to our platform using the FHIR standard. Our analytics teams find this format difficult to work with when creating dashboards and visualizations. You are required to tranform these FHIR messages into a more workable format preferably in a tabular format.


## SOLUTION
Collected FHIR messages related to patients from the GitHub repository and stored them in MongoDB. Created aggregation pipelines to process the data and transformed it into easily workable data frames. 

### STEPS:
1) Get all json file names from Github link https://github.com/emisgroup/exa-data-eng-assessment/ data directory.
2) Python http requests are sent and response objects are returned as json format.
3) Uploaded all the json objects to MongoDB as documents using PyMongo driver. Deleted existing documents before uploading.
4) Created multiple aggregation piplines to process multiple documents and return computed results.
5) Transfomed the results into pandas dataframe for readability.
6) Repeated steps 3 & 4 for multiple computational scenarios and the results are shown.
7) Containerised the pipeline using docker / docker-compose.




