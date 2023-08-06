# Developer Information

## General overview

This Jupyter extension contains of two components:

**Jupyter serverextension**

* written in Python
* see [jupyter-openbis-extension/](jupyter-openbis-extension)
* serverextension is registered with the `jupyter serverextension enable --py jupyter-openbis-extension` command
* registration should happen automatically when installilng via `pip install jupyter-openbis-extension`
* this serverextension is loaded whenever a Jupyter server is started – either `jupyter notebook` or `jupyter lab`
* serverextension talks to openBIS instances via the [pyBIS module](https://pypi.org/project/PyBIS/)
* serverextension also talks to the notebook extension (see below) via https
* serverextension uses an instance of the [tornado webserver](https://www.tornadoweb.org/en/stable/) that is used by Jupyter server
* downloads and uploads dataSets and openBIS metadata

**Jupyter notebook extension** (aka Jupyter nbextension)

* written in JavaScript
* see [jupyter-openbis-extension/static](jupyter-openbis-extension/static)
* is registered with the `jupyter nbextension install --py jupyter-openbis-extension --user` and `jupyter nbextension enable --py jupyter-openbis-extension --user` commands
* registration should happen automatically when installilng via `pip install jupyter-openbis-extension`
* nbextension is started whenever a notebook is opened
* a new instance of the nbextension is started for *every* notebook
* displays the three prominent buttons (configuration, download, upload) inside a Jupyter notebook
* talks to the Jupyter serverextension (see above) via https requests

## Jupyter serverextension

sources see [jupyter-openbis-extension/](jupyter-openbis-extension)

[server.py](jupyter-openbis-extension/server.py) dispatches all requests coming from the nbextension. Currently, following endpoints are present:

* GET `/openbis/dataset/(?P<connection_name>.*)?/(?P<permId>.*)?/(?P<downloadPath>.*)` – downloads the files of a dataSet to the disk.
* POST `/openbis/dataset/(?P<connection_name>.*)` – upload of dataSets
* GET `/openbis/datasetTypes/(?P<connection_name>.*)` – receive a list of available dataSet types (including all properties)
* GET `/openbis/sample/(?P<connection_name>.*)?/(?P<identifier>.*)` – receive a list of dataSets for a given sample or experiment identifier (should be *dataSets*, not *sample*)
* GET/POST `/openbis/conns` – receive openBIS connections or create new ones
* PUT `/openbis/conn/(?P<connection_name>.*)` – modifiy an existing openBIS connection

[connection.py](jupyter-openbis-extension/connection.py) – handles the openBIS connections

[dataset.py](jupyter-openbis-extension/dataset.py) – handles the dataSets (down- and upload)

[sample.py](jupyter-openbis-extension/server.py) – returns the list of available dataSets


## Jupyter nbextension

[main.js](jupyter-openbis-extension/static/main.js) – Main entry point for the nbextension. Registers the connectionDialog, downloadDialog, and uploadDialog

[connectionDialog.js](jupyter-openbis-extension/static/connectionDialog.js) – shows the connection dialog

[downloadDialog.js](jupyter-openbis-extension/static/downloadDialog.js) – shows the download dialog

[uploadDialog.js](jupyter-openbis-extension/static/uploadDialog.js) – shows the upload dialog

[state.js](jupyter-openbis-extension/static/state.js) – stores some state information, e.g. current connection, last downloaded dataSet, last entered metadata etc.

[common.js](jupyter-openbis-extension/static/common.js) – commonly used utilities, e.g. create feedback, create error message, get cookie
