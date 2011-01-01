%define	major 1
%define libname %mklibname home %{major}
%define develname %mklibname home -d

Summary:	A library providing a getpwnam() emulation
Name:		libhome
Version:	0.10.2
Release:	%mkrel 7
Group:		System/Libraries
License:	GPL
URL:		http://pll.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pll//%{name}-%{version}.tar.gz
Patch0:		libhome-0.10.1-DESTDIR.diff
Patch1:		libhome-0.10.2-fix-link.patch
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	db4-devel
BuildRequires:	groff-for-man
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libhome is a library providing a getpwnam() emulation. It support MySQL (3.23),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

%package -n	%{libname}
Summary:	A library providing a getpwnam() emulation
Group:          System/Libraries

%description -n	%{libname}
libhome is a library providing a getpwnam() emulation. It support MySQL (3.23),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

%package -n	%{develname}
Summary:	Static library and header files for the libhome library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname home 1 -d}

%description -n	%{develname}
libhome is a library providing a getpwnam() emulation. It support MySQL (3.23),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

This package contains the static libhome library and its header files.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# do not use bdb-4.3 just yet
perl -pi -e "s|db-4.3|db-4.8|g" configure*

%build
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%configure2_5x \
    --with-conffile=%{_sysconfdir}/home.conf
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}

%makeinstall_std

install -m0640 home.conf %{buildroot}%{_sysconfdir}/home.conf

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING.LIB NEWS README
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/home.conf
%attr(0755,root,root) %{_libdir}/*.so.*
%attr(0755,root,root) %{_bindir}/home_finger
%attr(0755,root,root) %{_bindir}/home_su
%attr(0755,root,root) %{_sbindir}/home_proxy
%attr(0644,root,root) %{_mandir}/man*/*

%files -n %{develname}
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/libhome.sh
%dir %{_includedir}/home
%attr(0644,root,root) %{_includedir}/home/*.h
%attr(0755,root,root) %{_libdir}/*.so
%attr(0755,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/*.a
