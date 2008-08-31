# TODO:
# - make separate package linked with sqlite
# - make milter subpackage
# - maybe make some separate package with contrib perl scripts?
# - remove bogus banner
#
Summary:	Bayesian Spam Filter
Summary(pl.UTF-8):	Bayesowski Filtr Antyspamowy
Name:		bogofilter
Version:	1.1.7
Release:	1
License:	GPL v2
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/bogofilter/%{name}-%{version}.tar.bz2
# Source0-md5:	0ece697e8b54fcc069dba1af55c6015a
Patch0:		%{name}-home_etc.patch
URL:		http://bogofilter.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	gsl-devel
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

%description -l pl.UTF-8
Bogofilter jest bayesowski filtrem antyspamowym. W podstawowym trybie
działania na emailu lub innym tekście odczytanym na wejściu wykonuje
statystyczne testy na występowanie "dobrych" i "złych" słów i zwraca
kod powrotu wskazujący czy wiadomość jest spamem, czy też nie.
Bogofilter jest zaprojektowany z użyciem szybkich algorytmów
(włączając w to Berkeley DB), napisany w czystym C i "podkręcony" pod
kątem szybkości, a więc może być używany na systemach "produkcyjnych",
które przetwarzają duże ilości poczty.

%prep
%setup -q
%patch0 -p1

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

install bogogrep $RPM_BUILD_ROOT%{_bindir}
# Some apps from contrib:
install contrib/bfproxy.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/bogominitrain.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/mime.get.rfc822.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/printmaildir.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/spamitarium.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/stripsearch.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/trainbogo.sh $RPM_BUILD_ROOT%{_bindir}

# Some final cleanups:
rm -f $RPM_BUILD_ROOT%{_bindir}/lexertest

%clean
rm -rf $RPM_BUILD_ROOT

# That banner is bogus - no sense to have it _while_ upgrading...
# It should be some trigger...
# It makes at least sense that someone will read this file
# before running bogofilter after upgrade and corrupt his db as
# it happened before. Bogofilter is not service/daemon by default
# so its not run automaticaly after upgrade. One can still backup
# his db.
%pre
%banner %{name} -e <<'EOF'

WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
------------------------------------------------------------------------
POTENTIAL FOR DATA CORRUPTION DURING UPDATES

If you plan to upgrade your database library, if only as a side effect
of an operating system upgrade, DO HEED the relevant documentation, for
instance, the %{_docdir}/%{name}-%{version}/README.db file.
You may need to prepare the upgrade with the old version of the software.

Otherwise, you may cause irrecoverable damage to your databases.

DO backup your databases before making the upgrade.
------------------------------------------------------------------------
WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING

EOF

%files
%defattr(644,root,root,755)
%doc AUTHORS GETTING.STARTED RELEASE* NEWS* README doc/{README.*,bogofilter-SA*,integrating*} TODO
%doc contrib/{bogofilter-qfe.sh,bogofilter-milter.pl,dot-qmail-bogofilter-default,*.example,parmtest.sh}
%doc contrib/{README.*,randomtrain.sh,scramble.sh}
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/bogofilter.cf
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
