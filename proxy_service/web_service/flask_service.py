from flask import Flask, jsonify
from proxy_service.manager.proxy_manager import ProxyManager
from proxy_service.util.crawl_decorator import my_log

app = Flask(__name__)
service_info = {
    'get': 'Get a valid proxy',
    'get_all': 'Get all valid proxies.',
    'refresh': 'Refresh proxy pool.'
}


@app.route('/', methods=['GET'])
def get_service_list():
    print('index in')
    return jsonify(service_info)


@app.route('/get/', methods=['GET'])
def get_proxy():
    print('get in')
    return ProxyManager().get_proxy()


@app.route('/get_all/', methods=['GET'])
def get_all_proxies():
    proxy_list = ProxyManager().get_all_proxies()
    if proxy_list == None:
        proxy_list = []
    return jsonify(data=proxy_list)


@app.route('/refresh/')
def refresh_proxy_pool():
    ProxyManager().check_proxies()
    return 'Refresh proxy pool'

if __name__ == '__main__':
    app.run()
