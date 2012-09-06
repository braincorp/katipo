katipo
======
katipo is a tool to facilate working together on multiple git projects that are interrelated. 
It is somewhat inspired by repo tool but uses merges rather than rebasing and works with
github pull requests rather than the more heavyweight reviewing tools repo uses.

The general syntax is similar to git:
    katipo command [options]
    
The initial release supports the following commands.

    katipo clone giturl assemblyfile

This is the first katipo command needed to initialize a working copy of the tree. The `giturl`
is a pointer to a git repo of assembly files (descriptions of a working tree - see below)
and assembly file is the specific file inside that repo to get instructions from.

Running this command will create a `.katipo` folder in the current folder and initialize git repos
according to the instructions of the assemblyfile. All other commands will search for a `.katipo`
folder to use as the root.

    katipo perrepo cmd [additional parameters to cmd]
  
Run cmd in each repo which katipo knows about.

    katipo checkout [-t] branchname

Checkout `branchname` in every repo if it exists, if not then fallback to `master` branch. `-t` - make
it a tracking branch.

    katipo test

Run `test.sh` in every repo which is a test repo.


Installation
--------------
The recommended method of installation at the moment (until it matures) is to clone
the Katipo repo.

    git clone git@github.com:braincorp/katipo.git

Then access the katipo command by running

    ./katipo/bin/katipo   

Note that the first time you run this command it may take awhile as it will automatically
install dependencies for katipo.

Assembly files
--------------
Assembly files are JSON files which describe the intended working copy layout. They are just a 
list of repos.

The look like:

    {
    "katipo_schema" : 1
    "repos": [
        {"giturl" : "git@github.com/braincorp/test.git",
            "path":"test",
            "test"=true
    ]
    }
    

`path` is optional and indicates the location where this repo will be located in the 
working copy.

`test` is optional and indicates if changes are tested against this repo or if it is just
a dependency. It defaults to `false`.

