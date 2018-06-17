import io
import os
import uuid
import mimetypes
import json
import falcon
from urllib import request
import detector

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
            body = json.load(req.stream)
            # assuming jpg but we should detect the right thing
            # from the content-type coming back from urllib
            try:
                fetch_image_response = request.urlopen(body['url']).read()
                ct = fetch_image_response.info().get_content_type()
                ext = mimetypes.guess_extension(ct, strict=True)
                print("=====")
                print(c)
                print(ext)
                print("=====")
                image_path = os.path.join(self._upload_path, str(session_id) + '.jpg')
                with io.open(image_path, 'wb') as image_file:
                    image_file.write(fetch_image_response.read())
                    
            except Exception as e:
                print(e)
                resp.status = falcon.HTTP_400
                resp.body = '"error" : "{message}"'.format(message=e)
        
        else:
            # Because Python's mimetypes insists on being silly
            if ext == '.jpe': ext = '.jpg'
            print('\n[DEBUG] GUESSED EXTENSION FROM MIME TYPE: ', ext)
            if ext not in ['.jpg', '.jpeg', '.png']:
                resp.status = falcon.HTTP_400 # Bad Request
                resp.body = '{ "error" : "Bad MIME type. Try another image." }'

            with io.open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                    if not chunk:
                        break

                    image_file.write(chunk)

        print('[DEBUG] Running image through darknet...')
        print('--------------------------')
        print('image_path =', str(image_path))
        print('results/' + str(session_id) + '.png')
        print('--------------------------')
        results = detector.detect(bytes(image_path, 'ascii'),
            self._results_path + '/{session_id}'.format(session_id=session_id))

        resp.status = falcon.HTTP_200
        resp.location = '/results/' + str(session_id) + '.png'
        print(results)
        resp.body = results
