import boto3
import falcon
import falcon.testing
import moto
import pytest


FORM_MIMETYPE = 'multipart/form-data; boundary=boundary1337'
FORM_FILE_CONTENT = b'PeregrineFalcon\n' * 64 * 1024
FORM = (
    b'--boundary1337\r\n'
    b'Content-Disposition: form-data; name="myfile"; filename="bytes"\r\n'
    b'Content-Type: application/x-falcon\r\n\r\n' +
    FORM_FILE_CONTENT +
    b'\r\n'
    b'--boundary1337--\r\n'
)


class CloudUpload:

    def on_post(self, req, resp):
        s3 = boto3.client('s3')

        for part in req.media:
            if part.name == 'myfile':
                s3.upload_fileobj(part.stream, 'mybucket', 'mykey')

        resp.location = '/files/mybucket/mykey'
        resp.status = falcon.HTTP_CREATED


@pytest.fixture
def api_client():
    handlers = falcon.media.Handlers({
        falcon.MEDIA_JSON: falcon.media.JSONHandler(),
        falcon.MEDIA_MULTIPART: falcon.media.MultipartFormHandler(),
    })
    api = falcon.App()
    api.req_options.media_handlers = handlers
    api.add_route('/uploads', CloudUpload())

    return falcon.testing.TestClient(api)


@moto.mock_s3
def test_upload_to_mock_s3(api_client):
    conn = boto3.resource('s3', region_name='eu-north-1')
    conn.create_bucket(Bucket='mybucket')

    resp = api_client.simulate_post(
        '/uploads', headers={'Content-Type': FORM_MIMETYPE}, body=FORM)
    assert resp.status_code == 201

    s3_obj = conn.Object('mybucket', 'mykey')
    Body = s3_obj.get()['Body']
    assert Body.read() == FORM_FILE_CONTENT
