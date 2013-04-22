import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(3, os.path.join(os.path.dirname(__file__), "..", ".."))

from IndexTest import IndexTest
unittest.TextTestRunner().run(IndexTest())
