import io
import os

import pytest

from falcon.media.multipart import MultipartForm, MultipartParseOptions
from falcon.util.streams import BufferedStream

try:
    from falcon.cyutil.streams import BufferedStream as CyBufferedStream
except ImportError:
    CyBufferedStream = None


PARSE_OPTIONS = MultipartParseOptions()

FORM1_BOUNDARY = b'BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx'
FORM1_GIB_SIZE = int(os.environ.get('TEST_FORM_GIB_SIZE', '5'))
FORM1 = (
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="file"; filename="bytes"\r\n'
    b'Content-Type: application/x-falcon\r\n\r\n' +
    b'123456789abcdef\n' * 64 * 1024 * 1024 * FORM1_GIB_SIZE +
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="empty"\r\n'
    b'Content-Type: text/plain\r\n\r\n'
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx--\r\n'
)

STREAM1 = io.BytesIO(FORM1)


def stream_factory(stream_type, bsize, stream, length):
    if stream_type == 'cythonized' and CyBufferedStream is None:
        pytest.skip('cythonized BufferedStream is unavailable')

    stream.seek(0)
    cls = BufferedStream if stream_type == 'stream' else CyBufferedStream
    return cls(stream.read, length, bsize)


@pytest.fixture
def form1():
    def _factory(stream_type, bsize):
        stream = stream_factory(stream_type, bsize, STREAM1, len(FORM1))
        return MultipartForm(stream, FORM1_BOUNDARY, len(FORM1), PARSE_OPTIONS)

    return _factory


@pytest.fixture
def expected_size1():
    return FORM1_GIB_SIZE * 1024 ** 3
