import json, re
from subprocess import call, Popen

from flask import Flask, request, abort

from dockerhubclient import DockerhubClient

from settings import *

app = Flask(__name__)

ALLOWED_COMMITTERS = ['benaduggan', 'baxterthehacker']
ENV = 'staging'

@app.route('/deploy/api',methods=['POST'])
def deploy():
   """
   this is for someone who wants to directly deploy onto the server

   The json object should be as follows:
   {
        "environment": "<staging|production>",
        "tag":"<empty|build-number>",
        "secret": "<shared secret>"
   }
   """
   data = json.loads(request.data)
   environment = data['environment']
   tag = data['tag']
   secret = data['secret']

   print "Request to deploy the api"
   print "Env: {} Tag: {}".format(environment, tag)

   if secret == API_SECRET:
      if deploy_api(tag):
         write_tag(tag)
         return 'OK'
      abort(500)
   else:
      abort(401)

@app.route('/deploy/api/github',methods=['POST'])
def deploy_from_github_commit():
    if verify_hmac_hash(request): # If request is really from Github
        data = json.loads(request.data)
        committer = data['head_commit']['committer']['username']
        message = data['head_commit']['message']

        print "New commit by: {}".format(committer)
        print "The commit message: {}".format(message)

        deploy_req = re.search('deploy\((?P<env>staging|production),\s(?P<tag>\d+)\)', message)
        if committer in ALLOWED_COMMITTERS:
          if deploy_req and deploy_req.group('env') == ENV and deploy_req.group('tag'):
             deploy_api(deploy_req.group('tag'))
             return "OK"

          abort(404) # Not able to deploy
        else:
          return abort(401) # committer isn't allowed to deploy


def verify_hmac_hash(request):
    signature = request.headers.get('X-Hub-Signature')
    data = request.data
    secret = bytes(GITHUB_SECRET, 'UTF-8')
    mac = hmac.new(secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)

def write_tag(tag):
    file = open(TAG_PATH,'w')
    file.write(tag)
    file.close()


def deploy_api(tag):
    client = DockerhubClient()
    if client.check_if_tag_exists(tag):
        print "\n\n DEPLOYING APP WITH TAG VERSION: {}\n\n".format(tag)
        cmd = call(DEPLOY_SCRIPT_PATH + " {}".format(tag), shell=True)
        # cmd = Popen(["../tinyhands/deploy.sh", tag])
        return True
    else:
        abort(404)

import ssl
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)

if __name__ == '__main__':
    if ENVIRONMENT == "local":
        app.run(host='0.0.0.0')
    elif ENVIRONMENT == "staging":
        app.run(host='0.0.0.0', ssl_context=context)
