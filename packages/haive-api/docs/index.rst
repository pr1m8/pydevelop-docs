==========
Haive API
==========

.. meta::
   :description: REST API framework and tools for the Haive ecosystem
   :keywords: haive, api, rest, web, server, endpoints, middleware

Welcome to Haive API documentation! This package provides a comprehensive
REST API framework that integrates ML models and data processing capabilities
into web services.

.. note::
   Haive API is built on FastAPI and provides production-ready features
   including authentication, rate limiting, and comprehensive middleware support.

Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install haive-api

Basic Usage
-----------

.. code-block:: python

   from haive.api import APIServer
   from haive.core import DataProcessor
   from haive.ml import MLPipeline, MLModel, ModelType

   # Create server with data processor
   processor = DataProcessor()
   server = APIServer(data_processor=processor)

   # Add a simple endpoint
   def health_check():
       return {"status": "healthy", "service": "haive-api"}
   
   server.add_endpoint("/health", health_check)

   # Add ML endpoint
   model = MLModel(id="api-model", model_type=ModelType.CLASSIFIER)
   pipeline = MLPipeline(processor, model)
   server.add_ml_endpoint("/predict", pipeline)

   # Start server
   server.run()

Core Components
===============

API Server
----------

The :class:`~haive.api.APIServer` class provides the main server functionality:

.. autoclass:: haive.api.APIServer
   :members:
   :show-inheritance:

Endpoints
---------

Haive API provides specialized endpoint classes for different use cases:

ML Endpoint
~~~~~~~~~~~

.. autoclass:: haive.api.MLEndpoint
   :members:
   :show-inheritance:

Data Endpoint
~~~~~~~~~~~~~

.. autoclass:: haive.api.DataEndpoint
   :members:
   :show-inheritance:

Batch Endpoint
~~~~~~~~~~~~~~

.. autoclass:: haive.api.BatchEndpoint
   :members:
   :show-inheritance:

Middleware
----------

The middleware system provides cross-cutting concerns:

Base Middleware
~~~~~~~~~~~~~~~

.. autoclass:: haive.api.BaseMiddleware
   :members:
   :show-inheritance:

Authentication Middleware
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: haive.api.AuthMiddleware
   :members:
   :show-inheritance:

Logging Middleware
~~~~~~~~~~~~~~~~~~

.. autoclass:: haive.api.LoggingMiddleware
   :members:
   :show-inheritance:

Rate Limiting Middleware
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: haive.api.RateLimitMiddleware
   :members:
   :show-inheritance:

Configuration
=============

Server Configuration
--------------------

.. autoclass:: haive.api.ServerConfig
   :members:
   :show-inheritance:

Request Context
---------------

.. autoclass:: haive.api.RequestContext
   :members:
   :show-inheritance:

Advanced Usage
==============

Custom Middleware
-----------------

Create custom middleware by extending :class:`~haive.api.BaseMiddleware`:

.. code-block:: python

   from haive.api import BaseMiddleware, RequestContext
   from typing import Dict, Any

   class CustomMiddleware(BaseMiddleware):
       def process_request(self, context: RequestContext, data: Dict[str, Any]) -> Dict[str, Any]:
           # Add custom request processing
           print(f"Processing request {context.request_id}")
           return data
       
       def process_response(self, context: RequestContext, response: Dict[str, Any]) -> Dict[str, Any]:
           # Add custom response processing
           response["custom_header"] = "haive-api"
           return response

   # Add to server
   server.add_middleware(CustomMiddleware())

Batch Processing
----------------

Handle multiple operations in a single request:

.. code-block:: python

   from haive.api import BatchEndpoint

   # Create batch endpoint
   batch_endpoint = BatchEndpoint(
       ml_pipeline=pipeline,
       data_processor=processor
   )
   
   server.add_endpoint("/batch", batch_endpoint.handle_request, methods=["POST"])

   # Example request:
   request_data = {
       "operations": [
           {"type": "predict", "data": {"feature1": 1.0}},
           {"type": "process", "data": {"key": "value"}},
           {"type": "predict", "data": {"feature1": 2.0}}
       ]
   }

API Examples
============

ML Prediction Endpoint
-----------------------

