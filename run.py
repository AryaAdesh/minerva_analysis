import sys
import os
from waitress import serve
import logging, sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

from minerva_analysis import app

if __name__ == '__main__':
    # use port 8000 if no port is specified via command line argument
    port = 8000 if len(sys.argv) < 2 or not str.isdigit(sys.argv[1]) else sys.argv[1]


    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")


    if len(sys.argv) > 2 and str2bool(sys.argv[2]):
        is_docker = True
    else:
        is_docker = False
    app.config['IS_DOCKER'] = is_docker

    app.config['MC_MICRO'] = os.environ.get("MC_MICRO", "false").lower() == "true"
    if app.config['MC_MICRO']:
        app.config['REG_PATH'] = os.environ.get("REG_PATH", "")
        app.config['CSV_PATH'] = os.environ.get("CSV_PATH", "")
        app.config['ORIGINAL_DIR'] = os.environ.get("ORIGINAL_DIR", "")

    print('Serving on 0.0.0.0:' + str(port) + ' or http://localhost:' + str(port))
    serve(app, host='0.0.0.0', port=port, max_request_body_size=1073741824000000,
          max_request_header_size=85899345920000)
