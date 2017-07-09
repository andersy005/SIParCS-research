# Make a module

Sometimes the best way to get access to a piece of software on the HPC system is to install it yourself as a **local install**. I learned this the hard way!


# Motivation:

Apparently [Spark Worker launch script](https://ncar.github.io/PySpark4Climate/installation/cheyenne/) must fork another process that doesn't inherit the same environment as the Master.

This caused us so much trouble every time we wanted to use a package that was locally installed and not system-widely installed.

**Solution:**
- Create modules for packages that are locally installed. 

This documents details the procedure for maintaining local installs in user's home directory or project space. 

**Note:** Throughout this document we'll assume you are installing into a directory named ```installs``` that is located in the ```work space``` on Glade filesystem, but you can follow the steps below in any directory for which you have read/write permissions.


## Getting Started
Before installing your software, you first preparea place for it to live. We recommend the following directory structure, which you should create in the top-level of your home directory or installs directory or any other directory where you have **read/write** permissions.

```
local
|-- src
|-- share
    `--lmodfiles
```

 Each directory serves a specific purpose:

 - ```local``` - Gathers all the files related to your local installs into one directory, rather than cluttering your home directory. Applications will be installed into this directory with the format "appname/version". This allows you to easily store multiple versions of a particular software install if necessary.


- ```local/src``` - Stores the installers -- generally source directories -- for your software. Also, stores the compressed archives ("tarballs") of your installers; useful if you want to reinstall later using different build options.


- ```local/share/lmodfiles``` - The standard place to store module files, which will allow you to dynamically add or remove locally installed applications from your environment.
You can create this structure with one command.


In my case, I have a directory where I keep all my local installs
```sh
$ echo $INSTALLS
/glade/p/work/abanihi/cy/installs
```
It's this directory that I will be using throughout this document.


You can create the structure above with one command.

```sh
$ mkdir -p $INSTALLS/local/src $INSTALLS/local/share/lmodfiles
```

## Installing Software/Packages

Now that you have your directory structure created, you can install your software. For demonstration purposes, I will install a local copy of ```GeoPandas```

### Step 1
- Get the source code onto the HPC filesystem in this case GLADE. The easiest thing to do is clone a GitHub repo or find a download link, copy it, and use the ```wget``` tool to download it on Cheyenne. I'll download this into ```$INSTALLS/local/src```:


```sh
$ cd $INSTALLS/local/src
$ git clone git@github.com:geopandas/geopandas.git
$ cd geopandas
```



### Step 2: Build it!

To build the module, I first create a temporary environment variable to aid in installation. I call it ```TEMP_INSTALL```.

```sh
$ export TEMP_INSTALL=${INSTALLS}/local/geopandas/0.2.1
```

I have specified a folder for the program (geopandas), and for the version (0.2.1).

Now, to be consistent with python installations, I am going to create a directory, whcih will contain the actual installation location.

```sh
$ mkdir -p $INSTALLS/local/geopandas/0.2.1/lib/python2.7/site-packages
```

- We need to add this path to PYTHONPATH so that Python can access it.


```sh
$ export PYTHONPATH=$INSTALLS/local/geopandas/0.2.1/lib/python2.7/site-packages/:$PYTHONPATH
```

### Step 3: Compile

To compile the module, we should switch to the GNU compilers. The system installation of Python was compiled with the GNU compilers, and this will help avoid any unnecessary complications. We will also load the Python module, if it hasn't already been loaded.

```sh
$ module swap intel gnu
$ module load python
```

Now, build it. This step may vary a bit, depending on the module you are compiling. You can execute ```$ python setup.py --help``` to see what options are available. Since we are overriding the install path to one that we can write to, and that fits our management plan, we need to use the ```--prefix``` option.


```sh
$ GEOS_CONFIG=/glade/u/apps/ch/opt/geos/3.6.1/gnu/6.2.0/bin/geos-config python setup.py install --prefix=$TEMP_INSTALL
``` 


### Step 4: Make a module
This is the most complicated option, but it is also the most flexible, as you can have multiple versions of this particular software installed, and specify at run-time which one to use. This is incredibly useful if a major feature changes that would break old code, for example.

Modules allow you to dynamically alter your environment to define environment variables and bring executables, libraries, and other features into your shell's search paths.

In the case of GeoPandas example, you should create the directory $INSTALLS/local/share/lmodfiles/geopandas and create a module file within that directory named 0.2.1.lua.

I will be using the filename 0.2.1.lua ("version".lua). A simple Lua module for GeoPandas installation would be:

```lua

-- Local Variables
local name = "geopandas"
local version= "0.2.1"

-- Locate Home Directory
local homedir = os.getenv("INSTALLS")
local root = pathJoin(homedir, "local", name, version)

-- Set Basic Paths
prepend_path("PYTHONPATH", pathJoin(root, "lib/python2.7/site-packages"))
prepend_path(root, "bin")

```


## Initializing Modules

Any module file you create should be saved into your local lmodfiles directory (```$INSTALLS/local/share/lmodfiles```). To prepare for future software installations, create a subdirectory within lmodfiles named after your software and add one module file to that directory for each version of the software installed.

To make this module usable, you need to tell lmod where to look for it. You can do this by issuing the command

```sh
$ module use $INSTALLS/local/share/lmodfiles
$ module load geopandas
```

**NOTE:** 

```module use $INSTALLS/local/share/lmodfiles``` and ```module load "software_name"``` needs to be entered into the command line every time you enter a new session on the system.
