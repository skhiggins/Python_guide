# Python Guide

This guide provides instructions for using Python on research projects. Its purpose is to use with collaborators and research assistants to make code consistent, easier to read, transparent, and reproducible.

### Style and Packages 

* For coding style practices, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). 
    - While you read the style guide and do your best to follow it, once you save the script you can use `flake8`, `pycodestyle_magic`, and 
    `pycodestyle`. Run `%load_ext pycodestyle_magic` and `%flake8_on`, and each cell will be checked for styling errors upon running. 
* Use `Pandas` and/or `datatable` for wrangling data. For big data (millions of observations, the efficiency advantages of datatable become important).
* Use `datetime` for working with dates.
* Never use `setwd()` or absolute file paths. Instead use relative file paths with the `pyprojroot` package.
* Use assert frequently to add programmatic sanity checks in the code
* Use `PanelOLS` from `linearmodels` for fixed effects regression. 

### Folder Structure 
Generally, within the folder where we are doing data analysis, we have:
* A root folder for the project
    - If you always open the project from the root folder then the `pyprojroot` package will work for relative filepaths
* data - Only raw data go in this folder
* documentation - documentation about the data go in this folder
* scripts - code goes in this folder
    - Number scripts in the order in which they should be run

### Master file
Keep a script that lists each script that should be run to go from raw data to final results. Under the name of each script should be a brief description of the purpose of the script, as well all the input data sets and output data sets that it uses.

### Graphing
* Use `matplotlib` or `seaborn` for graphing. For graphs with colors, use `cubehelix` for a colorblind friendly palette.
* For reproducible graphs, always specify the `width` and `height` arguments in `savefig`.
* To see what the final graph looks like, open the file that you save since its appearance will differ from what you see in the Jupyter Notebook.
* For high resolution, save graphs with a `dpi=300` or greater value in `savefig`
* For maps, use the `basemap` package from `matplotlib`, (This has to be installed separately.) A helpful tutorial is available [here] (https://basemaptutorial.readthedocs.io/en/latest/index.html)
  
### Randomization

When randomizing assignment in a randomized control trial (RCT):
    * Seed: Use a seed from https://www.random.org/: put Min 1 and Max 100000000, then click Generate, and copy the result into your script. Towards the top of the script, assign the seed with the line `numpy.random.seed(...) # from random.org` where ... is replaced with the number you got from random.org
    * Use the `random` package. Here is a [cheatsheet] (https://pynative.com/python-random-module/) of different randomization functions
    * Build a randomization check: create a second variable a second time with a new name, repeating `numpy.random.seed(seed)` immediately before creating the second variable. Then check that the randomization is identical using `assert(df.var1 == dfvar2)`.
    * It is also good to do a more manual check where you run the full script once, save the resulting data with a different name, then restart R (see instructions below), run it a second time. Then read in both data sets with the random assignment and assert that they are identical.
    * Note: if creating two cross-randomized variables, you would not want to repeat set.seed(seed) before creating the second one, otherwise it would use the same assignment as the first.

### Running scripts 
Once you complete a jupyter scripty, which you might be running line by line. Use kernal restart and run all to ensure that the script runs in it's entiretly. 

### Reproducibility
Use a virtual environment through `venv` to manage the packages in a project and avoid conflicts related to package versioning. 
    * In the command line `pip freeze > requirements.txt` will create a text document of the packages in the environment `pip install -r requirements.txt` will install all the required packages.

### Misc.
Some additional tips.
    * Progress bars: `progressbar2` for intensite purposes you can add progress bars through this package. See [examples](https://progressbar-2.readthedocs.io/en/latest/examples.html) here.
