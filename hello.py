from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    if client:
        data = {'name':user}
        db.create_document(data)
        return 'Hi %s! I added you to the database.' % user
    else:
        print('No database')
        
        return '''
<div style="border: 2px gray solid; background-color: #ddd;">
<h1>You have searched for Nike Reax 8 TR 42.5:</h1>
<a href="https://www.mall.cz/obuv/nike-reax-8-tr-425"><img src="https://www.mall.cz/i/39895704/1000/1000"></a> <br>
</div>

<h2> We think you could like the following products:</h2>

<hr>

<h3>1. Nike AIR PRECISION NBK 41</h3> <br>
<a href="https://www.mall.cz/obuv/nike-air-precision-nbk-41"><img src="https://www.mall.cz/i/39921121/1000/1000"></a> <br>
<hr>

<h3>2. Nike RunAllDay Running Shoe 41</h3> <br>
<a href="https://www.mall.cz/obuv/nike-runallday-running-shoe-41"><img src="https://www.mall.cz/i/39882153/1000/1000"></a> <br>
<hr>

<h3>3. Puma 365 CT Jr Black Safety 28</h3> <br>
<a href="https://www.mall.cz/obuv/puma-365-ct-jr-black-safety-28"><img src="https://www.mall.cz/i/40072330/1000/1000"></a> <br>
<hr>

<h3>4. Mizuno Synchro MD 2 Black/White/Green 41</h3> <br>
<a href="https://www.mall.cz/obuv/mizuno-synchro-md-2-blackwhitegreen-41"><img src="https://www.mall.cz/i/36471888/1000/1000"></a> <br>
<hr>

<h3>5. Puma Enzo Mesh Black White 41</h3> <br>
<a href="https://www.mall.cz/obuv/puma-enzo-mesh-black-white-41"><img src="https://www.mall.cz/i/39966033/1000/1000"></a> <br>
<hr>

<h3>6. New Balance MT620GT 41,5</h3> <br>
<a href="https://www.mall.cz/obuv/newbalance-mt620gt-415"><img src="https://www.mall.cz/i/39881673/1000/1000"></a> <br>
<hr>

<h3>7. Nike Zoom Evidence Basketball Shoe 41</h3> <br>
<a href="https://www.mall.cz/obuv/nike-zoom-evidence-basketball-shoe-41"><img src="https://www.mall.cz/i/39881673/1000/1000"></a> <br>
<hr>

<h3>8. Puma Mega NRGY Knit Black Asphalt 41</h3> <br>
<a href="https://www.mall.cz/obuv/puma-mega-nrgy-knit-black-asphalt-41"><img src="https://www.mall.cz/i/39966211/1000/1000"></a> <br>
<hr>

<img src="http://files.nar.cz/mall-cz.jpg">
<img src="https://www.pagerduty.com/wp-content/uploads/2017/04/logo-bluemix.png">
'''

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
