import libRL
import multiprocessing
from os import path
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from wtforms import(
    StringField, SubmitField, 
    BooleanField, RadioField, 
    FloatField
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'go on then, keep your secrets'


class TextForms(FlaskForm):
    file_input = FileField(
        'File Input :', 
        validators=[FileRequired()]
    )
    
    frequency = StringField(
        'Frequency :', 
        validators=[DataRequired()],
        render_kw={"placeholder": "(start, stop, [step])"}
    )

    thickness = StringField('Thickness :', 
        validators=[DataRequired()],
        render_kw={"placeholder": "(start, stop, [step])"}    
    )

    save_location = StringField('Save Location :', 
        render_kw={"placeholder": r"~\Desktop"}
    )

    submit = SubmitField('Start')


class ReflectionLossForm(TextForms):

    multi = BooleanField('Multiprocessing: ')
    graph = BooleanField('Graph: ')

    interp = RadioField(
        'Interpolation Method:',
        choices=[('cspline','CSpline'),('linear','Linear')],
        default='cspline'
    )

    override = RadioField(
        'Override:',
        choices=[('','None'),('chi Zero','Chi Zero'),('eps set','Eps Set')],
        default=''
    )


class CharacterizationForm(TextForms):

    multi = BooleanField('Multiprocessing: ')
    graph = BooleanField('Graph: ')

    interp = RadioField(
        'Interpolation Method:',
        choices=[('cspline','CSpline'),('linear','Linear')],
        default='cspline'
    )

    override = RadioField(
        'Override:',
        choices=[('','None'),('chi zero','Chi Zero'),('eps set','Eps Set')],
        default=''
    )
    

class BandwidthForm(TextForms):
    thrs = FloatField(
        'Threshold :',
        render_kw={"placeholder": "-10"}
    )

    bands = StringField(
        'Bands :', 
        validators=[DataRequired()],
        render_kw={"placeholder": "(start, stop, [step])"}    
    )

    graph = BooleanField('Graph: ')

    interp = RadioField(
        'Interpolation Method:',
        choices=[('cspline','CSpline'),('linear','Linear')],
        default='cspline'
    )

    override = RadioField(
        'Override:',
        choices=[('','None'),('chi zero','Chi Zero'),('eps set','Eps Set')],
        default=''
    )


@app.route('/', methods=['GET', 'POST'])
def index():  
    return render_template('index.html')


@app.route('/reflection_loss', methods=['GET','POST'])
def reflection_loss_page():

    form = ReflectionLossForm()
    
    if form.is_submitted():

        if form.save_location.data == '':
            quick_save = path.expanduser(r"~\Desktop")
        else:
            quick_save = form.save_location.data

        if form.graph.data is True:
            quick_graph = path.expanduser(r"~\Desktop")
        else:
            quick_graph = form.save_location.data

        libRL.reflection_loss(
            data=form.file_input.data,
            f_set=string_fmt(form.frequency.data),
            d_set=string_fmt(form.thickness.data),
            interp=form.interp.data,
            multiprocessing=form.multi.data,
            override=form.override.data,
            quick_save=quick_save,
            quick_graph=quick_graph
        )

    return render_template('reflection_loss.html', form=form)

@app.route('/characterization', methods=['GET', 'POST'])
def characterization_page():
    
    form = CharacterizationForm()

    if form.is_submitted():

        if form.save_location.data == '':
            quick_save = path.expanduser(r"~\Desktop")
        else:
            quick_save = form.save_location.data

        libRL.characterization(
            data=form.file_input.data,
            f_set=string_fmt(form.frequency.data),
            interp=form.interp.data,
            multiprocessing=form.multi.data,
            override=form.override.data,
            quick_save=quick_save
        )        

    return render_template('characterization.html', form=form)

@app.route('/bandwidth', methods=['GET', 'POST'])
def bandwidth_page():
    form = BandwidthForm()

    if form.is_submitted():

        if form.save_location.data == '':
            quick_save = path.expanduser(r"~\Desktop")
        else:
            quick_save = form.save_location.data

        if form.graph.data is True:
            quick_graph = path.expanduser(r"~\Desktop")
        else:
            quick_graph = form.save_location.data

        if isinstance(form.thrs.data, type(None)) is True:
            thrs = -10
        else:
            thrs = form.thrs.data

        libRL.band_analysis(
            data=form.file_input.data,
            f_set=string_fmt(form.frequency.data),
            d_set=string_fmt(form.thickness.data),
            m_set=string_fmt(form.bands.data),
            thrs=thrs,
            interp=form.interp.data,
            override=form.override.data,
            quick_save=quick_save,
            quick_graph=quick_graph
        )

    return render_template('bandwidth.html', form=form)

def string_fmt(string):
    remove = ['(',')']
    for char in remove:
        string=string.replace(char,'')
    string=string.split(',')
    return tuple([float(x) for x in string])

def run_app(port):
    app.run(host='localhost', port=port)