import glob
import libRL
import shutil
import datetime
from os import path, remove, mkdir, rmdir
from flask import Flask, render_template, request, send_from_directory
from numpy.random import randint
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'go on then, keep your secrets'

here = path.abspath(path.dirname(__file__))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')


@app.route('/reflection_loss', methods=['GET','POST'])
def reflection_loss():

    form = dict(request.form)

    quick_graph = False

    if len(form.keys()) > 1:       
        save_loc = prep_tmp('rl')

        if 'graph' in form.keys():
            quick_graph = save_loc
        else:
            quick_graph = False

        input_file = request.files['input']

        res = libRL.reflection_loss(
            data=input_file,
            f_set = string_fmt(form['frequency']),
            d_set = string_fmt(form['thickness']),
            interp=form['interp'],
            multicolumn=True,
            as_dataframe=True,
            quick_graph=quick_graph
        )

        name = path.splitext(input_file.filename)[0]

        res.to_csv(path.join(save_loc, name+'.csv'))
        zipUp('rl')

        return resultant()

    return render_template('reflection_loss.html')

@app.route('/characterization', methods=['GET','POST'])
def characterization():
    
    form = dict(request.form)

    if len(form.keys()) > 1:

        save_loc = prep_tmp('char')

        input_file = request.files['input']

        res = libRL.characterization(
            data=input_file,
            f_set = string_fmt(form['frequency']),
            params='all',
            as_dataframe=True,
        )

        name = path.splitext(input_file.filename)[0]

        res.to_csv(path.join(save_loc, name+'.csv'))

        zipUp('char')

        return resultant()

    return render_template('characterization.html')

@app.route('/effective_bandwidth', methods=['GET','POST'])
def effective_bandwidth():

    form = dict(request.form)

    quick_graph = False

    if len(form.keys()) > 1:
        save_loc = prep_tmp('band')

        if 'graph' in form.keys():
            quick_graph = save_loc
        else:
            quick_graph = False

        try:
            thrs = float(form['thrs'])
        except:
            thrs = -10

        input_file = request.files['input']

        res = libRL.band_analysis(
            data=input_file,
            f_set = string_fmt(form['frequency']),
            d_set = string_fmt(form['thickness']),
            m_set = string_fmt(form['bands']),
            thrs = thrs,
            as_dataframe=True,
            quick_graph = quick_graph
        )

        name = path.splitext(input_file.filename)[0]
 
        res.to_csv(path.join(save_loc, name+'.csv'))
        zipUp('band')

        return resultant()

    return render_template('effective_bandwidth.html')

def string_fmt(string):
    remove = ['(',')']
    for char in remove:
        string=string.replace(char,'')
    string=string.split(',')
    return tuple([float(x) for x in string])

def prep_tmp(item):

    save_loc = path.join(here, 'tmp', item)

    try:
        mkdir(save_loc)
    except: pass

    try:
        tmp_files = glob.glob(path.join(here, 'tmp', item, '**'))
        for file_to_remove in tmp_files:
            remove(file_to_remove)
    except: pass

    return save_loc

def zipUp(temp_file):

    shutil.make_archive(
        path.join(here, 'tmp', 'results'),
        'zip', 
        path.join(here, 'tmp', temp_file)
    )

    print(
        '\nsaving .zip file at ' 
        + str(path.join(here, 'tmp', 'results.zip'))
        +'\n'
    )

def resultant():
    return send_from_directory(
        path.join(here, 'tmp'), 
        'results.zip',
        as_attachment=True
    )

def run_app(port):
    app.run(host='localhost', port=port)

# if __name__ == "__main__":
#     run_app(5000)