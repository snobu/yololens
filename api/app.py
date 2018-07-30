#!/usr/bin/env python3

import os
import falcon
from images import Resource
from cosmos import History

api = application = falcon.API()

images = Resource(None)
cosmos = History()

api.add_route('/api/images', images)
api.add_route('/api/cosmos', cosmos)
