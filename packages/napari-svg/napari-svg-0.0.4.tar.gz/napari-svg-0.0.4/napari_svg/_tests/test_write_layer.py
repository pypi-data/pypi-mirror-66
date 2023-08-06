import os
import numpy as np
import pytest
from napari_svg import napari_write_image, napari_write_points
from napari.layers import Image, Points


@pytest.fixture(params=['image', 'points'])
def layer_writer_and_data(request):
    if request.param == 'image':
        data = np.random.rand(20, 20)
        layer = Image(data)
        writer = napari_write_image
    elif request.param == 'points':
        data = np.random.rand(20, 2)
        layer = Points(data)
        writer = napari_write_points
    else:
        return None, None
    
    layer_data = layer.as_layer_data_tuple()
    return writer, layer_data


def test_write_layer_no_metadata(tmpdir, layer_writer_and_data):
    """Test writing layer data with no metadata."""
    writer, layer_data = layer_writer_and_data
    path = os.path.join(tmpdir, 'layer_file.svg')
    
    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    assert writer(path, layer_data[0], {})

    # Check file now exists
    assert os.path.isfile(path)


def test_write_image_from_napari_layer_data(tmpdir, layer_writer_and_data):
    """Test writing layer data from napari layer_data tuple."""
    writer, layer_data = layer_writer_and_data
    path = os.path.join(tmpdir, 'layer_file.svg')

    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    assert writer(path, layer_data[0], layer_data[1])

    # Check file now exists
    assert os.path.isfile(path)


def test_write_image_no_extension(tmpdir, layer_writer_and_data):
    """Test writing layer data with no extension."""
    writer, layer_data = layer_writer_and_data
    path = os.path.join(tmpdir, 'layer_file')

    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    assert writer(path, layer_data[0], layer_data[1])

    # Check file now exists with an svg extension
    assert os.path.isfile(path + '.svg')


def test_no_write_image_bad_extension(tmpdir, layer_writer_and_data):
    """Test not writing layer data with a bad extension."""
    writer, layer_data = layer_writer_and_data
    path = os.path.join(tmpdir, 'layer_file.csv')

    # Check file does not exist
    assert not os.path.isfile(path)

    # Check no data is writen
    assert not writer(path, layer_data[0], layer_data[1])

    # Check file still does not exist
    assert not os.path.isfile(path)
