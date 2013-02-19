# $Id$

Summary:    Markov Chain based haplotyper
Name:       mach
Version:    1.0.18
Release:    2
License:    Unknown
Group: Applications/Life Sciences/genetics
Source:     %{name}.%{version}.source.tgz
Packager:   TACC - vaughn@tacc.utexas.edu
# This is the actual installation directory - Careful
#BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%define debug_package %{nil}
%include rpm-dir.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME mach

%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%define MODULE_VAR TACC_MACH

# Allow for creation of multiple packages with this spec file
# Any tags right after this line apply only to the subpackage
# Summary and Group are required.
# %package -n %{name}-%{comp_fam_ver}
# Summary: HMMER biosequence analysis using profile hidden Markov models
# Group: Applications/Life Sciences

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description

##
## PREP
##
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -c -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/xsede/modulefiles:/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
module load TACC
#module swap $TACC_FAMILY_COMPILER gcc/4.7.1

# This should help us resolve location of zlib
# Will need to move if we install a system-level zlib
#
make all

# May want to revisit placement of this, or alternative implementation
export DONT_STRIP=1

cp executables/mach1 executables/thunder $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
MACH 1.0 is a Markov Chain based haplotyper. It can resolve long haplotypes or infer 
missing genotypes in samples of unrelated individuals. The current version is a pre-release.
Documentation for %{name} is available - http://www.sph.umich.edu/csg/abecasis/MACH
The executable can be found in %{MODULE_VAR}_DIR

This module provides the mach1 and thunder executables.

Version %{version}
]])

whatis("Name: MACH")
whatis("Version: %{version}")
whatis("Category: Computational biology, genetics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing, Genetics, GWAS, Imputation")
whatis("Description: Markov Chain based haplotyper")
whatis("URL: http://www.sph.umich.edu/csg/abecasis/MACH")

prepend_path("PATH",              "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")

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

