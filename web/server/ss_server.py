from flask import Flask
from flask import request
import base64
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!";



@app.route('/saveg', methods=['GET', 'POST'])
def saveg():
	if request.method == 'POST':
		#store graph
		savegraph(request.form['name'], request.form['graph_json'])


@app.route("/upload", methods=['GET', 'POST'])
def saveScreenShot():
	if request.method == 'POST':
		save(request.form['name'], request.form['dataBase64'])
		return "Saved"
	else:
		return "Error"

def savegraph(name, graph_json):
	f = open('./crossing_pics/' + name, 'w')
	f.write(graph_json)
	f.close()

def save(name, data):
	f = open('./' + name, 'w')
	sp = data.split('image/png;base64,')
	decoded_data = base64.b64decode(sp[1])
	f.write(decoded_data)
	f.close()

if __name__=="__main__":
	app.run()