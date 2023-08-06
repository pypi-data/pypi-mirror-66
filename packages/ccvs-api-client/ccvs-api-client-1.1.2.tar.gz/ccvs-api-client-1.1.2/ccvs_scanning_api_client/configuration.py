# Copyright 2019 WHG (International) Limited. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class Configuration(object):

    def __init__(self, host):
        host = host if host[-1] == '/' else host + '/'
        self.host = host
