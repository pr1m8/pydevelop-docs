==========
Haive ML
==========

.. meta::
   :description: Machine Learning components and pipelines for the Haive ecosystem
   :keywords: haive, machine learning, ml, pipeline, model, training, prediction

Welcome to Haive ML documentation! This package provides comprehensive
machine learning capabilities built on the solid foundation of Haive Core.

.. note::
   Haive ML leverages industry-standard libraries like scikit-learn and NumPy
   while providing a unified interface that integrates seamlessly with the
   broader Haive ecosystem.

Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install haive-ml

Basic Usage
-----------

.. code-block:: python

   from haive.ml import MLModel, MLPipeline, ModelType, ModelTrainer
   from haive.core import DataProcessor

   # Create an ML model
   model = MLModel(
       id="my-classifier",
       model_type=ModelType.CLASSIFIER,
       parameters={"learning_rate": 0.01}
   )

   # Train the model
   X_train = [{"feature1": 1.0, "feature2": 2.0}]
   y_train = [1]
   
   trainer = ModelTrainer()
   result = trainer.train_model(model, X_train, y_train)
   print(f"Training accuracy: {result['final_metrics']['accuracy']}")

   # Create a pipeline
   processor = DataProcessor()
   pipeline = MLPipeline(processor, model)
   
   # Make predictions
   test_data = [{"feature1": 2.0, "feature2": 3.0}]
   predictions = pipeline.predict(test_data)
   print(f"Predictions: {predictions.predictions}")

Core Components
===============

ML Models
---------

The :class:`~haive.ml.MLModel` class provides a unified interface for
machine learning models:

.. autoclass:: haive.ml.MLModel
   :members:
   :show-inheritance:

ML Pipelines
------------

The :class:`~haive.ml.MLPipeline` class orchestrates data processing
and model predictions:

.. autoclass:: haive.ml.MLPipeline
   :members:
   :show-inheritance:

Model Training
--------------

The :class:`~haive.ml.ModelTrainer` class provides advanced training
capabilities including cross-validation:

.. autoclass:: haive.ml.ModelTrainer
   :members:
   :show-inheritance:

Model Types
-----------

.. autoclass:: haive.ml.ModelType
   :members:

Pipeline Results
----------------

.. autoclass:: haive.ml.PipelineResult
   :members:
   :show-inheritance:

Advanced Features
=================

Cross-Validation
-----------------

Haive ML provides comprehensive cross-validation support:

.. code-block:: python

   def model_factory():
       return MLModel(id="cv-model", model_type=ModelType.CLASSIFIER)
   
   cv_results = trainer.cross_validate(
       model_factory=model_factory,
       X=X_train,
       y=y_train,
       cv_folds=5
   )
   
   print(f"Mean accuracy: {cv_results['mean_metrics']['accuracy']}")
   print(f"Std deviation: {cv_results['std_metrics']['accuracy']}")

Model Persistence
-----------------

Models can be easily saved and loaded:

.. code-block:: python

   # Save model
   model.save_model("my_model.json")
   
   # Load model
   loaded_model = MLModel.load_model("my_model.json")

Examples and Tutorials
======================

.. toctree::
   :maxdepth: 2
   
   examples/classification
   examples/regression
   examples/pipelines
   examples/training
   tutorials/getting_started
   tutorials/advanced_training
   tutorials/model_evaluation

API Reference
=============

.. toctree::
   :maxdepth: 3
   
   api/haive.ml

Integration Guide
=================

Haive ML is designed to work seamlessly with other Haive packages:

**Integration with Haive Core:**

- Built on :class:`haive.core.BaseModel` for consistent data management
- Uses :class:`haive.core.DataProcessor` for input preprocessing
- Leverages :class:`haive.core.ConfigManager` for configuration

**Integration with Haive API:**

- ML models can be exposed via REST endpoints using :class:`haive.api.MLEndpoint`
- Pipelines integrate directly with :class:`haive.api.APIServer`

.. code-block:: python

   from haive.api import APIServer
   
   # Create API server with ML endpoint
   server = APIServer()
   server.add_ml_endpoint("/predict", pipeline)
   server.run()

.. seealso::
   
   - :doc:`haive-core:index` - Core data structures and utilities
   - :doc:`haive-api:index` - REST API framework

Mathematical Background
======================

Model Training Process
----------------------

The training process follows standard machine learning principles:

.. math::

   \text{Loss} = \frac{1}{n} \sum_{i=1}^{n} L(y_i, \hat{y}_i)

Where :math:`L` is the loss function, :math:`y_i` are true labels,
and :math:`\hat{y}_i` are predicted labels.

Cross-Validation Metrics
-------------------------

Cross-validation provides robust model evaluation:

.. math::

   \text{CV Score} = \frac{1}{k} \sum_{i=1}^{k} \text{Score}_i

Where :math:`k` is the number of folds and :math:`\text{Score}_i`
is the score for fold :math:`i`.

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