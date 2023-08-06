Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython_azurecustomvision_prediction/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/circuitpython_azurecustomvision_prediction/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/JimBobBennett/CircuitPython_AzureCustomVision_Prediction/workflows/Build%20CI/badge.svg
    :target: https://github.com/JimBobBennett/CircuitPython_AzureCustomVision_Prediction/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython prediction library for the Azure custom vision service.

To use this library, you will need to create a custom vision project at `CustomVision.ai <https://customvision.ai?WT.mc_id=circuitpythonazurecustomvisionprediction-github-jabenn>`_.
Once you have your project, you will need to train either an image classification model, or an object detection model. You can then use this library to make predictions against this model.

You can read more on how to do this in the Microsoft docs:

- `Train an image classifier <https://aka.ms/AA88qph>`_
- `Train an object detection model <https://aka.ms/AA88llc>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit CircuitPython Requests <https://github.com/adafruit/Adafruit_CircuitPython_Requests>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython_azurecustomvision_prediction/>`_. To install for current user:

.. code-block:: shell

    pip3 install circuitpython-azurecustomvision-prediction

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-azurecustomvision-prediction

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-azurecustomvision-prediction

Usage Example
=============

.. code-block:: python

    client = CustomVisionPredictionClient("api_key", "endpoint")

    predictions = client.classify_image_url("project_id", "published_name", "https://www.adafruit.com/includes/templates/shop2019/images/adafruit-logo.png")

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/JimBobBennett/CircuitPython_azurecustomvision_Prediction/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
