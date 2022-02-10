# Python Guide

This guide provides instructions for using Python on research projects. Its purpose is to use with collaborators and research assistants to make code consistent, easier to read, transparent, and reproducible.

Also see my [R Guide](https://github.com/skhiggins/R_guide) and [Stata Guide](https://github.com/skhiggins/Stata_guide).

## Style

For coding style practices, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). 
- While you should read the style guide and do your best to follow it, there are tools to help you.
    - In JupyterLab, first install `flake8`, `pycodestyle`, and  `pycodestyle_magic`. Then include 
        ```python
        %load_ext pycodestyle_magic
        %flake8_on
        ```
        in a blank cell at the top of your script, and each cell afterwards will be checked for styling errors upon running.
    - In Spyder go to Tools > Preferences > Editor > Code Introspection/Analysis and activate the option called "Real-time code style analysis". After doing so, Spyder will show bad formatting warnings directly in the editor.   

## Packages

- Use `pandas` for wrangling data. 
    - [`datatable`](https://github.com/h2oai/datatable) mimics R's `data.table` for working with relatively big data (millions of observations), but I haven't tested it.
    - For truly big data (hundreds of millions or billions of observations) use [`pyspark`](https://spark.apache.org/docs/latest/api/python/index.html).
- Use `datetime` for working with dates.
- Never use `os.chdir()` or absolute file paths. Instead use relative file paths with the `pyprojroot` package.
    <!-- - If you have private information on something like Boxcryptor, this would be the only exception to the rule, in that case, note in your file that this line must be changed. -->
    - `pyprojroot` looks for the following files to determine which oflder is your root folder for the project: .git, .here, *.Rproj, requirements.txt, setup.py, .dvc, *.spyproject, pyproject.toml, .idea, or .vscode. If you don't have any of them, either create a project in Spyder using Projects > New Project, or create a blank file with one of these names (e.g., .here) in your project root directory. 
- Use `assert` frequently to add programmatic sanity checks in the code
- `pandas.describe()` can be useful to print a "codebook" of the data, i.e. some summary stats about each variable in a data set. 
- Use `pipconflictchecker` to make sure there are not dependency conflicts after mass installing packages through pip.
- Use [`fastreg`](https://github.com/iamlemec/fastreg) for fast sparse regressions, particularly good for high-dimensional fixed effects.
- Use [`pandas_tab.tab()`](https://github.com/ryxcommar/pandas_tab/tree/c15ed7cdccb883c7fe3aa36f56a12036cc26063f) for one-way and two-way tabulations similar to Stata's `tabulate`.

## Folder structure 

Generally, within a project folder, we have a subfolder called `analysis` where we are doing data analysis (and other sub-folders like `paper` where the paper draft is saved). Within the `analysis` subfolder, we have:
- An .spyproject file for the project. (This can be created in Spyder, with Projects > New Project.) 
  - If you always open the project within Spyder before working (See "Project" in the left of Spyder) then the `pyprojroot` package will work for relative filepaths.  More details can be found [here](https://docs.spyder-ide.org/current/panes/projects.html). 
- data - only raw data go in this folder
- documentation - documentation about the data go in this folder
- proc - processed data sets go in this folder
- results - results go in this folder
  - figures - subfolder for figures
  - tables - subfolder for tables
- scripts - code goes in this folder
  - Number scripts in the order in which they should be run
  - programs - a subfolder containing functions called by the analysis scripts (if applicable)
  - old - a subfolder where old scripts from previous versions are stored if there are major changes to the structure of the project for cleanliness

## Scripts structure

### Separating scripts
Because we often work with large data sets and efficiency is important, I advocate (nearly) always separating the following three actions into different scripts:
1. Data preparation (cleaning and wrangling)
1. Analysis (e.g. regressions)
1. Production of figures and tables

The analysis and figure/table scripts should not change the data sets at all (no pivoting from wide to long or adding new variables); all changes to the data should be made in the data cleaning scripts. The figure/table scripts should not run the regressions or perform other analysis; that should be done in the analysis scripts. This way, if you need to add a robustness check, you don't necessarily have to rerun all the data cleaning code (unless the robustness check requires defining a new variable). If you need to make a formatting change to a figure, you don't have to rerun all the analysis code (which can take awhile to run on large data sets).

### Naming scripts
- Include a 00_run.py script (described below).
- Because a project often uses multiple data sources, I usually include a brief description of the data source being used as the first part of the script name (in the example below, `ex` describes the data source), followed by a description of the action being done (e.g. `dataprep`, `reg`, etc.), with each component of the script name separated by an underscore (`_`).
- Number scripts in the order in which they should be run, starting with 01. 
<!-- In 00_run.py, the objects should be called run_01_ex_dataprep because objects cannot start with a number but the names of the scripts themselves should be for example 01_ex_dataprep.py, not run_01_ex_dataprep.py. -->

### 00_run.py script 

Keep a script that lists each script that should be run to go from raw data to final results. Under the name of each script should be a brief description of the purpose of the script, as well all the input data sets and output data sets that it uses. Ideally, a user could run the master script to run the entire analysis from raw data to final results (although this may be infeasible for some project, e.g. one with multiple confidential data sets that can only be accessed on separate servers). 
   
  ```python
  # Run script for example project
  
  # PACKAGES ------------------------------------------------------------------
  import os
  import subprocess
  from pyprojroot import here

  # PRELIMINARIES -------------------------------------------------------------
  # Control which scripts run
  run_01_ex_dataprep = 1
  run_02_ex_reg = 1
  run_03_ex_table = 1
  run_04_ex_graph = 1

  program_list = []

  # RUN SCRIPTS ---------------------------------------------------------------
  if run_01_ex_dataprep:
      program_list.append(here('./scripts/01_ex_dataprep.py'))
  # INPUTS
  #  here("./data/example.csv") # raw data from XYZ source
  # OUTPUTS
  #  here("./proc/example_cleaned.csv") # cleaned 

  if run_02_ex_reg:
      program_list.append(here("./scripts/02_ex_reg.py")) 
  # INPUTS
  #  here("./proc/example_cleaned.csv") # 01_ex_dataprep.py
  # OUTPUTS 
  #  here("./proc/ex_results.csv") # regression results
  
  if run_03_ex_table:
      program_list.append(here("./scripts/03_ex_table.py"))
  # Create table of regression results
  # INPUTS 
  #  here("./proc/ex_results.csv") # 02_ex_reg.py
  # OUTPUTS
  #  here("./results/tables/ex_table.tex") # tex of table for paper

  if run_04_ex_graph:
      program_list.append(here('./scripts/04_ex_graph.py')) 
  # Create scatterplot of Y and X with local polynomial fit
  # INPUTS
  #  here("./proc/example_cleaned.csv") # 01_ex_dataprep.py
  # OUTPUTS
  #  here("./results/tables/ex_scatter.eps") # figure    

  for program in program_list:
      subprocess.call(['python', program])
      print("Finished:" + str(program))
  ```
  
If your scripts are .ipynb rather than .py files, instead of using `subprocess.call()` to run the list of programs in `program_list`, replace the `subprocess.call()` loop with the following:
  ```python
  import nbformat
  from nbconvert.preprocessors import ExecutePreprocessor
  for program in program_list:
      with open(program) as f:
          nb = nbformat.read(f, as_version=1)
          ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
          ep.preprocess(nb, {'metadata': {'path': here('./scripts')}})
      print("Finished:" + str(program))
  ```

## Graphing

- Use `matplotlib` or `seaborn` for graphing. For graphs with colors, use `cubehelix` for a colorblind friendly palette.
- For reproducible graphs, always specify the `width` and `height` arguments in `savefig`.
- To see what the final graph looks like, open the file that you save since its appearance will differ from what you see in the JupyterLabs or the Spyder plots pane.
- For higher (in fact, infinite) resolution, save graphs as .eps files. (This is better than .pdf given that .eps are editable images, which is sometimes required by journals.)
  - I've written a Python function [`crop_eps`](https://github.com/skhiggins/PythonTools/blob/master/crop_eps.py) to crop (post-process) .eps files when you can't get the cropping just right in Stata.
- For maps (and working with geospatial data more broadly), use `GeoPandas`.

## Saving files

- For small data sets, save as .csv with `pandas.to_csv()` and read with `pandas.read_csv()`. 
- For larger data sets, save with `pandas.to_pickle()` using a .pkl file extension, and read with `pandas.read_pickle()`. 
- For truly big data sets (hundreds of millions or billions of observations), use `write.parquet()` and `read.parquet()` from `pyspark.sql`.
 
## Randomization

When randomizing assignment in a randomized control trial (RCT):
- Seed: Use a seed from https://www.random.org/: put Min 1 and Max 100000000, then click Generate, and copy the result into your script at the appropriate place. Towards the top of the script, assign the seed with the line 
  ```python
  seed = ... # from random.org
  random.seed(seed)
  ```
  where `...` is replaced with the number that you got from [random.org](https://www.random.org/).
- Use the `stochatreat` package to assign treatment and control groups. 
- Build a randomization check: create a second variable a second time with a new name, repeating `random.seed(seed)` immediately before creating the second variable. Then check that the randomization is identical using `assert(df.var1 == df.var2)`.
- It is also good to do a more manual check where you run the full script once, save the resulting data with a different name, then restart Python (see instructions below), run it a second time. Then read in both data sets with the random assignment and assert that they are identical.

Above I described how data preparation scripts should be separate from analysis scripts. Randomization scripts should also be separate from data preparation scripts, i.e. any data preparation needed as an input to the randomization should be done in one script and the randomization script itself should read in the input data, create a variable with random assignments, and save a data set with the random assignments.

## Running scripts 

Once you complete a script or Jupyter notebook, which you might be running line by line, make sure it runs on a fresh Python session. 
    - To do this in Jupyter, use the menus and select  `Kernel` > `Restart and run all` to ensure that the script runs in its entirety.
    - To do this in Spyder, 

## Reproducibility

Create a virtual environment to run your project. Use a virtual environment through `venv` (instead of `pyenv`) to manage the packages in a project and avoid conflicts related to package versioning. 
- If you are using Anaconda, navigate to the directory of the project in the command line, and type `conda create -n yourenvname python=x.x anaconda`. Activate the environment using `conda activate yourenvname` and `deactivate` will exit the environment.
- First run `conda install pip` to install pip to your directory. 
- Final step in Anaconda to install the packages, find your anaconda directory, it should be something like `/anaconda/envs/venv_name/`. Install new packages by using `/anaconda/envs/venv_name/bin/pip install package_name`, this can also be used to install the requirements.txt file. To create a `requirements.txt` file use `pip freeze -l > requirements.txt` 
- If you are only using Python3, `python3 -m venv yourenvname` will create your environment. Activate the environment using `source activate yourenvname` and `deactivate` will exit the environment.
- In the command line after activating your virtual environment in Python3 using `pip freeze > requirements.txt` will create a text document of the packages in the environment to include in your project directory.
-  `pip install -r requirements.txt` in a virtual environment will install all the required packages for the project in Python3. 

<!---
## Version control

### GitHub

Instructions coming soon.

## Misc.

Some additional tips.

- Progress bars: Use the package `progressbar2` for intensive tasks to monitor progress. See [examples](https://progressbar-2.readthedocs.io/en/latest/examples.html) here.
 ---> 
