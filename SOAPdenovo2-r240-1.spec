Summary:    SOAP de novo 2 - Short Oligonucleotide Analysis Package
Name:       SOAPdenovo2
Version:    r240
Release:    1
License:    GPLv3
Vendor:     BGI
Group: Applications/Life Sciences
Source:     SOAPdenovo2-r240.tar.gz
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------

%include rpm-dir.inc
%include ../system-defines.inc

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_SOAPDENOVO2

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME %{name}
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_SOAPDENOVO2

%description
SOAPdenovo2, a short read de novo assembly tool, is a package for assembling short oligonucleotide into contigs and scaffolds.

## PREP
%prep
rm -rf $RPM_BUILD_ROOT

%setup -n %{PNAME}-%{version}

%build

%install

%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
module purge
module load TACC
module unload $TACC_FAMILY_COMPILER
module load gcc

make 

module unload python

cp -r SOAPdenovo-127mer SOAPdenovo-63mer $RPM_BUILD_ROOT/%{INSTALL_DIR}

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{PNAME}. SOAPdenovo2 resolves more repeat regions in contig assembly, increases coverage and length in scaffold construction, improves gap closing, and optimizes for large genome. 
To startup this program, use either SOAPdenovo-127mer or SOAPdenovo-63mer in the command line. 
Publication for %{PNAME} is available online at the publisher website: http://www.gigasciencejournal.com/content/1/1/18/
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PATH has been updated to include %{PNAME}.

Version %{version}
]])

whatis("Name: soapdenovo2")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Assembly")
whatis("Description: soapdenovo2 - novel short-read assembly method that can build a de novo draft assembly for the human-sized genomes")
whatis("URL: http://soap.genomics.org.cn/soapdenovo.html")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/SOAPdenovo-127mer")
prepend_path("PATH"       ,"%{INSTALL_DIR}/SOAPdenovo-63mer")

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

