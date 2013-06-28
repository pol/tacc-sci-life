Summary:    maker -- a portable and easy to configure genome annotation pipeline
Name:       maker
Version:    2.28b
Release:    1
License:    GNU General Public License
Group: Applications/Life Sciences
Source:     %{name}-%{version}.tar.gz
Packager:   TACC - jiao@tacc.utexas.edu
# This is the actual installation directory - Careful
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
%include ../system-defines.inc
# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define PNAME maker

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
MAKER is a portable and easily configurable genome annotation pipeline. It's purpose is to allow smaller eukaryotic and prokaryotic genome projects to independently annotate their genomes and to create genome databases. MAKER identifies repeats, aligns ESTs and proteins to a genome, produces ab-initio gene predictions and automatically synthesizes these data into gene annotations having evidence-based quality values. 
#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define MODULE_VAR TACC_MAKER

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/***
%setup -n %{name}-%{version}

%build   
%install
%include ../system-load.inc          
    
# Load additional modules here (as needed)
module purge 
module load TACC
module swap mvapich2 openmpi

cd src
perl Build.PL << EOF
y
/opt/apps/intel11_1/openmpi/1.4.3/bin/mpicc
/opt/apps/intel11_1/openmpi/1.4.3/include
EOF
./Build installdeps << EOF
Y  
yes

yes
yes
yes
yes
yes
yes
yes
yes
yes
yes
y
yes
yes
a
n
yes
Y
EOF

./Build installexes << EOF
Y
nasridine
ylt993
EOF

./Build install

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with cmake.
This module makes available the openbabel executable. Documentation for %{name} is available online at the publisher\'s website: http://irs.inms.nrc.ca/software/egsnrc/egsnrc.html

Version %{version}
]])

whatis("Name: maker")
whatis("Version: %{version}")
whatis("Category: Biology, sequencing")
whatis("Keywords:  Genome, Sequencing, Annotation")
whatis("Description: Maker - a portable and easily configurable genome annotation pipeline.") 
whatis("http://www.yandell-lab.org/software/maker.html")

prepend_path("PATH",              "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN", "%{INSTALL_DIR}/bin")
prepend_path("LD_PRELOAD",              "/opt/apps/intel11_1/openmpi/1.4.3/lib/libmpi.so")
setenv ( "OMPI_MCA_mpi_warn_on_fork",    "0")

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

