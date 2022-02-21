from flask_restful import Api
from flask import Flask
import logging
import sys

from scrap_post import scrap_post
from scrap_thread import scrap_thread
from scrap_page import scrap_page
from scrap_board import scrap_board

app = Flask(__name__)
api = Api(app)
log = logging.getLogger('werkzeug')
log.disabled = True


api.add_resource(scrap_post, "/scrap/post/<string:datatype>/<string:board>/<string:thread_id>/<string:post_id>", resource_class_kwargs={'datapath': sys.argv[3]})
api.add_resource(scrap_thread, "/scrap/thread/<string:datatype>/<string:board>/<string:thread_id>", resource_class_kwargs={'datapath': sys.argv[3]})
api.add_resource(scrap_page, "/scrap/page/<string:datatype>/<string:board>/<string:page_number>", resource_class_kwargs={'host': sys.argv[1], 'port': int(sys.argv[2]), 'datapath': sys.argv[3]})
api.add_resource(scrap_board, "/scrap/board/<string:datatype>/<string:board>", resource_class_kwargs={'host': sys.argv[1], 'port': int(sys.argv[2]), 'datapath': sys.argv[3]})

if __name__ == "__main__":
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=True, threaded=True)
