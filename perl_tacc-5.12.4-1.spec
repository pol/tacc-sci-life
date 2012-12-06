
Summary: Perl for TACC Systems
Name:  perl_tacc
Version: 5.12.4
Release: 1
License: GPL
Group: Development/Languages
Packager: jlockman@tacc.utexas.edu
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%include rpm-dir.inc

# NOTE: 
# I built all rpms for Perl seperately and installed into a tmpfs
# tarred it all up and this will dump the contents into the correct
# location

%define PerlSrc perl_tacc-%{version}.tar.gz

%define APPS /opt/apps
%define MODULES modulefiles
%define version_short 5.12


%define INSTALL_DIR %{APPS}/perl/%{version_short}
%define MODULE_DIR %{APPS}/%{MODULES}/perl
%define SUBMODULES %{APPS}/perl/%{MODULES}

%description
Perl programming language
%prep

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd $RPM_BUILD_ROOT/%{INSTALL_DIR}
cd ..
tar xvfz $RPM_SOURCE_DIR/%{PerlSrc}
#cd -


##
## BUILD
##
%build

###
### INSTALL
###


%install

mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version_short} << 'EOF'
#%Module1.0#####################################################################
##
## Intel compilers
##
proc ModulesHelp { } {

puts stderr ""
puts stderr "The Perl module enables the Perl compiler"
puts stderr "and updates the \$PATH, \$LD_LIBRARY_PATH, and "
puts stderr "\$MANPATH environment variables to access the compiler binaries,"
puts stderr "libraries, and available man pages, respectively."
puts stderr ""
puts stderr "If you would like to install Perl modules in your home directory"
puts stderr "you wil need to set the PERL5LIB variable"
puts stderr " "
puts stderr "\nVersion %{version_short}\n"

}

module-whatis "Name: Perl"
module-whatis "Version: %{version_short}"
module-whatis "Category: compiler, runtime support"
module-whatis "Keywords: System, Compiler"
module-whatis "Description: Perl"
module-whatis "URL: http://perl.org"

# for Tcl script use only

set     version         	%{version_short}

prepend-path    PATH            %{INSTALL_DIR}/bin/
prepend-path    MANPATH         %{INSTALL_DIR}/man/
prepend-path    LD_LIBRARY_PATH %{INSTALL_DIR}/lib64/perl5
prepend-path    MODULEPATH      %{SUBMODULES}

EOF

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version_short} << 'EOF'
#%Module1.0#################################################
##
## Version file for %{version_short} intel compiler.
## File default is copied to .version in modulefiles directory. 
##
 
set     ModulesVersion     "%{version_short}"

EOF

##
## FILES
##
%files
%defattr(755,root,root)
%{INSTALL_DIR}
%{MODULE_DIR}

##
## CLEAN
##
%clean
rm -rf $RPM_BUILD_ROOT
