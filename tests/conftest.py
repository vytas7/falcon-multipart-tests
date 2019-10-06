import io

import pytest

from falcon.cyutil.streams import BufferedStream as CyBufferedStream
from falcon.util.streams import BufferedStream
from falcon.media.multipart import MultipartForm, MultipartParseOptions


PARSE_OPTIONS = MultipartParseOptions()

FORM1_BOUNDARY = b'BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx'
FORM1_GIB_COUNT = 5
FORM1 = (
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="file"; filename="bytes"\r\n'
    b'Content-Type: application/x-falcon\r\n\r\n' +
    b'123456789abcdef\n' * 64 * 1024 * 1024 * FORM1_GIB_COUNT +
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="empty"\r\n'
    b'Content-Type: text/plain\r\n\r\n'
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx--\r\n'
)

STREAM1 = io.BytesIO(FORM1)


def stream_factory(stream_type, bsize, stream, length):
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
    return FORM1_GIB_COUNT * 1024 ** 3