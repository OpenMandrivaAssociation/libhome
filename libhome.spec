%define	major 1
%define libname %mklibname home %{major}
%define develname %mklibname home -d

Summary:	A library providing a getpwnam() emulation
Name:		libhome
Version:	0.10.2
Release:	9
Group:		System/Libraries
License:	GPL
URL:		http://pll.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/pll//%{name}-%{version}.tar.gz
Patch0:		libhome-0.10.1-DESTDIR.diff
Patch1:		libhome-0.10.2-fix-link.patch
Patch2:		libhome-0.10.2-db5.patch
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	db-devel
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
Requires:	%{name}-utils = %{version}-%{release}

%description -n	%{libname}
libhome is a library providing a getpwnam() emulation. It support MySQL (3.23),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

%package	utils
Summary:        A library providing a getpwnam() emulation
Group:          System/Libraries
Conflicts:	lib64home1 < 0.10.2-8
Conflicts:	libhome1 < 0.10.2-8

%description	utils
libhome is a library providing a getpwnam() emulation. It support MySQL (3.23),
Open LDAP 2 or system /etc/passwd frontend. It's intended to replace getpwnam
within a system daemons who needs user authentification or identification when
the users are listed on foreign servers.

This package contains various utilities provided by libhome.

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
export LDFLAGS=-lcrypt

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
%attr(0755,root,root) %{_libdir}/*.so.*

%files utils
%defattr(-,root,root)
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/home.conf
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
%attr(0644,root,root) %{_libdir}/*.a


%changelog
* Tue May 08 2012 Crispin Boylan <crisb@mandriva.org> 0.10.2-9
+ Revision: 797559
- Rebuild

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - build with db5
    - split out binaries and man pages
    - (from fwang | 2011-04-12 12:06:31 +0200)

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.2-7mdv2011.0
+ Revision: 627253
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.2-6mdv2011.0
+ Revision: 626532
- rebuilt against mysql-5.5.8 libs

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.2-4mdv2011.0
+ Revision: 609752
- rebuild

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 0.10.2-3mdv2010.1
+ Revision: 537297
- fix link with newer ldflags and db4.8

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.2-2mdv2010.1
+ Revision: 507486
- rebuild

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 0.10.2-1mdv2010.1
+ Revision: 482801
- 0.10.2

* Sun Sep 13 2009 Thierry Vignaud <tv@mandriva.org> 0.10.1-8mdv2010.0
+ Revision: 438620
- rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-7mdv2009.1
+ Revision: 311242
- rebuilt against mysql-5.1.30 libs

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-6mdv2009.0
+ Revision: 233727
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 26 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-5mdv2008.1
+ Revision: 137971
- rebuilt against openldap-2.4.7 libs

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10.1-4mdv2008.0
+ Revision: 83692
- new devel naming

