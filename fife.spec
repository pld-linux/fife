#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Flexible Isometric Free Engine
Summary(pl.UTF-8):	Flexible Isometric Free Engine - elastyczny, wolnodostępny silnik izometryczny
Name:		fife
Version:	0.3.5
Release:	6
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/fife/%{name}_%{version}.tar.gz
# Source0-md5:	11ba50b34239535a270d442466632ef7
Patch0:		%{name}-extra_libs.patch
Patch1:		%{name}-glee.patch
URL:		http://fifengine.net/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	boost-devel
BuildRequires:	guichan-devel >= 0.8.2
BuildRequires:	guichan-opengl-devel >= 0.8.2
BuildRequires:	guichan-sdl-devel >= 0.8.2
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	scons >= 2.0
BuildRequires:	swig-python
BuildRequires:	tinyxml-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FIFE is a cross platform 2D game creation framework written in C++
with Python bindings. It's designed to be flexible enough to support a
wide variety of 2D game types but specializes in 2D isometric type
views.

%description -l pl.UTF-8
FIFE to wieloplatformowy szkielet do tworzenia gier 2D napisany w C++
z wiązaniami do Pythona. Jest zaprojektowany jako wystarczająco
elastyczny do obsługi wielu rodzajów gier 2D, ale specjalizuje się w
widokach 2D typu izometrycznego.

%package devel
Summary:	Header files for FIFE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FIFE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for FIFE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FIFE.

%package static
Summary:	Static FIFE library
Summary(pl.UTF-8):	Statyczna biblioteka FIFE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FIFE library.

%description static -l pl.UTF-8
Statyczna biblioteka FIFE.

%package -n python-%{name}
Summary:	Flexible Isometric Free Engine Python Module
Summary(pl.UTF-8):	Moduł Pythona do silnika FIFE (Flexible Isometric Free Engine)
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

%description -n python-%{name}
FIFE is a cross platform 2D game creation framework written in C++
with Python bindings. It's designed to be flexible enough to support a
wide variety of 2D game types but specializes in 2D isometric type
views.

This package contains Python module.

%description -n python-%{name} -l pl.UTF-8
FIFE to wieloplatformowy szkielet do tworzenia gier 2D napisany w C++
z wiązaniami do Pythona. Jest zaprojektowany jako wystarczająco
elastyczny do obsługi wielu rodzajów gier 2D, ale specjalizuje się w
widokach 2D typu izometrycznego.

Ten pakiet zawiera moduł Pythona.

%prep
%setup -qn %{name}_%{version}
%patch0 -p1
%patch1 -p1

%build
# force pre C++11 standard, code uses std::make_pair in a way incompatible with rvalue refs
CXXFLAGS="%{rpmcxxflags} -std=c++03"
%scons -j1 fife-shared fife-python \
	%{?with_static_libs:fife-static} \
	--lib-dir=%{_libdir} \
	--prefix=%{_prefix} \
	--python-prefix=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT

CXXFLAGS="%{rpmcxxflags} -std=c++03"
%scons -j1 install-shared install-python install-dev \
	%{?with_static_libs:install-static} \
	--lib-dir=%{_libdir} \
	--prefix=%{_prefix} \
	--python-prefix=%{py_sitedir} \
	--install-sandbox=$RPM_BUILD_ROOT

SAVED_PWD=$PWD
cd $RPM_BUILD_ROOT%{_libdir}
ln -s libfife.so.0.?.? libfife.so.0
ln -s libfife.so.0.?.? libfife.so
cd $SAVED_PWD

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%attr(755,root,root) %{_libdir}/libfife.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfife.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfife.so
%{_includedir}/%{name}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfife.a
%endif

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/_fife.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/extensions