.. code-block:: python

   # Setup
   server.add_ml_endpoint("/predict", ml_pipeline)

   # Request
   POST /predict
   {
       "samples": [
           {"feature1": 1.0, "feature2": 2.0},
           {"feature1": 3.0, "feature2": 4.0}
       ]
   }

   # Response
   {
       "success": true,
       "predictions": [1, 0],
       "confidence": [0.95, 0.87],
       "model_version": "0.1.0",
       "metadata": {
           "endpoint": "ml",
           "request_id": 1,
           "samples_count": 2
       }
   }

Data Processing Endpoint
------------------------

.. code-block:: python

   # Setup
   server.add_data_endpoint("/process", data_processor)

   # Request
   POST /process
   {
       "data": {"key": "value", "number": 42}
   }

   # Response
   {
       "success": true,
       "processed_data": {"key": "VALUE", "number": 42},
       "metadata": {
           "endpoint": "data",
           "request_id": 1,
           "processor_stats": {"processed_count": 1}
       }
   }

Production Deployment
====================

Security Configuration
----------------------

.. code-block:: python

   from haive.api import APIServer, AuthMiddleware, RateLimitMiddleware

   # Create server with security middleware
   server = APIServer()
   
   # Add authentication
   auth_middleware = AuthMiddleware(
       api_key="your-secret-key",
       require_auth=True
   )
   server.add_middleware(auth_middleware)
   
   # Add rate limiting
   rate_limiter = RateLimitMiddleware(
       requests_per_minute=100,
       window_size=60
   )
   server.add_middleware(rate_limiter)

Monitoring and Logging
----------------------

.. code-block:: python

   from haive.api import LoggingMiddleware

   # Add comprehensive logging
   logging_middleware = LoggingMiddleware(
       log_level="info",
       include_data=False  # Don't log sensitive data in production
   )
   server.add_middleware(logging_middleware)

Examples and Tutorials
======================

.. toctree::
   :maxdepth: 2
   
   examples/basic_server
   examples/ml_integration
   examples/middleware
   examples/batch_processing
   tutorials/getting_started
   tutorials/production_deployment
   tutorials/security_best_practices

API Reference
=============

.. toctree::
   :maxdepth: 3
   
   api/haive.api

Integration Guide
=================

Haive API seamlessly integrates with other Haive packages:

**Integration with Haive Core:**

- Uses :class:`haive.core.DataProcessor` for request/response processing
- Built on :class:`haive.core.BaseModel` architecture
- Leverages :class:`haive.core.ConfigManager` for server configuration

**Integration with Haive ML:**

- :class:`haive.api.MLEndpoint` directly integrates :class:`haive.ml.MLPipeline`
- Automatic model versioning and metadata tracking
- Built-in support for batch predictions

.. code-block:: python

   # Complete integration example
   from haive.core import DataProcessor, ConfigManager
   from haive.ml import MLModel, MLPipeline, ModelType
   from haive.api import APIServer, AuthMiddleware

   # Initialize components
   config_manager = ConfigManager()
   processor = DataProcessor()
   model = MLModel(id="integrated-model", model_type=ModelType.CLASSIFIER)
   pipeline = MLPipeline(processor, model)

   # Create API server
   server = APIServer(data_processor=processor)
   server.add_middleware(AuthMiddleware(api_key=config_manager.get("API_KEY")))
   server.add_ml_endpoint("/predict", pipeline)
   server.add_data_endpoint("/process")

   # Start server
   server.run()

.. seealso::
   
   - :doc:`haive-core:index` - Core data structures and utilities  
   - :doc:`haive-ml:index` - Machine Learning components

HTTP API Reference
==================

Authentication
--------------

All endpoints support Bearer token authentication:

.. http:method:: POST /predict
   :reqheader Authorization: Bearer <api_key>

Endpoints
---------

.. http:get:: /

   Root endpoint providing API information.

.. http:get:: /health

   Health check endpoint.

.. http:get:: /stats

   Server statistics endpoint.

.. http:post:: /predict

   ML prediction endpoint.

   **Request:**

   .. code-block:: json

      {
          "samples": [
              {"feature1": 1.0, "feature2": 2.0}
          ]
      }

   **Response:**

   .. code-block:: json

      {
          "success": true,
          "predictions": [1],
          "confidence": [0.95]
      }

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