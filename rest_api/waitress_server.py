from waitress import serve

from rest_api import app

# serve(app, host='0.0.0.0', port=8080, backlog=2048, recv_bytes=8192*2, inbuf_overflow=524288*2)
serve(app, host='0.0.0.0', port=8080)
