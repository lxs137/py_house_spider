from flask import Flask, jsonify
from proxy_service.manager.proxy_manager import ProxyManager
app = Flask(__name__)
service_info = {
    'get': 'Get a valid proxy',
    'get_all': 'Get all valid proxies.',
}


@app.route('/index')
def get_service_list():
    return jsonify(service_info)


@app.route('/get')
def get_proxy():
    return ProxyManager().get_proxy()


@app.route('/get_all')
def get_all_proxies():
    return ProxyManager().get_all_proxies()


@app.route('/refresh')
def refresh_proxy_pool():
    ProxyManager().check_proxies()
    return 'Refresh proxy pool'

if __name__ == '__main':
    app.run()