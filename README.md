# Analog Daddy

## Motivation

This library shows Analog Design who the daddy is. Well, it's just an attempt to make transistor sizing less painful. Additionally, it includes certain scripts and tools to make any aspect of Analog Design a little less painful.

Analog Design requires practice, intuition and experience. It is difficult to build circuits for a given specification that works across PVT (process, voltage and temperature) corners. Then they should also work in real silicon.
It is 'hard' and requires time.
However, as far as the transistor sizing for a given DC operating point goes, with complicated models, pen-paper calculations to actual design convergence
have become more painful. The lookup table based design methodology tries to find a middle ground. You can read more about it in
[Systematic Design of Analog CMOS Circuits: Using Pre-Computed Lookup Tables by P.G.A. Jespers and B. Murmann, Cambridge University Press, 2017](https://www.cambridge.org/us/academic/subjects/engineering/circuits-and-systems/systematic-design-analog-cmos-circuits-using-pre-computed-lookup-tables?format=AR).

## Previous Work

The [Gm/Id starter kit by Prof. Boris Murmann et al.](https://github.com/bmurmann/Book-on-gm-ID-design)
is an excellent tool to get comfortable with gm/id methodology and use Lookup tables in general with whatever design methodology you like. Thus, this kit could serve as an advanced calculator. The kit
is excellently written, but it is written in Matlab. I have a different blog post detailing why Matlab sucks, but the gist is that if this tool/methodology
is going to be learned by new Analog Design engineers like me and taught in many other institutes, I would want them to use Python in this fun venture. Additionally, my experience with interactive plotting capabilities of MATLAB has been subpar.
There are multiple toolkits already written which are listed on the main website. Below, I add the summaries and why I am not going in that direction.

1. [Analog Designer's Toolbox](https://adt.master-micro.com/): Maybe, I will eventually get bored of maintaining this library and using this polished tool
for my day-to-day work, but I feel that there has to be some alternative for the hobbyists and enthusiasts to tinker with.
The tool is closed-source and might be made for serious work. I would want this tool we are building to be polished and be used for serious work but also would want it open source for interested people to tinker with and a community to be built around it.

2. [Fengqi Zhang’s gmIdNeoKit](https://github.com/fengqzHD/gmIdNeoKit): This modification improves upon the data generation process in MATLAB by adding
the -v7.3 flag which is essential for large databases and should be the default. Secondly, it provides a nice GUI to work with. However, for any modifications,
I would have to learn pyQT5. I prefer using Jupyter Notebooks and accompanying widgets since it is easily shareable and presentable. Plus, I would prefer
using interactive plotting from the very beginning using Plotly or Dash.

3. [Ashwith Rego’s Python code (pyMOSchar)](https://github.com/ashwith/pyMOSChar): This by far is the closest to what I would want the tool to do. However, it is not
modified for Python 3. Additionally, it used the binary reading of the PSF files, which was a pain in the ass to debug. Additionally, it does not
support cross-ratio lookup.
With all these different variants available, yet with certain shortcomings in each approach, I decided to start a more 'modern' and open implementation.
But, thanks to these existing code-bases I don't have to reinvent the wheel and this serves as a good reference.

4. [Mohamed Watfa's gmid toolkit in Python](https://github.com/medwatt/gmid): While I was trying to actively avoid writing the library, he has written something which works. I am in process of taking ideas from this toolkit. However, it currently does not support importing data from Cadence's Assembler and I have no clue how the numpy file is structured to use the functions. The author has updated with a new way to generate LUT recently (Nov 2 2023).

## Roadmap

I wrote this with high hopes that I will get motivated to write it. Turns out I really don't like to code. But a good thing happened. ChatGPT!
Well I am taking all the help from ChatGPT and whatever to avoid writing the code myself. I will keep my results posted here.

The following are the key features in order of priority of them being implemented.

- [x] Thoroughly document the process of setting up custom Testbench (Cadence Virtuoso) and Expression setup in (Cadence Assembler).
- [x] Thoroughly documented code. (Tried my best to ask ChatGPT to document it.)
- [ ] Packaging for `pip`.
- [ ] Packaging for `conda-forge`.
- [x] Test suite for basic functions, so that upgrading libraries and dependency is easier.
- [ ] Support lazy loading of the database file to improve speed and efficiency. Not sure if it is needed right now.
- [x] Support all the lookup modes
- [ ] Support for `lookupVGS` and corresponding test suite.
- [x] Give templates for basic and interactive plotting using Plotly/Dash. See the [notebooks directory](./docs/notebooks)
- [x] Have basic plots and a template `.npy` file for ~[Skywater-130 nm PDK](https://github.com/google/skywater-pdk)~ GPDK for illustration and design purposes. I will not be using Skywater-130 nm PDK since a there is no version of PDK available to setup with Cadence for free. Instead, a derived data and plot of GPDK will be shared here. This will not violate any licensing restrictions since this is derived data and and has smaller data points.

## Acknowledgements and Licensing

This library was created with extensive help of ChatGPT and White Claw Hard Seltzer. Both have helped equally in programming, debugging and testing; with extra patience donated by White claw
when ChatGPT refused to work for me. Additionally, I have use few ideas from the previous work mentioned above. This work will be licensed as AGPLv3 since I would not
want anyone to monetize this and even if they do I want the changes to be given back to this tool's codebase.

One misconception for engineers in corporate environments is that if they modify the tool and distribute it internally within the company, they would have
to make the source code public. NO! If it is distributed over a network, the "users" which in your case would be your employees have the right
to request the source code, which is usually accessible to anyone within your organization. So you are all good to go and use it even within your company.
I would love to merge the changes you make to the tool and be public, but I understand that might not be entirely possible, which is okay.

Special thanks to Bharadwaj Padmanabhan for helping in testbench creation and providing the relevant images. I would also like to thank Gayathri Nair for helping me to generate the LUT for GPDK90.

## Installation

### Online Installation for devices with internet access

If you are setting up Python for the first time, you need to install [miniconda](https://docs.conda.io/projects/miniconda/en/latest/) by following the instructions [here](https://docs.conda.io/projects/miniconda/en/latest/). You can alternatively install [Anaconda](https://www.anaconda.com/download/). [Difference between Anaconda or Miniconda](https://stackoverflow.com/questions/45421163/anaconda-vs-miniconda)

After that you need to create what is called a conda environment. For the examples below the name of my environment is "test_env". Then we use [conda-forge](https://conda-forge.org/)

```bash
# create a test_env with the required configuration.
conda create --name test_env python=3.10 jupyterlab scipy numpy matplotlib dash pandas
conda config --add channels conda-forge
conda config --set channel_priority strict
conda activate test_env
```

Now you can install the package using the following.

```bash
# for online installation
pip install git+ssh://git@github.com/siddhantladdha/analog_daddy.git
```

To upgrade to the latest version you need to uninstall and re-install using the
following. [Source](https://stackoverflow.com/questions/71356330/updating-pip-installed-package-from-git)

```bash
pip uninstall analog_daddy
pip install git+ssh://git@github.com/siddhantladdha/analog_daddy.git
```

### Offline installation for devices without internet access

Sometimes, the linux servers you design on at workplace have limited or no internet
access. Creating an offline installation of miniconda/conda and porting it to your
server is painful. The good news is if the IT department at your workplace is
competent, you might already have access to reasonably newer versions of the above
required libraries. In that case you can just clone this repository.

If there is no such provision in place I feel it is your right to file a JIRA ticket and
get such an installation working. (They can follow the online installation and set it up
for designers company wide.) However, do remember that they also have the right to refuse
to set it up. So the best course of action would be to use this on your local machine.
(Windows/Mac/Linux). You can then follow Online installation.

Or if the libraries are maintained and you still want to install it here is the command.
It is highly recommended you create a virtual environment and install it.

```bash
# for offline installation if you have installed the repository
pip install /path/to/your/local/git/repo
```

## Usage

- [Testbench Setup Instructions](./docs/notebooks/testbench_setup.ipynb)
- [Import Demo Jupyter Notebook](./docs/notebooks/import_demo.ipynb)
- [Usage Demo Jupyter Notebook](./docs/notebooks/usage_demo.ipynb)
- [Design Demo Jupyter Notebook](./docs/notebooks/design_demo.ipynb)

## Testing and Packaging (For Developer use)

```python
python -m unittest discover tests
```

```bash
python setup.py sdist bdist_wheel # run this command after any updates to make sure package is build correctly.
# pip freeze > requirements.txt  # incase you add or remove any dependencies.
```
