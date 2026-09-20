# Control Systems - GNU Radio Conference 2026

**Miniforge and Python Environment - Installation Instructions**

**The DSP Coach, LLC**

**Last Updated: September 20, 2026**

Installs:

- Miniforge (conda)
- Python 3.14
- NumPy 2.5, SciPy 1.18, Matplotlib 3.11, python-control 0.10
- marimo 0.24
- IPython 9.17

---

## Overview

The following is a procedure for installing Miniforge, which includes Python,
together with the handful of additional libraries needed to run the "Control
Systems" notebook used in this session. Allow yourself at least thirty minutes
to complete this procedure, most of which is download time while conda
retrieves the packages.

So that the notebook provided for the workshop runs seamlessly, please install
Miniforge and the associated python packages according to these instructions
where possible, and bring any issues you encounter to my attention before the
session rather than during it, so that valuable workshop time isn't spent
dealing with installation related issues. The steps below were written so that
they apply equally to Windows, macOS and Linux; where a step genuinely differs
between platforms, that is called out with a separate heading for each
operating system.

If you already have a working Python installation that you use for other
purposes, there is no need to remove it or to change it in any way. Everything
in this procedure is done inside a separate conda environment created
specifically for this workshop, which leaves the rest of your machine exactly
as it is. If you already have Miniconda or Anaconda installed rather than
Miniforge, that is also fine and you can skip STEP 1 entirely; the commands in
the remaining steps have been written so that they work identically on all
three distributions.

**A note on marimo:**

The notebook for this session is a marimo notebook rather than a Jupyter
notebook, so if you were expecting Jupyter, that is the one thing here that
will be unfamiliar. marimo is a newer notebook environment for Python that
differs from Jupyter in two ways that matter to us. The first is that a marimo
notebook is stored as an ordinary Python file rather than as a JSON document
with the outputs embedded in it, which makes the material far easier to
distribute, to read, and to track in version control. The second is that
marimo is reactive: rather than running cells yourself in the correct order
and hoping the state is what you think it is, marimo works out which cells
depend on which, and when a value changes it automatically re-runs everything
downstream of it. That second property is the reason I have moved this
particular session over, because it lets the loop filter parameters be put on
sliders so that the Bode plot, the stability margins and the step response all
update as you move them, which is a much better way to teach loop design than
looking at a fixed set of plots.

You do not need to know anything about marimo in advance. It is installed as
part of STEP 2 along with everything else, and STEP 5 explains how to open the
notebook and what you are looking at.

**Anaconda, Miniconda, and Miniforge:**

Anaconda is a large download that includes most of the libraries and modules
commonly used in data science applications. We will instead use Miniforge,
which is a minimal installer for conda (an open-source package and environment
manager), where any additional libraries needed, now or in the future, can be
downloaded and installed as needed. Miniforge is maintained by the conda-forge
community rather than by Anaconda, Inc., and it is configured out of the box to
pull packages from the conda-forge channel, which carries no commercial
licensing requirements and keeps this environment free to use in personal,
academic and commercial settings alike. The conda commands and syntax are
identical to those used with Anaconda or Miniconda, so any prior familiarity
you have carries over directly.

Unlike the environments used in my longer courses, nothing installed here has
to be compiled from source, which means there is no need to install Microsoft
C++ Build Tools on Windows, the Xcode Command Line Tools on macOS, or a
compiler toolchain on Linux. Every package comes as a prebuilt conda package
for all three platforms, and this procedure is correspondingly shorter than the
installation guides used in the courses.

## Formatting Conventions

Throughout this document the following conventions are used:

Text indicating code you should enter verbatim is shown in a code block:

```bash
marimo edit control_systems.py
```

Text indicating generic code that should be replaced is enclosed in `<>`:

```
conda activate <env-name>
```

---

## STEP 1: Install Miniforge

If you already have Miniforge, Miniconda or Anaconda installed on your machine
and it is working, you do not need to install anything in this step and you can
proceed directly to STEP 2: Create the Workshop Environment. Everything that
follows works with any of the three distributions.

