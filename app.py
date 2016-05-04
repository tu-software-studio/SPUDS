import json, re
from subprocess import call

from flask import Flask, request, abort

from dockerhubclient import DockerhubClient

app = Flask(__name__)

ALLOWED_COMMITTERS = ['benaduggan', 'baxterthehacker']
ENV = 'staging'

# @app.route('/deploy/codeship',methods=['POST'])
# def deploy_codeship():
#    """
#    this is specifically for the codeship deployment process
#    It will probably only work for the client for awhile
#
#    The json object should be as follows:
#    {
#         "environment": "<staging|production>",
#         "app":"<client|api>",
#         "tag":"<empty|build-number>"
#    }
#    """
#
#    data = json.loads(request.data)
#    environment = data['environment']
#    app = data['app']
#    tag = data['tag']
#
#    print "Env: {} App: {} Tag: {}".format(environment, app, tag)
#
#    deploy_api(tag)
#
#    return 'OK'

@app.route('/deploy/github',methods=['POST'])
def deploy_commit_message():
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

def deploy_api(tag):
    client = DockerhubClient()
    if client.check_if_tag_exists(tag):
        print "\n\n DEPLOYING APP WITH TAG VERSION: {}\n\n".format(tag)
        rc = call("../tinyhands/run.sh {}".format(tag), shell=True)
    else:
        abort(404)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
