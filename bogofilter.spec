Summary:	Bayesian Spam Filter
Summary(pl):	Bayesjañski Filtr Antyspamowy
Name:		bogofilter
Version:	0.92.8
Release:	1
License:	GPL
Vendor:		Eric S. Raymond <esr@thyrsus.com>
Group:		Applications/Mail
Source0:	http://osdn.dl.sourceforge.net/bogofilter/%{name}-%{version}.tar.gz
# Source0-md5:	f8732688a3fe887a67da0ec39dbb06a1
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-dummy.patch
URL:		http://bogofilter.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	gsl-devel
BuildRequires:	judy-devel
Requires:	gsl >= 1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer

%description
Bogofilter is a Bayesian spam filter. In its normal mode of operation,
it takes an email message or other text on standard input, does a
statistical check against lists of "good" and "bad" words, and returns
a status code indicating whether or not the message is spam.
Bogofilter is designed with fast algorithms (including Berkeley DB
system), coded directly in C, and tuned for speed, so it can be used
for production by sites that process a lot of mail.

%description -l pl
Bogofilter jest bayesjañskim filtrem antyspamowym. W podstawowym
trybie dzia³ania na emailu lub innym tek¶cie odczytanym na wej¶ciu
wykonuje statystyczne testy na wystêpowanie "dobrych" i "z³ych" s³ów i
zwraca kod powrotu wskazuj±cy czy wiadomo¶æ jest spamem, czy te¿ nie.
Bogofilter jest zaprojektowany z u¿yciem szybkich algorytmów
(w³±czaj±c w to Berkeley DB), napisany w czystym C i "podkrêcony" pod
k±tem szybko¶ci, a wiêc mo¿e byæ u¿ywany na systemach "produkcyjnych",
które przetwarzaj± du¿e ilo¶ci poczty.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf.example $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf

rm -f $RPM_BUILD_ROOT%{_bindir}/lexertest

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS RELEASE* NEWS README TODO CHANGES*
%config(noreplace,missingok) %{_sysconfdir}/bogofilter.cf
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man1/*
