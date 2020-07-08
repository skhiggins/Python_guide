# Python Guide

This guide provides instructions for using Python on research projects. Its purpose is to use with collaborators and research assistants to make code consistent, easier to read, transparent, and reproducible.

## Style and Packages 

* For coding style practices, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). 
    - While you should read the style guide and do your best to follow it, there are packages to help you.
    - In Jupyter Notebooks before you write your script you can install three packages `flake8`, `pycodestyle`, and  `pycodestyle_magic`. 
    - If you are in a Jupyter notebook, after importing your files Run `%load_ext pycodestyle_magic` and `%flake8_on` in two blank cells, and each cell afterwards will be checked for styling errors upon running.
    - In Spyder go to Tools > Preferences > Editor > Code Introspection/Analysis and activate the option called `Real-time code style analysis` this will show bad formatting warnings directly in the editor.   
* Use `Pandas` and/or `datatable` for wrangling data. For big data (millions of observations, the efficiency advantages of datatable become important).
* Use `datetime` for working with dates.
* Never use `os.chdir()` or absolute file paths. Instead use relative file paths with the `pyprojroot` package.
* Use `assert` frequently to add programmatic sanity checks in the code
* Use `fastreg` from this [Github] (https://github.com/iamlemec/fastreg) for fast sparse regressions, particularly good for high-dimensional fixed effects.

## Folder Structure 

Generally, within the folder where we are doing data analysis, we have:
* A root folder for the project
    - If you always open the project from the root folder then the `pyprojroot` package will work for relative filepaths
* data - only raw data go in this folder
* documentation - documentation about the data go in this folder
* proc - processed data sets go in this folder
* scripts - code goes in this folder
    - Number scripts in the order in which they should be run

## Master script

Keep a script that lists each script that should be run to go from raw data to final results. Under the name of each script should be a brief description of the purpose of the script, as well all the input data sets and output data sets that it uses. Ideally, a user could run the master script to run the entire analysis from raw data to final results (although this may be infeasible for some project, e.g. one with multiple confidential data sets that can only be accessed on separate servers).

## Graphing

* Use `matplotlib` for graphing. For graphs with colors, use `cubehelix` for a colorblind friendly palette.
* For reproducible graphs, always specify the `width` and `height` arguments in `savefig`.
* To see what the final graph looks like, open the file that you save since its appearance will differ from what you see in the Jupyter Notebook.
* For high resolution, save graphs as .pdf or .svg files. Both of these files have trouble in Google Slides and Powerpoint, but there are workarounds if you want to preserve image quality provided for [pdf](https://support.microsoft.com/en-us/office/insert-pdf-file-content-into-a-powerpoint-presentation-5e7719d5-508c-4c07-a3d4-68123c373a62) and [svg](https://support.google.com/docs/thread/18704826?hl=en)
<!-- * For maps, use the `basemap` package from `matplotlib`, (This has to be installed separately.) A helpful tutorial is available [here] (https://basemaptutorial.readthedocs.io/en/latest/index.html) -->
  
## Randomization

When randomizing assignment in a randomized control trial (RCT):
* Seed: Use a seed from https://www.random.org/: put Min 1 and Max 100000000, then click Generate, and copy the result into your script at the appropriate place. Towards the top of the script, assign the seed with the line `numpy.random.seed(...) # from random.org` where ... is replaced with the number you got from random.org
* Use the `randomizelabel` package to assign treatment and control gorups. It's available at this [Github] (https://github.com/btskinner/randomizelabel) link with instructions. 
* Build a randomization check: create a second variable a second time with a new name, repeating `numpy.random.seed(seed)` immediately before creating the second variable. Then check that the randomization is identical using `df.var1 == df.var2`.
* It is also good to do a more manual check where you run the full script once, save the resulting data with a different name, then restart R (see instructions below), run it a second time. Then read in both data sets with the random assignment and assert that they are identical.
   
## Running scripts 
Once you complete a jupyter script, which you might be running line by line. In the menu go to  `kernel` -> `restart and run all` to ensure that the script runs in it's entirety. 

## Reproducibility
Create a virtual environment to run your project. Use a virtual environment through `venv` (instead of `pyenv`) to manage the packages in a project and avoid conflicts related to package versioning. 
* `python3 -m venv /path/to/new/virtual/environment` this creates the target director and places a `pyvenv.cfg`. Activate this in command line and install all the packages you need in your script here.  
* In the command line after activating your virtual environment using `pip freeze > requirements.txt` will create a text document of the packages in the environment to include in your project directory.
*  `pip install -r requirements.txt` in a virtual environment will install all the required packages for the packages. 

## Misc.

Some additional tips.

* Progress bars: `progressbar2` for intensite purposes you can add progress bars through this package. See [examples](https://progressbar-2.readthedocs.io/en/latest/examples.html) here.