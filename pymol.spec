%define name 	pymol
%define version 0.98
%define release 1mdk

%define pyver	2.4

Summary: 	PyMOL Molecular Graphics System
Name: 		%name
Version: 	%version
Release: 	%release
License: 	Python license
Group: 		Sciences/Chemistry
URL: 		http://www.pymol.org
Source0: 	%name-0_98-src.tar.bz2
#Patch:		%name-0.90-setup.patch.bz2
BuildRoot: 	%_tmppath/%name-root
Requires: 	python python-numeric tcl tk tkinter Pmw tcsh
BuildRequires: 	python-devel python-numeric-devel tcl tk
BuildRequires:	png-devel MesaGLU-devel libMesaglut-devel

%description
PyMOL is a molecular graphics system with an embedded Python interpreter 
designed for real-time visualization and rapid generation of high-quality 
molecular graphics images and animations. It is fully extensible and 
available free to everyone via the "Python" license.  Although a newcomer 
to the field, PyMOL can already be used to generate stunning images and 
animations with unprecedented ease. It can also perform many other 
valuable tasks (such as editing PDB files) to assist you in your research.

%prep
%setup -q
#%patch

%install
python setup.py install --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_bindir
echo '#!/bin/sh' > $RPM_BUILD_ROOT/%_bindir/pymol
echo '%{_bindir}/python %{_libdir}/python%{pyver}/site-packages/pymol/__init__.py $*' >> $RPM_BUILD_ROOT/%_bindir/pymol
chmod 755 $RPM_BUILD_ROOT/%_bindir/pymol

# menu
install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="pymol"\
needs="x11"\
section="More Applications/Sciences/Chemistry"\
title="PyMol"\
icon="chemistry_section.png"\
longtitle="Python controlled molecular graphics"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files
%defattr (-,root,root)
%doc CHANGES DEVELOPERS LICENSE README
%_libdir/python*/site-packages/*
%_bindir/%name
%_menudir/%name

