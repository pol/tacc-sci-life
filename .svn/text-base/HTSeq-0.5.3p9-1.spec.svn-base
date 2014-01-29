Summary:    HTSeq
Name:       htseq
Version:    0.5.3p9
Release:    1
License:    GPL
Vendor:     EMBL
Group: Applications/Life Sciences
Source:     HTSeq-%{version}.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir
%include ../system-defines.inc
%include rpm-dir.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define PNAME htseq

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: Provides infrastructure to process data from high-throughput sequencing assays
# Group:   Applications/Biology

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
HTSeq is a Python package that provides infrastructure to process data from high-throughput sequencing assays

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_HTSEQ

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source
%setup -n HTSeq-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
%include ../system-load.inc

module load python

python setup.py build
mkdir -p $PWD/lib/python2.7/site-packages/
export PYTHONPATH=$PWD/lib/python2.7/site-packages/:$PYTHONPATH
python setup.py install --prefix=$PWD

cp -r lib bin doc LICENSE VERSION README $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{PNAME}, which depends on python and numpy.
To call this function, use "import HTSeq" within python. 
Documentation for %{PNAME} is available online at the publisher website: http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PYTHONPATH has been prepended to include the HTSeq library.

Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, High-throughput Sequencing")
whatis("Description: HTSeq - Analysing high-throughput sequencing data with Python")
whatis("URL: https://pypi.python.org/pypi/HTSeq")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PYTHONPATH"       ,"%{INSTALL_DIR}/lib/python2.7/site-packages/")

prereq("python")

EOF

#--------------
#  Version file.
#--------------

cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF



#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

