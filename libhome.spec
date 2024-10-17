%define major 1
%define pmajor 2
%define libname %mklibname home %{major}
%define libproxy %mklibname nss_home_proxy %{pmajor}
%define devname %mklibname home -d

Summary:	A library providing a getpwnam() emulation
Name:		libhome
Version:	0.10.2
Release:	11
License:	GPLv2+
Group:		System/Libraries
Url:		https://pll.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pll//%{name}-%{version}.tar.gz
Patch0:		libhome-0.10.1-DESTDIR.diff
Patch1:		libhome-0.10.2-fix-link.patch
Patch2:		libhome-0.10.2-db5.patch
BuildRequires:	groff-for-man
BuildRequires:	libtool
BuildRequires:	db-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(openssl)

%description
libhome is a library providing a getpwnam() emulation. It support MySQL,
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	A library providing a getpwnam() emulation
Group:		System/Libraries

%description -n %{libname}
libhome is a library providing a getpwnam() emulation. It support MySQL,
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

%files -n %{libname}
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/libhome.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libproxy}
Summary:	A library providing a getpwnam() emulation
Group:		System/Libraries
Conflicts:	%{_lib}home1 < 0.10.2-10

%description -n %{libproxy}
libhome is a library providing a getpwnam() emulation. It support MySQL,
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

%files -n %{libproxy}
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/libnss_home_proxy.so.%{pmajor}*

#----------------------------------------------------------------------------

%package utils
Summary:	A library providing a getpwnam() emulation (utilities package)
Group:		System/Libraries

%description utils
libhome is a library providing a getpwnam() emulation. It support MySQL,
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

This package contains various utilities provided by libhome.

%files utils
%config(noreplace) %{_sysconfdir}/home.conf
%{_bindir}/home_finger
%{_bindir}/home_su
%{_sbindir}/home_proxy
%{_mandir}/man*/*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development library and header files for the libhome library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libproxy} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
libhome is a library providing a getpwnam() emulation. It support MySQL),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

This package contains the static libhome library and its header files.

%files -n %{devname}
%attr(0755,root,root) %{_bindir}/libhome.sh
%{_includedir}/home/
%{_libdir}/*.so

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
autoreconf
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"
export LDFLAGS="%{ldflags} -lcrypt"

%configure2_5x \
	--with-conffile=%{_sysconfdir}/home.conf \
	--disable-static
%make

%install
install -d %{buildroot}%{_sysconfdir}

%makeinstall_std

install -m0640 home.conf %{buildroot}%{_sysconfdir}/home.conf

