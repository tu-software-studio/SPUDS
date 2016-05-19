# SPUDS

# Installation
1. Clone the repository and cd into it
2. Install virutalenvwrapper `sudo apt-get install virtualenvwrapper`, create a new virtual environment `mkvirtualenv <name>`, and enter it `workon <name>`
3. set the repo as the virtualenvs root `setvirtualenvproject`
4. Install required packages `pip install -r requirements.txt`
5. Create the settings.py file: `cp settings-template.py settings.py`
6. To run the app `python app.py`
7. If you can't figure this out, contact Ben Duggan.


# Information
## Deploy From Github - /deploy/api/github
This feature is still in development.

The Github deployment process is designed to be used with the push event from Github.

It verifies the request is from Github by using the secret provided from Github. It then checks to see if the
person who triggered the event is in the ALLOWED_COMMITTERS list. If they are, it will try to regex the last commit
message to see if a deployment is desired to be triggered. Here is an example of what the regex is looking
for: `deploy(staging, 123451234)`. If it matches, it triggers the deployment process.


## Deploy from HTTP Client - /deploy/api
The HTTP endpoint is probably the easiest process to use. If you download a client like [httpie](https://github.com/jkbrzt/httpie) you can deploy the application with one line in the terminal; eg. `http POST https://staging.tinyhandsdreamsuite.org:5000/deploy/api < api-deploy.json`

The format of the json file is as follows:
```
{
     "environment": "<staging|production>",
     "tag":"<empty|build-number>",
     "secret": "<shared secret>"
}
```
The secret is the method of authentication for this endpoint. If someone knows the secret, they are able to deploy the application. Because of this method, it is really only safe to deploy on an https connection because anyone could intercept the packet with the secret.

## The deployment process
Currently the deployment process consists of checking whether or not the tag for the docker image exists on Dockerhub, and then calling out to a deployment bash script. This script currently just sets the tag version of the dreamsuite and runs it.

## Settings

All configuration settings should be located in the settings.py and the settings-template.py files. The settings-template.py file is a place to share what the settings are with empty values so that we can keep track of the variables used in the application. This also allows us to keep the values empty so that we can keep this open-source without sharing private information. This file needs to be created since it is not in VC. The easiest way to do that is `cp settings-template.py settings.py`.

Just make sure if you add more settings that they end up in the settings-template.py file