For a new installation, download the installer appropriate for your operating
system from the following link:

<https://conda-forge.org/download/>

### Windows Users

From the download page, choose the **Windows x86_64** installer, which is a
normal graphical installer ending in `.exe`. Run it and accept the defaults as
you proceed through the installation, with the following two exceptions worth
paying attention to. When prompted for who the installation is for, be sure to
select **"Just Me"**, otherwise there can be permission related issues later.
When prompted for the installation location, accept the default location unless
that path contains spaces or characters outside the standard English alphabet
(for example, it is recommended not to install into a path such as
`C:\Program Files`), since paths of that kind are a known source of trouble with
conda. Press Install to accept the default Advanced Installation Options and
complete the installation, then press Next and Finish on the final screen.

Once the installation has completed, open the **"Miniforge Prompt"**. This can
be launched from the Windows Start Menu from the Miniforge3 folder, or by
simply typing "Miniforge" in the "Type Here to Search" field next to the Start
button in the lower left-hand corner of the screen. Use this Miniforge Prompt
window for every command given in the remainder of this document, rather than
the standard Command Prompt (`cmd.exe`) or PowerShell, as those will not have
conda available to them until further configuration is done.

### macOS Users

The download page offers two different macOS installers and you need the one
that matches the processor in your Mac. To determine which one that is, open
the Apple menu in the top-left corner of the screen and choose **About This
Mac**. A line reading **Chip: Apple M1** (or M2, M3, M4, or any other M-series
chip) means you have Apple Silicon and should download the **Apple Silicon**
(`arm64`) installer, while a line reading **Processor: Intel** means you should
download the **Intel** (`x86_64`) installer. If you would rather determine this
from the terminal, entering `uname -m` will report `arm64` for Apple Silicon and
`x86_64` for Intel.

Note that the macOS download is a shell script ending in `.sh` rather than an
application, so double-clicking it in the Finder will not install anything.
Instead, open a Terminal window and enter the following two commands, which
change into your Downloads folder and then run the installer script:

```bash
cd ~/Downloads
bash Miniforge3-*.sh
```

Accept the license agreement and the default installation location as the
installer prompts you. When the installer asks whether you wish to update your
shell profile to automatically initialize conda, answer **yes**. This is the
step that makes the `conda` command available in every new terminal window you
open afterward, and skipping it is the most common reason for conda appearing
not to have installed at all. Once the installation has completed, close the
Terminal window and open a new one so that the profile changes take effect.

### Linux Users

From the download page, choose the **Linux x86_64** installer, which is a shell
script ending in `.sh`. Open a terminal window and enter the following two
commands, which change into your Downloads folder and then run the installer
script:

```bash
cd ~/Downloads
bash Miniforge3-*.sh
```

Accept the license agreement and the default installation location as the
installer prompts you, and answer **yes** when the installer asks whether you
wish to update your shell profile to automatically initialize conda, as this is
what makes the `conda` command available in new terminal windows. Once the
installation has completed, close the terminal window and open a new one so
that the profile changes take effect.

### Confirming the Miniforge Installation

On all three platforms, confirm that the installation was successful by
entering the following (on Windows this is entered in the Miniforge Prompt
described above, and on macOS and Linux in a terminal window that you have
opened *after* completing the installation):

```bash
conda --version
```

The response should be the word `conda` followed by a version number, for
example `conda 25.7.0`. The exact version number is not important.

If instead you are on macOS or Linux and the terminal responds with
`conda: command not found`, this most likely means that the shell profile
initialization step mentioned above was skipped during the installation. This
can be corrected by entering the following, then closing and reopening the
terminal window and repeating the `conda --version` test above:

```bash
~/miniforge3/bin/conda init
```

---

## STEP 2: Create the Workshop Environment

This step creates a new conda environment named `grcon2026_control` and installs
into it everything that the "Control Systems" notebook needs. Creating a
separate environment in this way, rather than installing these packages
alongside everything else on your machine, is what allows the workshop material
to run in a known configuration without disturbing any other Python work you
may have.

