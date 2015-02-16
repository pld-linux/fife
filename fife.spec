#
# TODO:
#	- package apidocs
#
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Flexible Isometric Free Engine
Name:		fife
Version:	0.3.3r3
Release:	8
License:	LGPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/fife/%{name}_%{version}.tar.gz
# Source0-md5:	ee39612009e124263dc79d1f0fa7ca7c
Patch0:		%{name}-extra_libs.patch
URL:		http://fifengine.net/
BuildRequires:	OpenAL-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	boost-devel
BuildRequires:	guichan-devel
#BuildRequires:	guichan_opengl-devel
#BuildRequires:	guichan_sdl-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	python-devel >= 2.7
BuildRequires:	scons
BuildRequires:	swig-python
BuildRequires:	tinyxml-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FIFE is a cross platform 2D game creation framework written in C++
with Python bindings. It's designed to be flexible enough to support a
wide variety of 2D game types but specializes in 2D isometric type
views.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package -n python-%{name}
Summary:	Flexible Isometric Free Engine Python Module
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

%description -n python-%{name}
FIFE is a cross platform 2D game creation framework written in C++
with Python bindings. It's designed to be flexible enough to support a
wide variety of 2D game types but specializes in 2D isometric type
views.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API and internal documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -qn %{name}_%{version}
%patch0 -p1

%build
%scons -j1 fife-shared fife-python \
	%{?with_static_libs:fife-static} \
	--lib-dir=%{_libdir} \
	--prefix=%{_prefix} \
	--python-prefix=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT

%scons -j1 install-shared install-python install-dev \
	%{?with_static_libs:install-static} \
	--lib-dir=%{_libdir} \
	--prefix=%{_prefix} \
	--python-prefix=%{py_sitedir} \
	--install-sandbox=$RPM_BUILD_ROOT

SAVED_PWD=$PWD
cd $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}.so.0.?.? lib%{name}.so.0
ln -s lib%{name}.so.0.?.? lib%{name}.so
cd $SAVED_PWD

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}

%files -n python-%{name}
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py*
%{py_sitedir}/%{name}/extensions

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib%{name}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc apidocs/*
%endif
