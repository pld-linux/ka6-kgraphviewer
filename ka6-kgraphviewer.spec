#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	6.8
%define		qtver		6.8
%define		kaname		kgraphviewer
Summary:	Graphviz DOT graph file viewer
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	0975c8a6c5d018ab505e1906649dc9af
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	graphviz-devel >= 2.30.0
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KGraphViewer is a Graphviz DOT graph file viewer.

%description -l pl.UTF-8
Przeglądarka plików DOT Graphiza.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/kgraphviewer
%ghost %{_libdir}/libkgraphviewer.so.0
%{_libdir}/libkgraphviewer.so.*.*
%{_libdir}/qt6/plugins/kf6/parts/kgraphviewerpart.so
%{_desktopdir}/org.kde.kgraphviewer.desktop
%{_datadir}/config.kcfg/kgraphviewer_partsettings.kcfg
%{_datadir}/config.kcfg/kgraphviewersettings.kcfg
%{_iconsdir}/hicolor/16x16/apps/kgraphviewer.png
%{_iconsdir}/hicolor/32x32/apps/kgraphviewer.png
%{_datadir}/metainfo/org.kde.kgraphviewer.appdata.xml
%{_datadir}/qlogging-categories6/kgraphviewer.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/kgraphviewer
%{_libdir}/cmake/KGraphViewerPart
%{_libdir}/libkgraphviewer.so