Open the Miniforge Prompt on Windows, or a terminal window on macOS or Linux.
You should see `(base)` at the left of the prompt, which indicates that the
base conda environment is active. If you do not see it, enter
`conda activate base` first.

Then change into the workshop folder, replacing the path shown with the actual
location of the folder on your machine, as the first of the two approaches
below reads a file from it:

```bash
cd <path-to-workshop-folder>
```

There are two ways to create the environment from here and both produce the
same result. Try the environment file first. If it gives you any trouble at
all, simply move on to the single command that follows it, which is one line
and is the more robust of the two across platforms.

### Option 1: Create the environment from the environment file

The workshop folder contains a conda environment file, `grcon2026_control.yml`,
which lists the environment name, the channel and every package to be
installed. Creating the environment from it takes one command:

```bash
conda env create -f grcon2026_control.yml
```

**Please note that this route has not been tested.** It is provided as a
convenience for those who prefer working from an environment file, but the
environment used for the workshop was built and tested with the command in
Option 2 below, not with this one. If conda reports an error, cannot find or
read the file, or anything else does not go as described here, do not spend
time on it. Remove any partial environment by entering
`conda env remove --name grcon2026_control` and use Option 2 instead, which
installs exactly the same set of packages.

### Option 2: Create the environment with a single command

If you created the environment with Option 1, you can skip this and go on to
STEP 3. Otherwise, enter the following as a single command on one line. Be
careful when copying and pasting from this document, as some viewers will
render the two consecutive dashes in `--name` as a single long dash, which
conda will not accept:

```bash
conda create --name grcon2026_control -c conda-forge python=3.14 numpy=2.5 scipy=1.18 matplotlib=3.11 control=0.10 marimo=0.24 ipython=9.17
```

This is the command the workshop environment was actually built and tested
with. It depends on no file being present, it does not care which folder you
run it from, and it behaves identically on Windows, macOS and Linux, which is
why it is the one to fall back to if the environment file gives any trouble.

### Whichever route you took

Conda will take a minute or so to work out which versions of these packages and
their dependencies fit together, will then print the full list of packages it
proposes to install, and will ask you to confirm before it proceeds. Review the
list if you wish and then press `y` and enter to continue. The download and
installation that follows will take several minutes and will retrieve a few
hundred megabytes of packages.

Two things about what is being installed are worth explaining, since they are
deliberate and appear in both routes above.

First, each package is given an explicit version number. This is so that the
environment you end up with is the same one that the notebook was developed and
tested against, rather than whichever releases happen to be current on the day
you run the command, and so that the same environment can be recreated in the
same form later on. The versions given are pinned at the minor release, which
means conda is free to select the most recent patch release within that line,
as patch releases within a line are the least likely to change behaviour. These
particular versions are the ones that were installed and tested on Windows on
September 19, 2026, which were current at that time.

Second, the packages are taken from the conda-forge channel, which is what the
`-c conda-forge` option in the single command and the `channels:` entry in the
environment file each specify. If you are using Miniforge this is already the
default and it changes nothing, but stating it explicitly means the identical
instructions also work correctly for anyone using Miniconda or Anaconda,
without permanently changing the channel configuration on their machine.

For reference, the libraries being installed are used by the notebook as
follows. NumPy provides the array and mathematical operations used throughout
and is imported as `np`, with its random number routines imported separately as
`rand`. SciPy provides the signal processing and FFT routines, imported as
`sig` and `fft` respectively. Matplotlib produces all of the plots and is
imported as `plt`. The python-control package, which conda installs under the
name `control`, is imported as `con` and provides the transfer function, Bode
plot, pole-zero map, model reduction and step response functions that the
control loop analysis is built on. marimo provides the notebook environment
itself, along with the slider controls used to vary the loop filter parameters,
the interactive pan and zoom on the matplotlib plots, and the audio playback
used in the FM demodulation example. IPython is not used by the notebook
itself, and is included because it provides a considerably more capable
interactive Python prompt than the default one, which is worth having at the
command line for trying something out quickly outside the notebook. The
notebook additionally imports the `math` and `wave` modules, but both of those
are part of the Python standard library and are installed along with Python
itself, so nothing further is needed for them.

