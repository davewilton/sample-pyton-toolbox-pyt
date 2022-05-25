# Sample Python PYT
Just a sample project showing how I like to set up an Esri Python addin and test it.


## Setting up Dev env ###

Steps:
* Launch ``proenv.bat`` (as administrator if desired but non admin preferred)
    - Located in your ``ArcGIS/Pro/bin/Python/Scripts`` folder
    - Gives you a terminal window with the ArcGIS Pro python environment activated
* Clone the environment to a new dev environment
    - ``conda create --name sampleAddin --clone arcgispro-py3``
    - If you opened proenv as administrator this will be put in an envs folder with the arcgis default python.
      Otherwise, it will be put somewhere in your user folder e.g. %localappdata%\esri\conda\envs


Set the interpreter for the PyCharm Project:
* File > settings > Project Interpreter
* Cog Icon > Add
* Virtual Environment > Existing virtual environment
* Locate python.exe most likely
    - C:\Users\%username%\AppData\Local\ESRI\conda\envs\sampleAddin

If your project has library requirements outside of those included with ArcGIS Pro:      
 
* Activate the new environment
    - ``activate sampleAddin``
* Install all requirements
    - ``pip install -r requirements.txt``
* run the tests
    - ``pytest tests/unit ``
    - ``pytest tests/end2end --nomock``
    
## Tests
### unit tests
Unit tests mock out arcpy for speed. Any arcpy objects used must be mocked out either locally in the test
or globally in the arcpy_mock module

### end to end tests
These use arcpy and input data and are therefore much slower.
