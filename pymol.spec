%define name 	pymol
%define version 1.0
%define release %mkrel 5

Summary: 	PyMOL Molecular Graphics System
Name: 		%name
Version: 	%version
Release: 	%release
License: 	Python license
Group: 		Sciences/Chemistry
URL: 		http://www.pymol.org
Source: 	%name-%version.tar.bz2
Source1:	%name.png
BuildRoot: 	%_tmppath/%name-root
Requires: 	python python-numeric tcl tk tkinter Pmw tcsh
BuildRequires: 	python-devel python-numeric-devel tcl tk
BuildRequires:	png-devel MesaGLU-devel libmesaglut-devel
BuildRequires:	freetype2-devel ImageMagick

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
python ./setup.py build

%install
python ./setup.py install --root=%buildroot

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R scripts data %buildroot%_datadir/%{name}

mkdir -p %{buildroot}%{_bindir}
cat <<EOF >%{buildroot}%{_bindir}/%{name}
export PYMOL_DATA=/usr/share/pymol/data
export PYMOL_SCRIPTS=/usr/share/pymol/scripts

python %{python_sitearch}/pymol/__init__.py
EOF

# menu
install -d $RPM_BUILD_ROOT%{_datadir}/applications
cat << EOF > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=PyMol
Comment=Python controlled molecular graphics
Exec=pymol
Icon=pymol
Type=Application
Categories=Chemistry;Science;
EOF

mkdir -p %{buildroot}{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert %SOURCE1 -resize 16x16 %buildroot%{_miconsdir}/%{name}.png
convert %SOURCE1 -resize 32x32 %buildroot%{_iconsdir}/%{name}.png
cp %SOURCE1 %buildroot%{_liconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr (-,root,root)
%doc ChangeLog DEVELOPERS LICENSE README
%doc examples
%python_sitearch/*
%_datadir/%name
%attr(0755,root,root) %_bindir/%name
%_datadir/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