---

## STEP 3: Activate the Environment

Creating an environment does not automatically begin using it, so the next step
is to activate it. Enter the following:

```bash
conda activate grcon2026_control
```

The prompt will change from `(base)` to `(grcon2026_control)`, and that change
is your confirmation that the environment is active. Every remaining command in
this document must be entered with `(grcon2026_control)` showing at the left of
the prompt, otherwise you will be working in a different environment and the
packages just installed will not be found.

(Windows users who would rather work in PowerShell than in the Miniforge Prompt
need one additional step first, and the order it is done in matters. PowerShell
knows nothing about conda until it has been set up for it, so the activate
command above will either report that `conda` is not recognized or simply leave
the prompt unchanged. That setup has to be started from the Miniforge Prompt,
as it is the only window where conda can be reached to begin with: open the
Miniforge Prompt as described in STEP 1, enter `conda init powershell` once,
then close it and open a new PowerShell window, after which
`conda activate grcon2026_control` will work there as expected. It only needs
doing once. Entering `conda init powershell` from within PowerShell itself will
not work, for the same reason the activate command does not. None of this
applies if you simply use the Miniforge Prompt throughout, which is what I
would recommend.)

---

## STEP 4: Confirm the Installation

Perform the following steps to confirm that everything is ready before the
workshop, rather than discovering a problem during the session.

With the environment activated as described in STEP 3, first confirm that all
of the libraries import correctly by entering the following as a single line:

```bash
python -c "import numpy, scipy, matplotlib, control, marimo, IPython; print('Environment OK')"
```

The response should be a single line reading `Environment OK`, after which you
are returned to the prompt with nothing else printed. If instead you see a
`ModuleNotFoundError`, or any other error traceback, then one of the packages
did not install correctly and it is worth repeating STEP 2 before going any
further.

**Be patient the first time you run this.** On a newly created environment this
command can take a minute or more with no output at all, and it will look for
all the world as though it has hung. It has not. Python is compiling the
freshly installed packages the first time they are imported, and on Windows the
antivirus software is scanning the several hundred megabytes of files that
conda has just written, neither of which happens again afterward. Leave it
alone and let it finish. Run the same command a second time and it will
complete in a couple of seconds, which is the speed you can expect from then
on, including the first time you open the notebook in STEP 5.

If you would like to see the versions that were installed, the following will
report them:

```bash
python -c "import numpy, scipy, matplotlib, control, marimo, IPython; print(numpy.__version__, scipy.__version__, matplotlib.__version__, control.__version__, marimo.__version__, IPython.__version__)"
```

Confirm the Python version as well by entering `python -V` and pressing enter
(be sure to use a capital V, as a lower case v means "verbose"). The response
will be the word `Python` followed by the version number installed in the
environment.

---

## STEP 5: Open and Run the Notebook

The final step is to confirm that marimo starts and that the workshop notebook
opens and runs.

With the environment still activated, navigate to the folder containing the
workshop material and open the notebook. Replace the path shown below with the
actual location of the workshop folder on your machine:

```bash
cd <path-to-workshop-folder>
marimo edit control_systems.py
```

marimo will start a small local server and open the notebook in your default
web browser. If for any reason the browser does not open by itself, look at the
terminal window, where marimo prints a web address beginning `http://localhost`
that you can copy and paste into a browser yourself.

**Running the notebook once it has opened.** When the notebook first appears,
its cells have not yet been run, so the plots and results will not be showing
yet. Press the play button in the lower right hand corner of the window to run
the notebook through. Note that this first run will take noticeably longer than
subsequent ones, for the same reason described in STEP 4, so give it a moment
to finish.

If you would rather the notebook ran by itself each time it is opened, rather
than waiting for you to press play, that behaviour can be changed through the
"Runtime Reactivity" options along the lower left hand side of the window,
where the notebook can be set to run automatically on open.

