===========
Haive Core
===========

.. meta::
   :description: Core data structures and utilities for the Haive ecosystem
   :keywords: haive, core, data processing, utilities, base models

Welcome to Haive Core documentation! This package provides the fundamental
building blocks and utilities used throughout the Haive ecosystem.

.. note::
   Haive Core is designed to be lightweight and dependency-free, making it
   easy to integrate into any project that needs robust data handling.

Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install haive-core

Basic Usage
-----------

.. code-block:: python

   from haive.core import DataProcessor, BaseModel

   # Create a data processor
   processor = DataProcessor()
   
   # Process some data
   result = processor.process({"key": "value", "number": 42})
   print(result.status)  # "success"
   print(result.data)    # {"key": "VALUE", "number": 42}

   # Create a base model
   model = BaseModel(id="my-model")
   model.update_metadata("version", "1.0")
   print(model.metadata)  # {"version": "1.0", "created_at": "..."}

Core Components
===============

Data Processing
---------------

The :class:`~haive.core.DataProcessor` class provides robust data processing
capabilities with built-in error handling and validation:

.. autoclass:: haive.core.DataProcessor
   :members:
   :show-inheritance:

Base Models
-----------

The :class:`~haive.core.BaseModel` class serves as the foundation for all
models in the Haive ecosystem:

.. autoclass:: haive.core.BaseModel
   :members:
   :show-inheritance:

Configuration Management
------------------------

The :class:`~haive.core.ConfigManager` handles configuration loading and
validation across the ecosystem:

.. autoclass:: haive.core.ConfigManager
   :members:
   :show-inheritance:

Examples and Tutorials
======================

.. toctree::
   :maxdepth: 2
   
   examples/basic_usage
   examples/advanced_processing
   examples/configuration
   tutorials/getting_started
   tutorials/best_practices

API Reference
=============

.. toctree::
   :maxdepth: 3
   
   api/haive.core

Integration Guide
=================

Haive Core integrates seamlessly with other Haive packages:

- **Haive ML**: Use :class:`~haive.core.BaseModel` as foundation for ML models
- **Haive API**: Process request data with :class:`~haive.core.DataProcessor`

.. seealso::
   
   - :doc:`haive-ml:index` - Machine Learning components
   - :doc:`haive-api:index` - REST API framework

Contributing
============

.. include:: ../CONTRIBUTING.md
   :parser: myst_parser.sphinx_

Changelog
=========

.. include:: ../CHANGELOG.md
   :parser: myst_parser.sphinx_

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex` 
* :ref:`search`