# -*- coding: utf-8 -*-

"""Plom tools for producing papers"""

__copyright__ = "Copyright (C) 2020 Andrew Rechnitzer and Colin B. Macdonald"
__credits__ = "The Plom Project Developers"
__license__ = "AGPL-3.0-or-later"
# SPDX-License-Identifier: AGPL-3.0-or-later

paperdir = "papersToPrint"
from .buildNamedPDF import buildAllPapers, confirmProcessed, confirmNamed
from .buildClasslist import processClasslist