**What you are looking at.** If you have used Jupyter before, the most
important difference to understand is that you do not run the cells yourself in
order. marimo determines which cells depend on the values produced by which
other cells, and it runs them in the correct order on your behalf. When you
move one of the sliders controlling the loop filter parameters, every plot and
every calculated result that depends on that value is recalculated and redrawn
immediately. There is therefore no such thing as a cell that has gone stale, or
a result on screen that no longer matches the code that produced it, which is
the failure mode this format is designed to remove.

Work down the notebook from the top as you would with any other document. Where
sliders are provided, move them and watch how the Bode plot, the stability
margins and the step response respond, since that is the part of the session
the notebook is built around.

**One section requires an additional file.** The FM demodulation example near
the end reads a captured IQ recording that is not distributed with the
material, for licensing reasons explained in `data/README.md` in the workshop
folder. That file explains where to download the recording and where to place
it. Every other part of the notebook runs without it.

When you are finished, return to the terminal or Miniforge Prompt window that
you started marimo from and press `Ctrl-C` to stop the server, after which the
browser tab can be closed. Note that this window must stay open while you are
working, as closing it stops the server and the notebook in the browser will
stop responding.

---

## Troubleshooting

**The browser does not open when marimo starts.** This happens on some systems
where no default browser is registered, and it does not indicate a problem with
the installation. Look in the terminal window for the line beginning
`http://localhost` and paste that address into a browser yourself.

**marimo reports that the address or port is already in use.** This means
another program, very often a marimo or Jupyter server left running from
earlier, already holds the default port. Either close that other window, or
start marimo on a different port by adding the `--port` option, for example
`marimo edit control_systems.py --port 2719`.

**PowerShell reports that running scripts is disabled on this system.** This
applies only to those who have chosen to use PowerShell rather than the
Miniforge Prompt, as described in STEP 3. A fresh Windows installation sets its
execution policy to `Restricted`, which blocks all scripts from running,
including the profile script that `conda init powershell` writes. The result is
that the initialization appears to have been carried out correctly, but the new
PowerShell window still cannot find conda, and usually shows an error
mentioning that running scripts is disabled. Allow locally created scripts to
run by entering the following once in PowerShell, then closing and reopening
the window:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

This applies to your own user account only and does not need administrator
rights. None of it is necessary if you use the Miniforge Prompt throughout.

**A message appears reading `Terms of Service have not been accepted for the
following channels`.** This is seen on Miniconda and Anaconda installations,
which are configured by default to use Anaconda's own package repository, and
recent versions of conda require those terms to be accepted before any command
will run. Nothing used in this workshop comes from that repository. You can
either accept the terms as the message instructs, or remove those channels
altogether by entering the following and then repeating STEP 2:

```bash
conda config --remove channels defaults
```

**The download fails partway through** with a message reading
`Connection broken`, `IncompleteRead`, or a similar connection error. This
simply means that the network connection dropped while packages were being
retrieved and there is nothing wrong with the command you entered. Re-run
whichever command from STEP 2 you used, as any packages already downloaded are
cached locally and the retry will pick up roughly where it left off. If the
retry instead reports that the environment already exists, remove the partial
environment first by entering `conda env remove --name grcon2026_control` and
then run the create command again.

---

© 2026 The DSP Coach, LLC (https://dsp-coach.com)

This document, the installation instructions accompanying "Control Systems -
GNU Radio Conference 2026" by The DSP Coach, is licensed under CC BY-NC-ND
4.0. To view a copy of this license, visit
<https://creativecommons.org/licenses/by-nc-nd/4.0/>

The example code these instructions prepare your machine to run is licensed
separately, under the MIT License. See the `LICENSE` and `LICENSE-CONTENT.md`
files distributed alongside this document.

That license covers the text of this document only. It does not extend to the
software described here: Miniforge, Python, NumPy, SciPy, Matplotlib,
python-control, marimo and IPython are independent open-source projects, each
distributed by its own authors under its own license, and nothing in this
document grants, restricts or alters any right in them. Product and company
names referred to throughout are the trademarks of their respective owners and
are used here only to identify the software being installed.
