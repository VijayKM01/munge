# $Id$

Name:		munge
Version:	0
Release:	1

Summary:	MUNGE Uid 'N' Gid Emporium
Group:		System Environment/Daemons
License:	GPL
URL:		http://www.llnl.gov/linux/munge/

BuildRoot:	%{_tmppath}/%{name}-%{version}

Source0:	%{name}-%{version}.tar

%package devel
Summary:	Headers and libraries for developing applications using MUNGE
Group:		Development/Libraries

%package libs
Summary:	Libraries for applications using MUNGE
Group:		System Environment/Libraries

%description
MUNGE (MUNGE Uid 'N' Gid Emporium) is a service for creating and validating
credentials in order to allow a process to securely authenticate the UID and
GID of another local or remote process within a security realm.  Clients can
create and validate these credentials without the use of root privileges,
reserved ports, or platform-specific methods.

%description devel
A header file and static library for developing applications using MUNGE.

%description libs
A shared library for applications using MUNGE.

%prep
%setup -n munge

%build
rm -f libmunge-32_64.a
%ifnos aix
##
# Add one of the following to the rpm command line to specify 32b/64b builds:
#   --with arch32               (build 32b executables and library)
#   --with arch64               (build 64b executables and library)
##
%configure \
  %{?_with_arch32: --enable-arch=32} \
  %{?_with_arch64: --enable-arch=64} \
  --program-prefix=%{?_program_prefix:%{_program_prefix}}
make
%else
##
# Add --target ppc-aix to the rpm command line to force AIX builds.
#   You will have to override the platform information at install time
#   with --ignoreos.
#
# Add one of the following to the rpm command line to specify 32b/64b builds:
#   --define 'arch 32'          (build 32b executables and library)
#   --define 'arch 64'          (build 64b executables and library)
#   --define 'arch 32_64'       (build 32b executables and multiarch library)
##
%{?arch:ARCH="%{arch}"}
if test "$ARCH" = "32_64"; then
  export OBJECT_MODE=64
  %configure -C --enable-arch=64 \
    --program-prefix=%{?_program_prefix:%{_program_prefix}} 
  ( cd src/libmunge && make install DESTDIR="`pwd`/../../tmp-$$/64" )
  make clean
  export OBJECT_MODE=32
  %configure -C --enable-arch=32 \
    --program-prefix=%{?_program_prefix:%{_program_prefix}}
  ( cd src/libmunge && make install DESTDIR="`pwd`/../../tmp-$$/32" )
  mkdir -p tmp-$$/64-lib
  ( cd tmp-$$/64-lib && ar -X64 -x ../64%{_libdir}/libmunge.a )
  mkdir -p tmp-$$/32-lib
  ( cd tmp-$$/32-lib && ar -X32 -x ../32%{_libdir}/libmunge.a )
  ar -X32_64 -c -q libmunge-32_64.a tmp-$$/*-lib/*
  rm -rf tmp-$$
elif test "$ARCH" = "32"; then
  export OBJECT_MODE=32
  %configure -C --enable-arch=32 \
    --program-prefix=%{?_program_prefix:%{_program_prefix}}
elif test "$ARCH" = "64"; then
  export OBJECT_MODE=64
  %configure -C --enable-arch=64 \
    --program-prefix=%{?_program_prefix:%{_program_prefix}} 
else
  %configure -C --program-prefix=%{?_program_prefix:%{_program_prefix}} 
fi
make
%endif
  
%install
rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"
DESTDIR="$RPM_BUILD_ROOT" make install
test -f libmunge-32_64.a \
  && cp libmunge-32_64.a "$RPM_BUILD_ROOT"%{_libdir}/libmunge.a

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ -x /sbin/chkconfig ]; then /sbin/chkconfig --add munge; fi

%post libs
if [ -x /sbin/ldconfig ]; then /sbin/ldconfig %{_libdir}; fi

%preun
if [ "$1" = 0 ]; then
  %{_sysconfdir}/init.d/munge stop >/dev/null 2>&1 || :
  if [ -x /sbin/chkconfig ]; then /sbin/chkconfig --del munge; fi
fi

%postun
if [ "$1" -ge 1 ]; then
  %{_sysconfdir}/init.d/munge condrestart >/dev/null 2>&1 || :
fi

%postun libs
if [ -x /sbin/ldconfig ]; then /sbin/ldconfig %{_libdir}; fi

%files
%defattr(-,root,root,0755)
%doc AUTHORS
%doc BUGS
%doc ChangeLog
%doc COPYING
%doc DISCLAIMER
%doc HISTORY
%doc INSTALL
%doc JARGON
%doc NEWS
%doc PLATFORMS
%doc QUICKSTART
%doc README*
%doc TODO
%doc doc/*
%dir %attr(0700,root,root) %config %{_sysconfdir}/munge
%config(noreplace) %{_sysconfdir}/*/*
%{_localstatedir}/*/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*[^3]/*

%files devel
%defattr(-,root,root,0755)
%{_includedir}/*
%{_libdir}/*.la
%{_mandir}/*3/*
%ifnos aix
%{_libdir}/*.a
%{_libdir}/*.so
%endif

%files libs
%defattr(-,root,root,0755)
%ifnos aix
%{_libdir}/*.so.*
%else
%{_libdir}/*.a
%endif
