"""Central place for package metadata.

The MIT License (MIT)
Copyright (c) 2017 Charles Y. Lin, Domen Blenkuš, Barbara Jenko, Rachel Hirsch
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# NOTE: We use __title__ instead of simply __name__ since the latter would
#       interfere with a global variable __name__ denoting object's name.
__title__ = 'resdk_bcm'
__summary__ = 'BCM Plugin for Resolwe SDK for Python'
__url__ = 'https://github.com/linlabcode/resolwe-bio-py-bcm'

# Semantic versioning is used. For more information see:
# https://packaging.python.org/en/latest/distributing/#semantic-versioning-preferred
__version__ = '1.0.0'

__author__ = ''
__email__ = ''

__license__ = 'MIT'
__copyright__ = '2017, ' + __author__

__all__ = (
    "__title__", "__summary__", "__url__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
)
