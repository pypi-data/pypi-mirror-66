import os
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process

from prometheus_client import generate_latest, REGISTRY, multiprocess, CollectorRegistry, Counter

from lemmings.utils.influx import Influx

web_requests = Counter(f'web_requests', f'Latency for incoming web requests', ["url"])
class TestServer(BaseHTTPRequestHandler):
    def do_GET(self):
        web_requests.labels(url="/prometheus").inc()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(generate_latest(REGISTRY))

def run_server(server_class=HTTPServer, handler_class=TestServer):
    multiprocess.MultiProcessCollector(REGISTRY)

    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("stop server")



class Prometheus:
    def __init__(self, registry=REGISTRY, shared_dir='./prometheus.tmp'):
        self.path = os.environ.setdefault('prometheus_multiproc_dir', shared_dir)
        shutil.rmtree(self.path, ignore_errors=True)
        os.mkdir(self.path)

        if not registry:
            registry = CollectorRegistry()
        self.registry = registry
        multiprocess.MultiProcessCollector(self.registry)
        self.influx = Influx(self.registry)
        self.args = []

    def filter(self, *args):
        self.args = args

    def dump_to_influx(self, all=False):
        args = self.args if not all else []
        return self.influx.save(*args)

    def clean(self):
        try:
            shutil.rmtree(self.path)
            print("temporary prometheus dir cleared")

            self.prom_server.terminate()
            self.prom_server.join(5)

        except BaseException as e:
            print("problem with temporary prometheus dir: ", e)

    def start_server_process(self):
        self.prom_server = Process(target=run_server, args=())
        self.prom_server.start()

