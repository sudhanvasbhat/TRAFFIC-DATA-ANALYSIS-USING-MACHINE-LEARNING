## Data Science Project
### Data Dorks

### Front End

[server_code](./server_code.py) file can be used to connect server for local implementation.

### Implementation using Anvil Account

  - Create a blank Anvil project and upload the [TADA.yaml](../TADA.yaml) file.
  - The [Backend_Server_code.ipynb](../Backend_and_Server.ipynb) (present in main) Jupyter Notebook file must be run locally, after updating with a personal server uplink key, to connect the server.
  - Obtaining the server uplink key:
    - In the Anvil project page, go to ``uplink`` -> ``enable server uplink`` and copy the server uplink key.
    - Replace the key in [Backend_Server_code.ipynb](../Backend_and_Server.ipynb) 
    - You might need to install the Anvil Uplink Library: ``pip install anvil-uplink``, if not already present.
  - App can now be run from Anvil

### Key development details

  - Global file contains all colour values, junction names and coordinates
  - Date and time from frontend is sent to the model as input
  - Model returns junction name and colour for all junctions based on input timeframe
  - Native libraries added : added javascript for marker

### Running locally

  - Clone this repository and navigate to the "Frontend" folder.
  - install [Coretto](https://docs.aws.amazon.com/corretto/latest/corretto-21-ug/downloads-list.html) (please install the .msi version)
  - ``pip install anvil-app-server``
  - You might need to also install the Anvil Uplink Library: ``pip install anvil-uplink``, if not already present.
  - In the command window, navigate to the "Frontend" folder, and type ``anvil-app-server --app TADA --uplink-key roadsandmaps_key`` and press enter, to run the server.
  - In another command window, navigate to the "Frontend" folder, and run the server_code file using ``python server_code.py``.
  - Now, open a browser window and navigate to (http://localhost:3030/), the application should appear.
  - Please wait until the model runs and the message "Succesfully connected!" appears on the command window that is running the server_code, before using the Application.

### Known Problems
- When running via anvil account, connecting to Anvil does not work when running the Jupyter Notebook using VisualStudioCode. [Jupyter](https://jupyter.org/install) works.
