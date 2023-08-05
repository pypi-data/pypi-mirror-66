# -*- coding: utf-8 -*-
#
# Copyright © 2017 Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)

"""Tests for memoryprofiler.py."""

from __future__ import division

# Standard library imports
import os
import sys

# Third party imports
import pytest
from pytestqt import qtbot
from qtpy.QtCore import Qt

from spyder.utils.qthelpers import qapplication
MAIN_APP = qapplication() 

# Local imports
from spyder_memory_profiler.widgets.memoryprofiler import MemoryProfilerWidget

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock  # Python 2


TEST_SCRIPT = \
"""@profile
def foo():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
foo()"""

@pytest.mark.qt_log_level_fail('WARNING')
def test_profile_and_display_results(qtbot, tmpdir, monkeypatch):
    """
    Run profiler on simple script and check that results are okay.

    This is a fairly simple integration test which checks that the plugin works
    on a basic level.
    """
    os.chdir(tmpdir.strpath)
    testfilename = tmpdir.join('test_foo.py').strpath

    with open(testfilename, 'w') as f:
        f.write(TEST_SCRIPT)

    MockQMessageBox = Mock()
    monkeypatch.setattr('spyder_memory_profiler.widgets.memoryprofiler.QMessageBox',
                        MockQMessageBox)

    widget = MemoryProfilerWidget(None)
    qtbot.addWidget(widget)
    with qtbot.waitSignal(widget.sig_finished, timeout=10000, raising=True):
        widget.analyze(testfilename)    

    MockQMessageBox.assert_not_called()
    dt = widget.datatree
    assert dt.topLevelItemCount() == 1  # number of functions profiled
    
    top = dt.topLevelItem(0)                               
    assert top.data(0, Qt.DisplayRole).startswith('foo ')
    assert top.childCount() == 6
    for i in range(6):
        assert top.child(i).data(0, Qt.DisplayRole) == i + 1  # line no

    # Column 2 has increment (in MiB); displayed as 'xxx MiB' so need to strip
    # last 4 characters. To make the test robust, we only check the sign
    assert float(top.child(2).data(2, Qt.DisplayRole)[:-4]) > 0
    assert float(top.child(3).data(2, Qt.DisplayRole)[:-4]) > 0
    # Test in next line is broken because of bug in memory_profiler
    # https://github.com/pythonprofilers/memory_profiler/issues/226
    # assert float(top.child(4).data(2, Qt.DisplayRole)[:-4]) < 0
    assert float(top.child(5).data(2, Qt.DisplayRole)[:-4]) == 0
