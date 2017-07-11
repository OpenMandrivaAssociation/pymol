### Attention to anyone touching this package
### Please contact me prior to touching it since
### this is a scientific package with a license evolution
### since release 1.3 so we keep the old one for now, until 
### any status update.
### steletch@mandriva.com
%define _disable_lto 1
%define _disable_rebuild_configure 1
%define _disable_ld_no_undefined 1

Summary:	Molecular Graphics System
Name:		pymol
Version:	1.8.6.0
Release:	1
License:	Python license
Group:		Sciences/Chemistry
URL:		http://www.pymol.org
Source:		https://downloads.sourceforge.net/pymol/%{name}-v%{version}.tar.bz2
Source1:	%{name}.png
Patch0:		add_missing_math_linker.patch

BuildRequires:	imagemagick
BuildRequires:	python-numeric-devel
BuildRequires:	python-numpy-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(msgpack)
BuildRequires:	pkgconfig(python3)

Requires:	python
Requires:	python-numeric
Requires:	tcl
Requires:	tk
Requires:	tkinter
Requires:	Pmw
Requires:	tcsh

%description
PyMOL is a molecular graphics system with an embedded Python interpreter 
designed for real-time visualization and rapid generation of high-quality 
molecular graphics images and animations. It is fully extensible and 
available free to everyone via the "Python" license.  Although a newcomer 
to the field, PyMOL can already be used to generate stunning images and 
animations with unprecedented ease. It can also perform many other 
valuable tasks (such as editing PDB files) to assist you in your research.

%prep
%setup -q -n %{name}
%apply_patches

%build
export CFLAGS=-fno-lto
export CC=gcc
export CXX=g++
%{__python} ./setup.py build

%install
%{__python} ./setup.py install --root=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R scripts data %buildroot%_datadir/%{name}

mkdir -p %{buildroot}%{_bindir}
cat <<EOF >%{buildroot}%{_bindir}/%{name}
export PYMOL_DATA=/usr/share/pymol/data
export PYMOL_SCRIPTS=/usr/share/pymol/scripts
export PYMOL_PATH=/usr/bin/pymol

%{__python} %{python_sitearch}/pymol/__init__.py
EOF

# menu
install -d %{buildroot}%{_datadir}/applications
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=PyMol
Comment=Python controlled molecular graphics
Exec=pymol
Icon=pymol
Type=Application
Categories=Chemistry;Science;Education;
EOF

mkdir -p %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert %{SOURCE1} -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{SOURCE1} -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
cp %{SOURCE1} %{buildroot}%{_liconsdir}/%{name}.png

%files
%doc ChangeLog DEVELOPERS LICENSE README
%doc examples
%{python_sitearch}/*
%{_datadir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

