import pytest


@pytest.mark.parametrize('stream_type,bsize', [
    ('stream', 4096),
    ('stream', 8192),
    ('stream', 1024 * 16),
    ('stream', 1024 * 32),
    ('stream', 1024 * 64),
    ('stream', 1024 * 128),
    ('stream', 1024 * 256),
    ('stream', 1024 * 512),
    ('stream', 1024 * 1024),
    ('cythonized', 4096),
    ('cythonized', 8192),
    ('cythonized', 1024 * 16),
    ('cythonized', 1024 * 32),
    ('cythonized', 1024 * 64),
    ('cythonized', 1024 * 128),
    ('cythonized', 1024 * 256),
    ('cythonized', 1024 * 512),
    ('cythonized', 1024 * 1024),
])
def test_part_aligned_read(stream_type, bsize, form1, expected_size1):
    for part in form1(stream_type, bsize):
        if part.name == 'file':
            stream = part.stream
            total = 0
            while True:
                chunk = stream.read(bsize)
                if not chunk:
                    break
                total += len(chunk)

            assert total == expected_size1
