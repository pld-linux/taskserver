#
# Conditional build:
%bcond_without	systemd		# without systemd unit

%define		shortname	taskd
Summary:	Taskserver is a sync server for Taskwarrior and related products
Name:		taskserver
Version:	1.1.0
Release:	3
License:	MIT
Group:		Applications
Source0:	http://www.taskwarrior.org/download/%{shortname}-%{version}.tar.gz
# Source0-md5:	ac855828c16f199bdbc45fbc227388d0
URL:		http://taskwarrior.org/
BuildRequires:	cmake
BuildRequires:	gnutls-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_systemd:Requires:	systemd-units >= 38}
Provides:	group(taskd)
Provides:	user(taskd)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Taskserver is a sync server for Taskwarrior and related products.

%prep
%setup -q -n %{shortname}-%{version}

%build
%cmake

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/lib/taskd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with systemd}
install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p scripts/systemd/taskd.service $RPM_BUILD_ROOT%{systemdunitdir}
%endif

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{shortname}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 340 taskd
%useradd -u 340 -r -d /var/lib/taskd -s /bin/false -c "Task Server user" -g taskd taskd

%post
%{?with_systemd:%systemd_post taskd.service}

%preun
%{?with_systemd:%systemd_preun taskd.service}

%postun
if [ "$1" = "0" ]; then
	%userremove taskd
	%groupremove taskd
fi
%{?with_systemd:%systemd_reload}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/%{shortname}
%attr(755,root,root) %{_bindir}/taskdctl
%{_mandir}/man1/%{shortname}.1*
%{_mandir}/man1/taskdctl.1*
%{_mandir}/man5/taskdrc.5*
%{?with_systemd:%{systemdunitdir}/taskd.service}
%dir %attr(750,taskd,taskd) /var/lib/taskd
