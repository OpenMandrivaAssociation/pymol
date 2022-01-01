%define _empty_manifest_terminate_build 0
#global _disable_ld_no_undefined %nil

%define oname PyMol
%define name %(echo %oname | tr [:upper:] [:lower:])

Summary:	Molecular Graphics System
Name:		pymol
Version:	2.5.0
Release:	1
# Which files use following license:
# BSD: main license of open source PyMOL and some plugins
# MIT: modules/pymol_web/examples/sample13/jquery.js
# Bitstream Vera: layer1/FontTTF.h
# OFL: layer1/FontTTF2.h
License:	MIT and BSD and Bitstream Vera and OFL
Group:		Sciences/Chemistry
URL:		http://www.pymol.org
Source0:	https://github.com/schrodinger/pymol-open-source/archive/v%{version}/%{name}-open-source-%{version}.tar.gz
Source1:	%{name}.png
#Patch0:		add_missing_math_linker.patch
# (upstream) https://github.com/schrodinger/pymol-open-source/issues/186
Patch100: %{name}-2.5.0-commit_a37118f6780dd9f76cf0a89155801e54cdb2e14d.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
#BuildRequires: catch-devel
BuildRequires:	mmtf-cpp-devel
BuildRequires:	gomp-devel
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glm)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(msgpack)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(pyside2)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(simplejson)
BuildRequires:	python3dist(numpy)
# Qt interface
BuildRequires: pkgconfig(freeglut)
BuildRequires: pkgconfig(pyside2)
BuildRequires: python3dist(pyqt5)

#Requires:	apbs
Requires:	chemical-mime-data
Requires:	python-numpy
Requires:	mmtf-cpp
Requires:	Pmw
Requires:	tkinter
# Qt interface
Requires:	python
Requires:	python-qt5
# tk interface
Requires:	tcl
Requires:	tk
Requires:	tkinter
Requires:	tcsh

%description
PyMOL is a molecular graphics system with an embedded Python interpreter 
designed for real-time visualization and rapid generation of high-quality 
molecular graphics images and animations. It is fully extensible and 
available free to everyone via the "Python" license.  Although a newcomer 
to the field, PyMOL can already be used to generate stunning images and 
animations with unprecedented ease. It can also perform many other 
valuable tasks (such as editing PDB files) to assist you in your research.

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

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-open-source-%{version}
ln -sr modules/web modules/pymol_web

%build
%setup_compile_flags
export CPPFLAGS="%{optflags}"
# clang fails with 'unterminated function-like macro invocation' error
export CC=gcc
export CXX=g++
#py3_build --use-msgpackc=c++11 --use-openmp=yes --jobs `/usr/bin/getconf _NPROCESSORS_ONLN`
%{__python} ./setup.py build --use-msgpackc=c++11 --use-openmp=yes --jobs `/usr/bin/getconf _NPROCESSORS_ONLN`

%install
#py3_install -- --use-msgpackc=c++11 --use-openmp=yes --pymol-path=%{python3_sitearch}/%{name}
%{__python} ./setup.py install --use-msgpackc=c++11 --use-openmp=yes --pymol-path=%{python3_sitearch}/%{name} --root=%{buildroot}

# launcher
install -dm 0755 %{buildroot}%{_bindir}/
cat <<EOF >%{buildroot}%{_bindir}/%{name}
export PYMOL_DATA=/usr/share/pymol/data
#export PYMOL_SCRIPTS=/usr/share/pymol/scripts
export PYMOL_PATH=/usr/bin/pymol

%{__python} %{python_sitearch}/pymol/__init__.py
EOF

install -dm 0755  %{buildroot}%{_datadir}/%{name}/
cp -R data %buildroot%_datadir/%{name}

# .desktop
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=%{oname}
Comment=Python controlled molecular graphics
Exec=%{name}
Icon=%{name}
Type=Application
Categories=Chemistry;Science;Education;
EOF

# icons
install -dm 0755 %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert %{SOURCE1} -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{SOURCE1} -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
install -pm 0644 %{SOURCE1} %{buildroot}%{_liconsdir}/%{name}.png

