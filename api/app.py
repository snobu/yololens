#!/usr/bin/env python3

import os
import falcon
from images import Resource

api = application = falcon.API()

images = Resource(None)
api.add_route('/api/images', images)
