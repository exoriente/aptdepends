# apt-depends

`apt-depends` allows you to keep track of manually installed `deb` packages on your system.
This is especially useful when installing dependencies for software that is not packaged as a `deb` itself.
With `apt-depends` you no longer need to install those packages independently (marked as "manual").
You can easily create and install a metapackage that has the required dependencies.

## Example of use

```bash
$ apt-depends install pyenv-dependencies build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```

The above command will create an empty metapackage with the name `pyenv-dependencies` and install it.
All words after the new package name are the names of packages `pyenv-dependencies` will depend on
and that will be automatically installed by as well, if they are not present on the system already.

This results in:

- A single new package `pyenv-dependencies` that is marked as manually installed
- All other packages will be marked as automatically installed

In this example the packages mentioned are required to run the excellent python development tool `pyenv` ([link](https://github.com/pyenv/pyenv)) on Ubuntu.
`pyenv` is not available by default as a `deb` package.
Installing the packages using `apt-get` ot `apt` will also do the job, but will mark each package as manually installed,
making it harder to identify and remove them if you don't need them anymore.

## Current status

`apt-depends` is not yet working. It's a small project I'm building in my off-hours to learn more python
and to make something I would use myself.
