import os
import random
import string

import pytest
from drope import cmdline


@pytest.fixture
def random_path(tmpdir):
    inner = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
    return os.path.join(tmpdir, inner)


def test_create_dir(random_path):
    assert not os.path.exists(random_path)
    cmdline.create_and_change_dir(random_path)
    assert os.getcwd() == random_path


def test_create_existing_dir(random_path):
    os.makedirs(random_path)
    assert os.path.exists(random_path)
    cmdline.create_and_change_dir(random_path)
    assert os.getcwd() == random_path
