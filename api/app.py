#!/usr/bin/env python3

import os
import falcon
import mimetypes
from images import Resource

from pathlib import Path
current_path = str(Path().absolute())

api = application = falcon.API()

frontend_path = os.path.dirname(os.path.abspath('../frontend')) + '/frontend'
results_path = os.path.dirname(os.path.abspath('../frontend/results')) + '/results'

images = Resource(None)
api.add_route('/images', images)
api.add_static_route('/', frontend_path, downloadable=False,
        fallback_filename='index.html')
api.add_static_route('/results', results_path, downloadable=False)
