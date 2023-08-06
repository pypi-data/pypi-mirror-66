import os
import numpy as np
import pytest
from napari_svg import napari_get_writer
from napari.layers import Image, Points


@pytest.fixture
def layer_data_and_types():
    layers = [
              Image(np.random.rand(20, 20)),
              Image(np.random.rand(20, 20)),
              Points(np.random.rand(20, 2)),
             ]
    layer_data = [l.as_layer_data_tuple() for l in layers]
    layer_types = [ld[2] for ld in layer_data]
    return layer_data, layer_types


def test_get_writer(tmpdir, layer_data_and_types):
    """Test writing layers data."""
    layer_data, layer_types = layer_data_and_types

    path = os.path.join(tmpdir, 'layers_file.svg')

    writer = napari_get_writer(path, layer_types)

    assert writer is not None

    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    assert writer(path, layer_data)

    # Check file now exists
    assert os.path.isfile(path)


def test_get_writer_no_extension(tmpdir, layer_data_and_types):
    """Test writing layers data with no extension."""
    layer_data, layer_types = layer_data_and_types

    path = os.path.join(tmpdir, 'layers_file')

    writer = napari_get_writer(path, layer_types)

    assert writer is not None

    # Check file does not exist
    assert not os.path.isfile(path)

    # Write data
    assert writer(path, layer_data)

    # Check file now exists
    assert os.path.isfile(path + '.svg')


def test_get_writer_bad_extension(tmpdir, layer_data_and_types):
    """Test not writing layers data with bad extension."""
    layer_data, layer_types = layer_data_and_types

    path = os.path.join(tmpdir, 'layers_file.csv')

    writer = napari_get_writer(path, layer_types)

    assert writer is None

    # Check file does not exist
    assert not os.path.isfile(path)


def test_get_writer_bad_layer_types(tmpdir):
    """Test not writing layers data with bad extension."""
    layer_types = ['image', 'points', 'bad_type']

    path = os.path.join(tmpdir, 'layers_file.svg')

    writer = napari_get_writer(path, layer_types)

    assert writer is None

    # Check file does not exist
    assert not os.path.isfile(path)
