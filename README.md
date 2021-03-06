katipo
======
katipo is a tool to facilate working together on multiple git projects that are interrelated. 
It is somewhat inspired by repo tool but uses merges rather than rebasing and works with
github pull requests rather than the more heavyweight reviewing tools repo uses. Additionally, it is easy to create new branches across multiple repos.

The general syntax is similar to git:
    katipo command [options]
    
The initial release supports the following commands.

    katipo clone giturl assemblyfile [working location]

This is the first katipo command needed to initialize a working copy of the tree. The `giturl`
is a pointer to a git repo of assembly files (descriptions of a working tree - see below)
and assembly file is the specific file inside that repo to get instructions from.

Running this command will create a `.katipo` folder in the working location and initialize git repos
according to the instructions of the assemblyfile. All other commands will search for a `.katipo`
folder to use as the root.

If not specified, working location defaults to cwd/basename of assembly file (similar to git clone).

    katipo perrepo cmd [additional parameters to cmd]
  
Run cmd in each repo which katipo knows about.

    katipo checkout [-t] branchname

Checkout `branchname` in every repo if it exists, if not then fallback to `master` branch. `-t` - make
it a tracking branch.

    katipo test

Run `test` in every repo which is a test repo. test must be executable.

Python virtual environment setup.
---------------
Katipo contains support for setting up your python environment (using virtualenv).
It only works if virtualenv is installed.

     katipo virtualenv [--python pythonexe]

will construct a virtualenv in root of the working folder/.env . It will populate the
virtualenv with the concatenated version of all requirements.txt files found in the base
of every repo (and readline if on OS X to work around the buggy readline installed by 
default). Additionally, it will modify the virtualenv script to add the base of every
repo the PYTHONPATH.

Once this command has run then activate the environment by running.

	source .env/bin/activate

in the base of the working folder.


Installation
--------------
To install or upgrade katipo use pip.

    $ (sudo) pip install -U git+http://github.com/braincorp/katipo.git  

Note that the first time you run this command it may take awhile as it will automatically
install dependencies for katipo.

Assembly files
--------------
Assembly files are JSON files which describe the intended working copy layout. They are just a 
list of repos.

The look like:

    {
    "version" : 1
    "repos": [
        {"giturl" : "git@github.com/braincorp/test.git",
            "path":"test",
            "test"=true
    ]
	# Comment Line - must be with a # in the first column
	# Optional python virtualenv parameters 
	# prompt - virtualenv prompt shown when environment active.
	"virtualenv" : { "prompt" : "katipo" }
	
	# Base files
	"base_files" : {
		 "use_repo.sh" :
			{ "content" : "Source this script to setup the environment for this package"
			}
		}
    }


`version` describes version of the assembly file. Right now should be always `1`

`path` is optional and indicates the location where this repo will be located in the 
working copy.

`test` is optional and indicates if changes are tested against this repo or if it is just
a dependency. It defaults to `false`.
