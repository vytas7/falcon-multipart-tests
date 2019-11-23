import pytest


@pytest.mark.parametrize('stream_type,bsize', [
    ('stream', 4096),
    ('stream', 1024 * 16),
    ('stream', 1024 * 128),
    ('cythonized', 4096),
    ('cythonized', 1024 * 16),
    ('cythonized', 1024 * 128),
])
def test_many_parts(stream_type, bsize, form2, part_factory2, expected_parts2):
    for index, part in enumerate(form2(stream_type, bsize)):
        if part.content_type == 'application/x-falcon-peregrine':
            assert part.stream.read() == part_factory2(index)
