import io
import os
import uuid
import mimetypes
import json
import falcon
from urllib import request
import detector
import codecs
import sys
from debug import YoloDebug

DEBUG = YoloDebug.DEBUG


class Resource(object):

    _CHUNK_SIZE_BYTES = 4096

    # The resource object must now be initialized with a path used during POST
    def __init__(self, storage_path):
        self._upload_path = '../frontend/uploads'
        self._results_path = '../frontend/results'

    def on_post(self, req, resp):
        session_id = uuid.uuid4()
        ext = mimetypes.guess_extension(req.content_type, strict=True)
        name = '{session_id}{ext}'.format(session_id=session_id, ext=ext)
        image_path = os.path.join(self._upload_path, name)

        if req.content_type == 'application/json':
            # Fetch URL
            reader = codecs.getreader('utf-8')
            body = json.load(reader(req.stream))
            # assuming jpg but we should detect the right thing
            # from the content-type coming back from urllib
            image_path = os.path.join(
                self._upload_path, str(session_id) + '.jpg')
            try:
                with io.open(image_path, 'wb') as image_file:
                    image_file.write(request.urlopen(body['url']).read())
            except Exception as e:
                print(e, flush=True)
                resp.status = falcon.HTTP_400
                resp.body = '"error" : "{message}"'.format(message=e)

        else:
            # Because Python's mimetypes insists on being silly
            if ext == '.jpe':
                ext = '.jpg'
            if DEBUG: print('\n[DEBUG] Guessed extension with mimetypes module: ' + ext, flush=True)
            if ext not in ['.jpg', '.jpeg', '.png']:
                resp.status = falcon.HTTP_400  # Bad Request
                resp.body = '{ "error" : "Bad MIME type. Try another image." }'

            with io.open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                    if not chunk:
                        break

                    image_file.write(chunk)

        if DEBUG: print('[DEBUG] Running image through darknet...', flush=True)
        if DEBUG: print('[DEBUG] image_path =', str(image_path), flush=True)
        if DEBUG: print('[DEBUG] results/' + str(session_id) + '.jpg', flush=True)
        results = detector.detect(bytes(image_path, 'ascii'),
                                  self._results_path + '/{session_id}'.format(session_id=session_id))

        resp.status = falcon.HTTP_200
        resp.location = '/results/' + str(session_id) + '.jpg'
        if DEBUG:
            print('[DEBUG] Results are in:', flush=True)
            print(results, flush=True)
        resp.body = results
