%define		shortname	taskd
Summary:	Taskserver is a sync server for Taskwarrior and related products
Name:		taskserver
Version:	1.0.0
Release:	1
License:	MIT
Group:		Applications
Source0:	http://www.taskwarrior.org/download/%{shortname}-%{version}.tar.gz
# Source0-md5:	1cead23539e36d5623cb3ca1225072c0
URL:		http://taskwarrior.org/
BuildRequires:	cmake
BuildRequires:	gnutls-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Taskserver is a sync server for Taskwarrior and related products.

%prep
%setup -q -n %{shortname}-%{version}

%build
%cmake

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{shortname}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{shortname}
%attr(755,root,root) %{_bindir}/taskdctl
%{_mandir}/man1/%{shortname}.1*
%{_mandir}/man5/taskdrc.5*
