from minerva_analysis import app, get_config_names
from flask import render_template, send_from_directory
from pathlib import Path
import json
import os


@app.route("/")
def my_index():
    return render_template("index.html", data={'datasource': '', 'datasources': get_config_names(),
                                               'is_docker': app.config['IS_DOCKER']})


@app.route('/<string:datasource>')
def image_viewer(datasource):
    datasources = get_config_names()
    if datasource not in datasources:
        datasource = ''
    return render_template('index.html', data={'datasource': datasource, 'datasources': datasources,
                                               'is_docker': app.config['IS_DOCKER']})



@app.route("/upload_page")
def upload_page():
     # Basic data common to both modes.
    data = {
        'datasource': '',
        'datasources': get_config_names(),
        'is_docker': app.config.get('IS_DOCKER', False)
    }
    # If running in MC_MICRO mode (i.e. automatic pipeline), prepopulate extra values.
    if app.config.get('MC_MICRO'):
        default_output = app.config.get('ORIGINAL_DIR', '')
        dataset_name = Path(default_output).name if default_output else ''
        data.update({
            'mcmicro': True,
            'reg_file': app.config.get('REG_PATH', ''),
            'csv_file': app.config.get('CSV_PATH', ''),
            'mcmicro_output_folder': default_output,
            'dataset_name': dataset_name,
            'auto_update': True  
        })
    return render_template("upload.html", data=data)




@app.route('/client/<path:filename>')
def serveClient(filename):
    return send_from_directory(app.config['CLIENT_PATH'], filename, conditional=True)
