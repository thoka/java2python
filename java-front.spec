Summary: java-front
Name: java-front
Version: 0.9.1pre20986
Release: 1
License: LGPL
Group: Development/Languages/Stratego
URL: http://www.strategoxt.org/Stratego/JavaFront
Source: java-front-0.9.1pre20986.tar.gz
BuildRoot: %{_tmppath}/%{name}-0.9.1pre20986-buildroot
Requires: aterm >= 2.5
Requires: sdf2-bundle >= 2.4
Requires: strategoxt >= 0.16
Provides: %{name} = %{version}

%description

%prep
%setup -q

%build
CFLAGS="-D__NO_CTYPE" ./configure --prefix=%{_prefix} --with-strategoxt=%{_prefix} --with-aterm=%{_prefix} --with-sdf=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}
%{_libdir}
%{_prefix}/libexec
# %{_libexecdir}
%{_datadir}
%doc

%changelog
