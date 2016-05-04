from flask import Flask, request, abort
import json, re


app = Flask(__name__)

ALLOWED_COMMITTERS = ['baxterthehacker']
ENV = 'staging'


@app.route('/deploy/codeship',methods=['POST'])
def deploy_codeship():
   """
   this is specifically for the codeship deployment process
   It will probably only work for the client for awhile

   The json object should be as follows:
   {
        "environment": "<staging|production>",
        "app":"<client|api>",
        "tag":"<empty|build-number>"
   }
   """

   data = json.loads(request.data)
   environment = data['environment']
   app = data['app']
   tag = data['tag']

   print "Env: {} App: {} Tag: {}".format(environment, app, tag)

   deploy_api(tag)

   return 'OK'

@app.route('/deploy/github',methods=['POST'])
def deploy_commit_message():
   data = json.loads(request.data)
   committer = data['head_commit']['committer']['username']
   message = data['head_commit']['message']

   print "New commit by: {}".format(committer)
   print "The commit message: {}".format(message)

   # check = re.match('deploy\((?P<env>staging|production),\s(?P<tag>\d+)\)$', 'deploy(staging, 12312312)')
   check = re.match('deploy\((?P<env>staging|production),\s(?P<tag>\d+)\)$', message)
   if committer in ALLOWED_COMMITTERS:
      print(check.groups())
      if check and check.group('env') == ENV and check.group('tag'):
         deploy_api(check.group('tag'))
         return "OK"
      abort(404)
   else:
      return abort(401)

def deploy_api(tag):
   print "\n\n DEPLOYING APP WITH TAG VERSION: {}\n\n".format(tag)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
