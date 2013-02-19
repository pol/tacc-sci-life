Summary:    plink - Whole genome association analysis toolset
Name:       plink
Version:    1.07
Release:    2
License:    GPLv2
Vendor:     Shaun Purcell
Group: Applications/Life Sciences
Source: http://pngu.mgh.harvard.edu/~purcell/plink/dist/plink-1.07-src.zip
#Source:     %{name}-%{version}-src.zip
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
%include rpm-dir.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME plink
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_PLINK

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
PLINK is a free, open-source whole genome association analysis toolset, designed to perform a range of basic, large-scale analyses in a computationally efficient manner. 

The focus of PLINK is purely on analysis of genotype/phenotype data, so there is no support for steps prior to this (e.g. study design and planning, generating genotype or CNV calls from raw data). Through integration with gPLINK and Haploview, there is some support for the subsequent visualization, annotation and storage of results.
PLINK (one syllable) is being developed by Shaun Purcell at the Center for Human Genetic Research (CHGR), Massachusetts General Hospital (MGH), and the Broad Institute of Harvard & MIT, with the support of others

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##
%setup -n %{name}-%{version}-src

##
## BUILD
##

%build

##
## INSTALL
##
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

# Load correct compiler
# %include compiler-load.inc
# Load correct mpi stack
# %include mpi-load.inc
# %include mpi-env-vars.inc
# Load additional modules here (as needed)

module purge
module load TACC
module load mkl

#make CC=icc CXX=icpc WITH_ZLIB=/usr/lib64/libz.so WITH_WEBCHECK=0
make 'LIBS=-ldl' 'WITH_ZLIB=/usr/lib64/libz.so' WITH_WEBCHECK=0
make CXXFLAGS='-L /usr/lib -L/usr/lib64 -lz' 'WITH_WEBCHECK=0'

cp ./plink ./README.txt $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with icc.

This module makes available the plink executable. Documentation for %{name} is available online at the publisher's website: http://pngu.mgh.harvard.edu/~purcell/plink/
The plink executable can be found in %{MODULE_VAR}_DIR

Version %{version}
]])

whatis("Name: plink")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Alignment, Sequencing, Genetics, GWAS")
whatis("Description: plink - Whole genome association analysis toolset")
whatis("URL: http://pngu.mgh.harvard.edu/~purcell/plink/")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")

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

