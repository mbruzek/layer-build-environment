# Overview

This charm clones a repository and builds it so the binaries can be copied off
and used in other CI steps.

# Usage

Step by step instructions on using the charm:

```bash
juju deploy build-environment
juju set build-environment install-repo=https://github.com/mbruzek/install-repo
juju set build-environment build-repo=https://github.com/kubernetes/kubernetes
juju set build-environment output-files=hyperkube,kubectl
```

You can then use the `juju scp` command to download the built binary files.

# Configuration

#### install-repo
The repository that holds the preinstallation files to run that will set up the
build environment

#### build-repo
The repository to build.

#### output-files
The list of output files that will be built by the build-environment. Copy 
these files out of the image.

# build-environment Contact Information

Contact Matthew.Bruzek@canonical.com for more information on this project.
