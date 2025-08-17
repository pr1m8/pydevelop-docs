Guides
======

Comprehensive guides for using PyDevelop-Docs effectively.

.. toctree::
   :maxdepth: 2
   :caption: Available Guides:

   SCREENSHOT_TESTING_GUIDE

Screenshot Testing Guide
------------------------

The :doc:`SCREENSHOT_TESTING_GUIDE` provides comprehensive coverage of:

* Setting up visual testing for documentation
* Running automated screenshot tests  
* Analyzing results with feedback loops
* Implementing fixes based on visual issues
* Creating continuous testing workflows

Key Features
~~~~~~~~~~~~

* **Automated Testing**: Build, serve, and test documentation automatically
* **Issue Detection**: Find missing navigation, CSS problems, and theme issues
* **Feedback Loop**: Get actionable suggestions for fixing problems
* **Continuous Monitoring**: Watch files and test on changes
* **Visual Regression**: Compare before/after screenshots

Quick Start
~~~~~~~~~~~

.. code-block:: bash

   # Run one-time visual test
   poetry run python scripts/visual_test_runner.py

   # Watch for changes and test continuously  
   poetry run python scripts/watch_and_test.py

The visual testing tools help ensure your documentation looks professional and works correctly across all themes and platforms.