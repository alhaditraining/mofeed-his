"""Delegate hooks to the packaged app module.

The app folder contains a nested module (`mofeed_his.mofeed_his`), so we
reuse its hook definitions to keep configuration in one place.
"""

# pylint: disable=wildcard-import
from mofeed_his.mofeed_his.hooks import *  # noqa: F401,F403
