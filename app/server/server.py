###############################################################################
#                                MAIN                                         #
###############################################################################

import logging
import flask

from instance import config
from model.data import data

#import sys
#sys.path.append(config.dirpath)
#import os
#os.chdir(config.dirpath)


'''
'''
def app(name=None, host="127.0.0.1", port="5000", threaded=False, debug=False):
    ## app object
    name = name if name is not None else __name__
    app = flask.Flask(name, instance_relative_config=True, template_folder='../templates')
        
        
    ## config   
    app.config.from_pyfile("instance.config.py", silent=True)
    
    
    ## api
    @app.route('/ping', methods=["GET"])
    def ping():
        return 'pong'
    
    @app.route("/", methods=["GET"])
    def index():
        #return flask.send_from_directory(directory=config.dirpath+"app/templates/", filename="index.html")
        return flask.render_template("index.html")
    
    @app.route("/data", methods=["GET"])
    def get_data():
        ### input dal client
        symbol = flask.request.args["symbol"]
        from_str = flask.request.args["from"]
        to_str = flask.request.args["to"]
        variable = flask.request.args["variable"]
        ### get data
        stock = data(symbol, from_str, to_str, variable)
        stock.get_dates()
        stock.get_data()
        img = stock.plot_ts(plot_ma=True, plot_intervals=True, window=30, figsize=(20,13))
        return flask.send_file(img, attachment_filename='plot.png', mimetype='image/png')
    
    
    ## errors
    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template("errors.html"), 404
    
    
    ## start server
    try:
        logging.info('Starting API server, listen IP ' + host + ' on port ' + str(port) + ' threaded = ' + str(threaded))
        app.run(host=host, port=port, threaded=threaded, debug=debug)
    except(Exception):
        logging.critical('Failure starting API Server')