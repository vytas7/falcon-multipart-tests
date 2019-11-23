import functools
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
FORM1_MIB_SIZE = int(os.environ.get('TEST_FORM_MIB_SIZE', '5120'))
FORM1 = (
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="file"; filename="bytes"\r\n'
    b'Content-Type: application/x-falcon\r\n\r\n' +
    b'123456789abcdef\n' * 64 * 1024 * FORM1_MIB_SIZE +
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx\r\n'
    b'Content-Disposition: form-data; name="empty"\r\n'
    b'Content-Type: text/plain\r\n\r\n'
    b'\r\n'
    b'--BOUNDARYxxxxxxxxxxxxxxxxxxxxxxx--\r\n'
)

STREAM1 = io.BytesIO(FORM1)


@functools.lru_cache(maxsize=65536)
def _part_factory(index):
    base_offset, exponent = divmod(index, 1000)
    return str((1337 + base_offset) ** (exponent + 1)).rstrip('L').encode()


PARSE_OPTIONS_MANY_PARTS = MultipartParseOptions()
PARSE_OPTIONS_MANY_PARTS.max_body_part_count = 1024 * 1024

FORM2_BOUNDARY = b'boundary--many-parts--'
FORM2_PART_COUNT = 65536

_part_template = (
    'Content-Disposition: form-data; name="part{}"\r\n'
    'Content-Type: application/x-falcon-peregrine\r\n\r\n'
)
FORM2 = (
    b'--boundary--many-parts--\r\n' +
    b''.join(
        (
            _part_template.format(index).encode() +
            _part_factory(index) +
            b'\r\n--boundary--many-parts--\r\n'
        )
        for index in range(FORM2_PART_COUNT)
    ) +
    b'Content-Disposition: form-data; name="empty"\r\n'
    b'Content-Type: text/plain\r\n\r\n'
    b'\r\n'
    b'--boundary--many-parts----\r\n'
)

STREAM2 = io.BytesIO(FORM2)


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
    return FORM1_MIB_SIZE * 1024 ** 2


@pytest.fixture
def form2():
    def _factory(stream_type, bsize):
        stream = stream_factory(stream_type, bsize, STREAM2, len(FORM2))
        return MultipartForm(
            stream, FORM2_BOUNDARY, len(FORM2), PARSE_OPTIONS_MANY_PARTS)

    return _factory


@pytest.fixture
def part_factory2():
    return _part_factory


@pytest.fixture
def expected_parts2():
    return FORM2_PART_COUNT
