from flask import Flask, jsonify
app = Flask(__name__)

service_info = {
    'get': 'Get a valid proxy',
    'get_all': 'Get all valid proxies.',
}

@app.route('/index')
def get_service_list():
    return jsonify(service_info)


if __name__=='__main':
    app.run()