# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sets up logging."""

import logging

from turbinia import config


def setup():
  """Set up logging parameters.

  This will also set the root logger, which is the default logger when a named
  logger is not specified.  We currently use 'turbinia' as the named logger,
  however some external modules that are called by Turbinia can use the root
  logger, so we want to be able to optionally configure that as well.
  """
  # TODO(aarontp): Add a config option to set the log level
  config.LoadConfig()
  logger = logging.getLogger('turbinia')
  # Eliminate double logging from root logger
  logger.propagate = False
  need_file_handler = True
  need_stream_handler = True

  # We only need a handler if one of that type doesn't exist already
  if logger.handlers:
    for handler in logger.handlers:
      # Want to do strict type-checking here because is instance will include
      # subclasses and so won't distinguish between StreamHandlers and
      # FileHandlers.
      # pylint: disable=unidiomatic-typecheck
      if type(handler) == logging.FileHandler:
        need_file_handler = False

      # pylint: disable=unidiomatic-typecheck
      if type(handler) == logging.StreamHandler:
        need_stream_handler = False

  file_handler = logging.FileHandler(config.LOG_FILE)
  formatter = logging.Formatter(u'%(asctime)s:%(levelname)s:%(message)s')
  file_handler.setFormatter(formatter)
  file_handler.setLevel(logging.DEBUG)
  if need_file_handler:
    logger.addHandler(file_handler)

  console_handler = logging.StreamHandler()
  formatter = logging.Formatter(u'[%(levelname)s] %(message)s')
  console_handler.setFormatter(formatter)
  if need_stream_handler:
    logger.addHandler(console_handler)

  # Configure the root logger to use exactly our handlers because other modules
  # like PSQ use this, and we want to see log messages from it when executing
  # from CLI.
  root_log = logging.getLogger()
  for handler in root_log.handlers:
    root_log.removeHandler(handler)
  root_log.addHandler(console_handler)
  root_log.addHandler(file_handler)
