# Movie Reviews
A python flask web app for writing movie reviews to be deployed to Google Cloud App Engine. Uses GCloud machine learning libraries for added functionality. 

## Requirements
The basics of deploying to the App Engine can be found [here](https://cloud.google.com/python/docs/). 

requirements.txt contains required Python libraries. 
Install using `pip3 install -r requirements.txt` 

Config.py must be updated with your GCloud Project ID and a name for the [storage bucket](https://cloud.google.com/storage/docs/creating-buckets) audio files are to be saved in.

Must enable the following GCloud APIs: Speech-to-Text, Translate, Datastore.

