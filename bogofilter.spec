Summary:	Bayesian Spam Filter
Summary(pl):	Bayesiañski Filtr Antyspamowy
Name:		bogofilter
Version:	0.7
Release:	0.1
License:	GPL
Group:		Applications/Mail
Vendor:		Eric Raymond <esr@thyrsus.com>
Source0:	http://www.tuxedo.org/~esr/bogofilter/%{name}-%{version}.tar.gz
URL:		http://www.tuxedo.org/~esr/bogofilter/
BuildRequires:	judy-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl



%prep
%setup -q

%build
aclocal
%{__autoconf}
autoheader
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
