Installation Guide
==================

This comprehensive guide covers all installation methods for test-haive-template.

.. contents:: Table of Contents
   :local:
   :depth: 2

System Requirements
-------------------

**Minimum Requirements:**

- **Python**: 3.8 or higher (3.10+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Package Manager**: pip (included with Python) or poetry

**Recommended Setup:**

- **Python**: 3.11+ for best performance
- **Virtual Environment**: venv, conda, or poetry
- **Git**: For development and contributing

Quick Install
-------------

For most users, the simplest installation method:

.. tab-set::

    .. tab-item:: pip

        .. code-block:: bash

            pip install test-haive-template

    .. tab-item:: poetry

        .. code-block:: bash

            poetry add test-haive-template

    .. tab-item:: conda

        .. code-block:: bash

            # If available on conda-forge
            conda install -c conda-forge test-haive-template


Virtual Environment Setup
--------------------------

**Using venv (Recommended for beginners):**

.. code-block:: bash

   # Create virtual environment
   python -m venv .venv
   
   # Activate (Linux/macOS)
   source .venv/bin/activate
   
   # Activate (Windows)
   .venv\Scripts\activate
   
   # Install package
   pip install test-haive-template

**Using poetry (Recommended for projects):**

.. code-block:: bash

   # Initialize new project
   poetry init
   
   # Add dependency
   poetry add test-haive-template
   
   # Install and activate shell
   poetry install
   poetry shell

**Using conda:**

.. code-block:: bash

   # Create environment
   conda create -n test_haive_template python=3.11
   
   # Activate environment
   conda activate test_haive_template
   
   # Install package
   pip install test-haive-template

Development Installation
------------------------

For contributing or customizing test-haive-template:

.. code-block:: bash

   # Clone repository
   git clone https://github.com/your-org/test-haive-template.git
   cd test-haive-template
   
   # Install in development mode
   pip install -e .
   
   # Or with poetry
   poetry install
   
   # Install development dependencies
   pip install -e ".[dev]"  # or poetry install --with dev


Platform-Specific Notes
------------------------

**Windows:**

.. code-block:: batch

   # Use PowerShell or Command Prompt
   python -m pip install test-haive-template
   
   # If you get permission errors
   python -m pip install --user test-haive-template

**macOS:**

.. code-block:: bash

   # If using Homebrew Python
   /opt/homebrew/bin/python3 -m pip install test-haive-template
   
   # System Python (not recommended)
   python3 -m pip install --user test-haive-template

**Linux:**

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt update && sudo apt install python3-pip
   python3 -m pip install test-haive-template
   
   # CentOS/RHEL/Fedora
   sudo dnf install python3-pip
   python3 -m pip install test-haive-template

Verify Installation
-------------------

After installation, verify everything is working:

**Check version:**

.. code-block:: bash

   python -c "import test_haive_template; print(test_haive_template.__version__)"

**Test basic functionality:**

.. code-block:: python

   import test_haive_template
   
   # Basic test
   print("test-haive-template imported successfully!")
   
   # Check available functions/classes
   print(dir(test_haive_template))

Troubleshooting
---------------

**Common Issues:**

.. tab-set::

    .. tab-item:: Permission Errors

        .. code-block:: bash

            # Use --user flag
            pip install --user test-haive-template
            
            # Or use virtual environment (recommended)
            python -m venv .venv && source .venv/bin/activate

    .. tab-item:: Import Errors

        .. code-block:: bash

            # Check installation location
            python -c "import test_haive_template; print(test_haive_template.__file__)"
            
            # Reinstall if needed
            pip uninstall test-haive-template && pip install test-haive-template

    .. tab-item:: Version Conflicts

        .. code-block:: bash

            # Check for conflicts
            pip check
            
            # Upgrade pip first
            python -m pip install --upgrade pip
            
            # Force reinstall
            pip install --force-reinstall test-haive-template


**Getting Help:**

If you're still having issues:

1. Check the `FAQ <https://github.com/your-org/test-haive-template/wiki/FAQ>`_
2. Search `existing issues <https://github.com/your-org/test-haive-template/issues>`_
3. Create a `new issue <https://github.com/your-org/test-haive-template/issues/new>`_ with:
   - Your operating system
   - Python version (``python --version``)
   - Complete error message
   - Installation method used

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   # With pip
   pip install --upgrade test-haive-template
   
   # With poetry
   poetry update test-haive-template
   
   # Check new version
   test_haive_template --version

Next Steps
----------

Now that test-haive-template is installed:

- 🚀 **Quick Start**: :doc:`quickstart` - Get up and running in 5 minutes
- ⚙️ **Configuration**: :doc:`configuration` - Customize your setup
- 📚 **Tutorials**: :doc:`../tutorials/first_steps` - Detailed walkthrough
- 💡 **Examples**: :doc:`../examples/index` - See real-world usage

.. tip::
   **New to test-haive-template?** Start with the :doc:`quickstart` guide for a hands-on introduction!