Summary:    Trinity De novo RNA-Seq Assembler
Name:       trinityrnaseq
Version:    r20140717
Release:    1
License:    BSD
Vendor:     Broad Institute
Group: Applications/Life Sciences
Source:     %{name}_%{version}.tar.gz
Packager:   TACC - gzynda@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# This will define the correct _topdir and turn of building a debug package
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define PNAME %{name}
%define MODULE_VAR TACC_TRINITY

# Turn off dependency checking. Trinity bundles so much that it's 
# frankly preposterous to do this
AutoReqProv: no

%description
Trinity, developed at the Broad Institute and the Hebrew University of Jerusalem, represents a novel method for the efficient and robust de novo reconstruction of transcriptomes from RNA-seq data. Trinity combines three independent software modules: Inchworm, Chrysalis, and Butterfly, applied sequentially to process large volumes of RNA-seq reads. Trinity partitions the sequence data into many individual de Bruijn graphs, each representing the transcriptional complexity at at a given gene or locus, and then processes each graph independently to extract full-length splicing isoforms and to tease apart transcripts derived from paralogous genes.

## PREP
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
%setup -n %{name}_%{version}

%build
%include ../system-load.inc
module purge
module load TACC
if [[ `hostname` == *.stampede.tacc.utexas.edu ]]
then
	module load intel/14.0.1.106
	make inchworm_target TRINITY_COMPILER=intel INCHWORM_CONFIGURE_FLAGS='CXXFLAGS="-mkl -rpath" CXX=icpc'
	make chrysalis_target TRINITY_COMPILER=intel SYS_OPT="-mkl -rpath"
	module swap intel gcc/4.7.1
	make plugins LDFLAGS="-lpthread -all-static -rpath"
	module swap gcc intel/14.0.1.106
	make all
else
	module load intel
	make inchworm_target TRINITY_COMPILER=intel INCHWORM_CONFIGURE_FLAGS='CXXFLAGS="-rpath" CXX=icpc'
	make chrysalis_target TRINITY_COMPILER=intel SYS_OPT="-rpath"
	module swap intel gcc/4.7.1
	make plugins LDFLAGS="-lpthread -all-static -rpath"
	module swap gcc intel
	make all
fi

%install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
rm -rf Inchworm/src
rm trinity-plugins/rsem-1.2.15/*.h trinity-plugins/rsem-1.2.15/*.cpp
rm -rf trinity-plugins/jellyfish/jellyfish
rm -rf trinity-plugins/jellyfish/lib
rm -rf Chrysalis/obj
find . -name *.tar.gz | xargs -n 1 rm
cp -r * $RPM_BUILD_ROOT/%{INSTALL_DIR}/
chmod -R a+rX $RPM_BUILD_ROOT/%{INSTALL_DIR}

##################################################
#	Module Section
##################################################
# ADD ALL MODULE STUFF HERE
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR, %{MODULE_VAR}_BUTTERFLY, %{MODULE_VAR}_CHRYSALIS, %{MODULE_VAR}_INCHWORM and %{MODULE_VAR}_INCHWORM_BIN for the location of the %{PNAME} distribution.

Please refer to http://trinityrnaseq.sourceforge.net/#running_trinity for help running trinity.

BioITeam also provides a script for efficient job submission - %{MODULE_VAR}_SUBMIT
	%{MODULE_VAR}_SUBMIT -h

Version %{version}
]])
whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, transcriptomics")
whatis("Keywords: Biology, Assembly, RNAseq, Transcriptome")
whatis("URL: http://trinityrnaseq.sourceforge.net/")
whatis("Description: Package for RNA-Seq de novo Assembly")

prepend_path("PATH"       	, "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_DIR"	, "%{INSTALL_DIR}/")
setenv("%{MODULE_VAR}_SUBMIT"	, "/corral-repl/utexas/BioITeam/bin/assemble_trinity")
setenv("%{MODULE_VAR}_BUTTERFLY", "%{INSTALL_DIR}/Butterfly")
setenv("%{MODULE_VAR}_CHRYSALIS", "%{INSTALL_DIR}/Chrysalis")
setenv("%{MODULE_VAR}_INCHWORM"	, "%{INSTALL_DIR}/Inchworm")
setenv("%{MODULE_VAR}_INCHWORM_BIN", "%{INSTALL_DIR}/Inchworm/bin")
setenv("%{MODULE_VAR}_UTIL"	, "%{INSTALL_DIR}/util")
setenv("%{MODULE_VAR}_PLUGINS"	, "%{INSTALL_DIR}/trinity-plugins")
EOF

if [[ `hostname` == *.stampede.tacc.utexas.edu ]]
then
	cat >> $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
	setenv("MKL_MIC_ENABLE"	, "1")
	EOF
fi

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
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
