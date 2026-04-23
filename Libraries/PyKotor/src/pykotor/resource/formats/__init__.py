"""BioWare resource format implementations.

Individual formats are imported as submodules (for example ``from pykotor.resource.formats import gff``).
This package ``__init__`` stays lightweight so core modules such as ``resource.type`` can import
``formats._base`` without loading optional format stacks or third-party parsers.
"""
