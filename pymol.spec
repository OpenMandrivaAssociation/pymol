%define name 	pymol
%define version 1.0
%define release %mkrel 1

Summary: 	PyMOL Molecular Graphics System
Name: 		%name
Version: 	%version
Release: 	%release
License: 	Python license
Group: 		Sciences/Chemistry
URL: 		http://www.pymol.org
Source: 	%name-%version.tar.bz2
BuildRoot: 	%_tmppath/%name-root
Requires: 	python python-numeric tcl tk tkinter Pmw tcsh
BuildRequires: 	python-devel python-numeric-devel tcl tk
BuildRequires:	png-devel MesaGLU-devel libmesaglut-devel

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

%build
%configure2_5x
%make

%install
%makeinstall_std

mkdir -p %buildroot%_bindir
ln -s ../../%python_sitearch/pymol %buildroot%_bindir/pymol

# menu
install -d $RPM_BUILD_ROOT%{_datadir}/applications
cat << EOF > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=PyMol
Comment=Python controlled molecular graphics
Exec=pymol
Icon=pymol
Type=Application
Categories=Chemistry;Science
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
%doc doc
%doc examples
%python_sitearch/*
%_datadir/%name
%attr(0755,root,root) %_bindir/%name
%_datadir/applications/*.desktop
