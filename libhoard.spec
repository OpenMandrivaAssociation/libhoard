%define major 0
%define libname %mklibname hoard %{major}
%define develname %mklibname hoard -d

Summary:	The Hoard Memory Allocator
Name:		libhoard
Version:	3.9.0
Release:	%mkrel 1
Group:		System/Libraries
License:	GPLv2+
URL:		https://www.hoard.org/
Source0:	http://www.cs.umass.edu/~emery/hoard/hoard-%{version}/libhoard-3.9.tar.gz
Patch0:		libhoard-3.9-glibc-2.14+fix.diff
Patch1:		libhoard-3.9-soname.diff

%description
The Hoard memory allocator is a fast, scalable, and memory-efficient memory
allocator for Linux, Solaris, Mac OS X, and Windows. Hoard is a drop-in
replacement for malloc that can dramatically improve application performance,
especially for multithreaded programs running on multiprocessors and multicore
CPUs.

%package -n	%{libname}
Summary:	A fast, scalable, and memory-efficient memory allocator
Group:		System/Libraries

%description -n	%{libname}
The Hoard memory allocator is a fast, scalable, and memory-efficient memory
allocator for Linux, Solaris, Mac OS X, and Windows. Hoard is a drop-in
replacement for malloc that can dramatically improve application performance,
especially for multithreaded programs running on multiprocessors and multicore
CPUs.

%package -n	%{develname}
Summary:	Development files for libhoard
Group:		Development/C++
Requires:	%{libname} >= %{version}
Provides:	hoard-devel = %{version}

%description -n	%{develname}
This package contains development files for libhoard.

%prep
%setup -q -n emeryberger-Hoard-d065953

find -type f | xargs chmod 644

%patch0 -p0
%patch1 -p0
cp -pf src/Makefile{,.orig}
perl -pi -e 's/-O/-fPIC -O/g;s/-static//g;s/-pipe//g' src/Makefile
# on non-i586 we assume that the default arch is sufficient
%ifnarch i586
perl -pi -e 's/-march=pentiumpro //g;s/ -malign-double//g' src/Makefile
%endif

%build
pushd src
make generic-gcc

%install
install -d %{buildroot}%{_libdir}
install -m0755 src/libhoard.so.%{major} %{buildroot}%{_libdir}
ln -s libhoard.so.%{major} %{buildroot}%{_libdir}/libhoard.so

%files -n %{libname}
%doc doc NEWS README THANKS
%{_libdir}/libhoard.so.%{major}*

%files -n %{develname}
%{_libdir}/libhoard.so
