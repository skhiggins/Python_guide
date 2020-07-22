# Python Guide

This guide provides instructions for using Python on research projects. Its purpose is to use with collaborators and research assistants to make code consistent, easier to read, transparent, and reproducible.

## Style

For coding style practices, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). 
* While you should read the style guide and do your best to follow it, there are packages to help you.
    - In Jupyter Notebooks before you write your script you can install three packages `flake8`, `pycodestyle`, and  `pycodestyle_magic`. 
    - If you are in a Jupyter notebook, after importing your files Run `%load_ext pycodestyle_magic` and `%flake8_on` in two blank cells, and each cell afterwards will be checked for styling errors upon running.
    - In Spyder go to Tools > Preferences > Editor > Code Introspection/Analysis and activate the option called `Real-time code style analysis` this will show bad formatting warnings directly in the editor.   

## Packages

* Use `pandas` for wrangling data. 
    - [`datatable`](https://github.com/h2oai/datatable) mimics R's `data.table` for working with relatively big data (millions of observations), but I haven't tested it.
    - For truly big data (hundreds of millions or billions of observations) use [`pyspark`](https://spark.apache.org/docs/latest/api/python/index.html).
* Use `datetime` for working with dates.
* Never use `os.chdir()` or absolute file paths. Instead use relative file paths with the `pyprojroot` package.
    - `pyprojroot` looks for the following files to determine which oflder is your root folder for the project: .git, .here, *.Rproj, requirements.txt, setup.py, .dvc, .spyproject, pyproject.toml, .idea, .vscode. If you don't have any of them, create a blank file with one of these names in your root directory. 
* Use `assert` frequently to add programmatic sanity checks in the code
* Use [`fastreg`](https://github.com/iamlemec/fastreg) for fast sparse regressions, particularly good for high-dimensional fixed effects.

## Folder structure 

Generally, within the folder where we are doing data analysis (the "root folder"), we have the following files and folders. 
* .here or setup.py 
  * If you always open the project from the root folder (e.g., by navigating to that folder in the terminal before running the command `jupter-lab` to open Jupyter in your browser), then the `pyprojroot` package will work for relative filepaths. 
* data - only raw data go in this folder
* documentation - documentation about the data go in this folder
* proc - processed data sets go in this folder
* results - results go in this folder
  * figures - subfolder for figures
  * tables - subfolder for tables
* scripts - code goes in this folder
  * Number scripts in the order in which they should be run
  * programs - a subfolder containing functions called by the analysis scripts (if applicable)

## Scripts structure

### Separating scripts
Because we often work with large data sets and efficiency is important, I advocate (nearly) always separating the following three actions into different scripts:
1. Data preparation (cleaning and wrangling)
1. Analysis (e.g. regressions)
1. Production of figures and tables

The analysis and figure/table scripts should not change the data sets at all (no pivoting from wide to long or adding new variables); all changes to the data should be made in the data cleaning scripts. The figure/table scripts should not run the regressions or perform other analysis; that should be done in the analysis scripts. This way, if you need to add a robustness check, you don't necessarily have to rerun all the data cleaning code (unless the robustness check requires defining a new variable). If you need to make a formatting change to a figure, you don't have to rerun all the analysis code (which can take awhile to run on large data sets).

### Naming scripts
* Include a 00_run.ipynb script (described below).
* Number scripts in the order in which they should be run, starting with 01.
* Because a project often uses multiple data sources, I usually include a brief description of the data source being used as the first part of the script name (in the example below, `ex` describes the data source), followed by a description of the action being done (e.g. `dataprep`, `reg`, etc.), with each component of the script name separated by an underscore (`_`).

### 00_run.ipynb script 

Keep a script that lists each script that should be run to go from raw data to final results. Under the name of each script should be a brief description of the purpose of the script, as well all the input data sets and output data sets that it uses. Ideally, a user could run the master script to run the entire analysis from raw data to final results (although this may be infeasible for some project, e.g. one with multiple confidential data sets that can only be accessed on separate servers).
   
  ```r
  # Run script for example project
  
  # PACKAGES ------------------------------------------------------------------
  import nbformat
  from nbconvert.preprocessors import ExecutePreprocessor
  from pyprojroot import here

  # PRELIMINARIES -------------------------------------------------------------
  # Control which scripts run
  run_01_ex_dataprep = 1
  run_02_ex_reg = 1
  run_03_ex_table = 1
  run_04_ex_graph = 1
  
  # RUN SCRIPTS ---------------------------------------------------------------
  
  # Read and clean example data
  if (run_01_ex_dataprep):
     with open(here('./scripts/run_01_ex_dataprep.ipynb')) as f:
        nb = nbformat.read(f, as_version=1)
     ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
     ep.preprocess(nb, {'metadata': {'path': here('./scripts')}})

  # INPUTS
  #  here("data", "example.csv") # raw data from XYZ source
  # OUTPUTS
  #  here("proc", "example_cleaned.csv") # cleaned 
  
  # Regress Y on X in example data
  if (run_02_ex_reg):
     with open(here('./scripts/run_02_ex_reg.ipynb')) as f:
        nb = nbformat.read(f, as_version=1)
     ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
     ep.preprocess(nb, {'metadata': {'path': here('./scripts')}})  
  # INPUTS
  #  here("./proc/example_cleaned.csv") # 01_ex_dataprep.ipynb
  # OUTPUTS 
  #  here("./proc/ex_fixest.csv") # fixest object from feols regression
  
  # Create table of regression results
 if (run_03_ex_table):
     with open(here('./scripts/run_03_ex_table.ipynb')) as f:
        nb = nbformat.read(f, as_version=1)
     ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
     ep.preprocess(nb, {'metadata': {'path': here('./scripts')}})   
  # INPUTS 
  #  here("./proc/ex_fixest.csv") # 02_ex_reg.ipynb
  # OUTPUTS
  #  here("./results/tables/ex_fixest_table.tex") # tex of table for paper
  
  # Create scatterplot of Y and X with local polynomial fit
  if (run_04_ex_graph):
     with open(here('./scripts/run_04_ex_graph.ipynb')) as f:
        nb = nbformat.read(f, as_version=1)
     ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
     ep.preprocess(nb, {'metadata': {'path': here('./scripts')}})  
  # INPUTS
  #  here("./proc/example_cleaned.csv") # 01_ex_dataprep.ipynb
  # OUTPUTS
  #  here("./results/tables/ex_scatter.eps") # figure
  ```

## Graphing

* Use `matplotlib` for graphing. For graphs with colors, use `cubehelix` for a colorblind friendly palette.
* For reproducible graphs, always specify the `width` and `height` arguments in `savefig`.
* To see what the final graph looks like, open the file that you save since its appearance will differ from what you see in the Jupyter Notebook.
* For high resolution, save graphs as .pdf or .eps files. Both of these files have trouble in Google Slides and Powerpoint, but there are workarounds if you want to preserve image quality provided for [pdf](https://support.microsoft.com/en-us/office/insert-pdf-file-content-into-a-powerpoint-presentation-5e7719d5-508c-4c07-a3d4-68123c373a62) and [eps](https://nutsandboltsspeedtraining.com/powerpoint-tutorials/import-eps-files-into-powerpoint/)
     * I've written a Python function [`crop_eps`](https://github.com/skhiggins/PythonTools/blob/master/crop_eps.py) to crop .eps files for the times when you can't get the cropping just right 
<!-- * For maps, use the `basemap` package from `matplotlib`, (This has to be installed separately.) A helpful tutorial is available [here] (https://basemaptutorial.readthedocs.io/en/latest/index.html) -->

## Saving files

* For small data sets, save as .csv with `pandas.to_csv()` and read with `pandas.read_csv()`. 

* For larger data sets, save as .h5 with `HDFStore()` with the `pytables` package, and read with `open_file()`. 

## Randomization

When randomizing assignment in a randomized control trial (RCT):
* Seed: Use a seed from https://www.random.org/: put Min 1 and Max 100000000, then click Generate, and copy the result into your script at the appropriate place. Towards the top of the script, assign the seed with the line 
  ```r
  random.seed(...) # from random.org
  ```
  where `...` is replaced with the number that you got from [random.org](https://www.random.org/) 
* Use the `stochatreat` package to assign treatment and control groups. 
* Build a randomization check: create a second variable a second time with a new name, repeating `random.seed(seed)` immediately before creating the second variable. Then check that the randomization is identical using `assert(df.var1 == df.var2)`.
* It is also good to do a more manual check where you run the full script once, save the resulting data with a different name, then restart Python (see instructions below), run it a second time. Then read in both data sets with the random assignment and assert that they are identical.

Above I described how data preparation scripts should be separate from analysis scripts. Randomization scripts should also be separate from data preparation scripts, i.e. any data preparation needed as an input to the randomization should be done in one script and the randomization script itself should read in the input data, create a variable with random assignments, and save a data set with the random assignments.

## Running scripts 

Once you complete a jupyter script, which you might be running line by line. In the menu go to  `kernel` -> `restart and run all` to ensure that the script runs in it's entirety. 

## Reproducibility

Create a virtual environment to run your project. Use a virtual environment through `venv` (instead of `pyenv`) to manage the packages in a project and avoid conflicts related to package versioning. 
* If you are using Anaconda, navigate to the directory of the project in the command line, and type `conda create -n yourenvname python=x.x anaconda`. Activate the environment using `conda activate yourenvname` and `deactivate` will exit the environment.
* If you are only using Python3, `py -m venv yourenvname`. Activate the environment using `source activate yourenvname` and `deactivate` will exit the environment.
* Install all the packages necessary for your project in your active virtual environment.
* In the command line after activating your virtual environment using `pip freeze > requirements.txt` will create a text document of the packages in the environment to include in your project directory.
*  `pip install -r requirements.txt` in a virtual environment will install all the required packages for the packages. 

## Version control

### GitHub

Instructions coming soon.

## Misc.

Some additional tips.

* Progress bars: Use the package `progressbar2` for intensive tasks to monitor progress. See [examples](https://progressbar-2.readthedocs.io/en/latest/examples.html) here.