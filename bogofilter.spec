# TODO:
# - make separate package linked with sqlite
# - make milter subpackage
# - maybe make some separate package with contrib perl scripts?
# - remove bogus banner
#
Summary:	Bayesian Spam Filter
Summary(pl.UTF-8):	Bayesowski Filtr Antyspamowy
Name:		bogofilter
Version:	1.2.5
Release:	1
License:	GPL v2
Group:		Applications/Mail
Source0:	https://downloads.sourceforge.net/bogofilter/%{name}-%{version}.tar.xz
# Source0-md5:	8763f87adfff7b802ced177d8c654539
Patch0:		%{name}-home_etc.patch
URL:		https://bogofilter.sourceforge.net/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
# alternatives (--with-database=): qdbm,sqlite3,tokyocabinet,kyotocabinet,lmdb
BuildRequires:	db-devel
BuildRequires:	flex
BuildRequires:	gettext-tools
BuildRequires:	gsl-devel >= 1.4
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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

cp -p $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf.example $RPM_BUILD_ROOT%{_sysconfdir}/bogofilter.cf

install bogogrep $RPM_BUILD_ROOT%{_bindir}
# Some apps from contrib:
install contrib/bfproxy.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/bogominitrain.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/mime.get.rfc822.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/printmaildir.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/spamitarium.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/stripsearch.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/trainbogo.sh $RPM_BUILD_ROOT%{_bindir}

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
%doc AUTHORS GETTING.STARTED NEWS* README RELEASE.NOTES TODO doc/{README.*,bogofilter-SA*,bogofilter-faq.html,bogofilter-tuning.HOWTO.html,bogotune-faq.html,integrating*}
%lang(bg) %doc doc/bogofilter-faq-bg.xhtml
%lang(fr) %doc doc/bogofilter-faq-fr.html
%lang(it) %doc doc/bogofilter-faq-it.html
%doc contrib/{README.*,bogo.R,bogofilter-qfe.sh,bogofilter-milter.pl,dot-qmail-bogofilter-default,*.example,parmtest.sh,randomtrain.sh,scramble.sh,vm-bogofilter.el}
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/bogofilter.cf
%attr(755,root,root) %{_bindir}/bf_compact
%attr(755,root,root) %{_bindir}/bf_copy
%attr(755,root,root) %{_bindir}/bf_tar
%attr(755,root,root) %{_bindir}/bfproxy.pl
%attr(755,root,root) %{_bindir}/bogofilter
%attr(755,root,root) %{_bindir}/bogogrep
%attr(755,root,root) %{_bindir}/bogolexer
%attr(755,root,root) %{_bindir}/bogominitrain.pl
%attr(755,root,root) %{_bindir}/bogotune
%attr(755,root,root) %{_bindir}/bogoupgrade
%attr(755,root,root) %{_bindir}/bogoutil
%attr(755,root,root) %{_bindir}/mime.get.rfc822.pl
%attr(755,root,root) %{_bindir}/printmaildir.pl
%attr(755,root,root) %{_bindir}/spamitarium.pl
%attr(755,root,root) %{_bindir}/stripsearch.pl
%attr(755,root,root) %{_bindir}/trainbogo.sh
%{_mandir}/man1/bf_compact.1*
%{_mandir}/man1/bf_copy.1*
%{_mandir}/man1/bf_tar.1*
%{_mandir}/man1/bogofilter.1*
%{_mandir}/man1/bogolexer.1*
%{_mandir}/man1/bogotune.1*
%{_mandir}/man1/bogoupgrade.1*
%{_mandir}/man1/bogoutil.1*
