import pandas as pandas
from openpyxl import load_workbook
from datetime import datetime

from ..forms import BoilerplateForm
from ..model import *
from ..utils import *
from flask import Flask, flash, redirect, url_for, render_template, Blueprint, request
from flask_login import login_required, current_user
from io import BytesIO

import io
import os
import time
import datetime

'''
Setup Redis connection for adding to the queue
'''

import redis
from rq import Queue

redis_conn = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT')
)

queue = os.getenv('REDIS_QUEUE')

redis_queue = Queue(queue, connection=redis_conn)

boilerform_blueprint = Blueprint("boilerform", __name__, template_folder="templates", static_folder='static', static_url_path='/boilerplate/static')
@boilerform_blueprint.route("/create_form", methods=["GET", "POST"])
#@login_required
def create_form():

    form = BoilerplateForm()

    if form.is_submitted():
        
        payload = {
            'statement': request.form.get('statement')
        }

        '''
        Send payload to your redis queue

        Arguements:
        1. script.function (i.e. boiler_worker.run_job) you want to run
        2. the payload (i.e. payload) you want to send to the worker
        '''

        job = redis_queue.enqueue('boiler_worker.run_job', payload)
        job_id = job.get_id()

        print(f'### YOUR JOB ID: {job_id}', flush=True)

        print(f"### payload {payload}", flush=True)
        return render_template('submitted.html')

    return render_template('boilerform.html', form=form)