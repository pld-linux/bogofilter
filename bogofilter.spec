#
# Conditional build:
# _with_db3	- build with db3 instead of db 4.x
#
Summary:	Bayesian Spam Filter
Summary(pl):	Bayesjañski Filtr Antyspamowy
Name:		bogofilter
Version:	0.14.5.2
Release:	1
License:	GPL
Group:		Applications/Mail
Vendor:		Eric S. Raymond <esr@thyrsus.com>
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	0ef3eb34943e10e9e317063307148940
URL:		http://bogofilter.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
%{!?_with_db3:BuildRequires:	db-devel}
%{?_with_db3:BuildRequires:	db3-devel}
BuildRequires:	flex
BuildRequires:	judy-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

cp $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf.example $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf

rm -f $RPM_BUILD_ROOT%{_bindir}/lexertest

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README NEWS TODO
%config(noreplace,missingok) %{_sysconfdir}/bogofilter.cf
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man1/*
