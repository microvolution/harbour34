# ---------------------------------------------------------------
# Copyright 2003 Przemyslaw Czerpak <druzus@polbox.com>,
# Dave Pearson <davep@davep.org>
# Harbour RPM spec file
#
# See LICENSE.txt for licensing terms.
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# HOWTO .rpm docs:
#    https://fedoraproject.org/wiki/How_to_create_an_RPM_package
#    https://www.gurulabs.com/media/files/courseware-samples/GURULABS-RPM-GUIDE-v1.0.PDF
# ---------------------------------------------------------------

######################################################################
## Definitions.
######################################################################

# please add your distro suffix if it does not belong to the ones recognized below
# and remember that order checking can be important

%define platform %(release=$(rpm -q --queryformat='%{VERSION}' fedora-release 2>/dev/null) && echo "fc$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' epel-release 2>/dev/null) && echo "el$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' centos-release 2>/dev/null) && echo "el$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' suse-release 2>/dev/null) && echo "sus$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' openSUSE-release 2>/dev/null) && echo "sus$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' redhat-release 2>/dev/null) && echo "rh$release" | tr -d '.')
%if "%{platform}" == ""
%define platform %(release=$(rpm -q --queryformat='%{VERSION}' system-release 2>/dev/null) && echo 'amzn1' | tr -d '.')
%if "%{platform}" == ""
%undefine platform
%endif
%endif
%endif
%endif
%endif
%endif
%endif

%define hb_ldconf %([ -d /etc/ld.so.conf.d ] && echo /etc/ld.so.conf.d)
%if "%{hb_ldconf}" == ""
%undefine hb_ldconf
%endif

%define name      harbour
%define dname     Harbour
%define version   0.0.0
%define releasen  1
%define verstat   dev
%define hb_etcdir /etc/%{name}
%define hb_plat   export HB_PLATFORM=linux
%define hb_cc     export HB_COMPILER=gcc
%define hb_cflag  export HB_USER_CFLAGS=
%define hb_lflag  export HB_USER_LDFLAGS=
%define hb_dflag  export HB_USER_DFLAGS=
%define shl_path  export LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}$(pwd)/lib/${HB_PLATFORM}/${HB_COMPILER}${HB_BUILD_NAME}
%define hb_gpm    export HB_WITH_GPM=%{!?_without_gpm:yes}%{?_without_gpm:no}
%define hb_crs    export HB_WITH_CURSES=%{!?_without_curses:yes}%{?_without_curses:no}
%define hb_sln    export HB_WITH_SLANG=%{!?_without_slang:yes}%{?_without_slang:no}
%define hb_x11    export HB_WITH_X11=%{!?_without_x11:yes}%{?_without_x11:no}
%define hb_local  export HB_WITH_ZLIB=%{?_with_localzlib:local} ; export HB_WITH_PCRE2=%{?_with_localpcre2:local} ; export HB_WITH_PCRE=%{?_with_localpcre1:local} ; export HB_WITH_BZIP2=%{?_with_localbz2:local} ; export HB_WITH_EXPAT=%{?_with_localexpat:local} ; export HB_WITH_LIBYAML=%{?_with_locallibyaml:local} ; export HB_WITH_SQLITE3=%{?_with_localsqlite3:local}
%define hb_proot  export HB_INSTALL_PKG_ROOT=${RPM_BUILD_ROOT}
%define hb_bdir   export HB_INSTALL_BIN=${RPM_BUILD_ROOT}%{_bindir}
%define hb_ldir   export HB_INSTALL_LIB=${RPM_BUILD_ROOT}%{_libdir}/%{name}
%define hb_ddir   export HB_INSTALL_DYN=${RPM_BUILD_ROOT}%{_libdir}/%{name}
%define hb_idir   export HB_INSTALL_INC=${RPM_BUILD_ROOT}%{_includedir}/%{name}
%define hb_tdir   export HB_INSTALL_DOC=${RPM_BUILD_ROOT}%{_docdir}/%{name}
%define hb_mdir   export HB_INSTALL_MAN=${RPM_BUILD_ROOT}%{_mandir}
%define hb_edir   export HB_INSTALL_ETC=${RPM_BUILD_ROOT}%{hb_etcdir}
%define hb_cdir   export HB_INSTALL_CONTRIB=${RPM_BUILD_ROOT}%{_datadir}/%{name}/contrib
%define hb_blds   export HB_BUILD_STRIP=all
%define hb_bldsh  export HB_BUILD_SHARED=%{!?_with_static:yes}
%define hb_cmrc   export HB_BUILD_NOGPLLIB=%{?_without_gpllib:yes}
%define hb_ctrb   export HB_BUILD_CONTRIBS="hbblink hbbz2 hbcomio hbcomm hbcrypto hbct hbexpat hbformat hbformat/utils hbfoxpro hbfship hbgt hbhpdf hbhttpd hblzf hbmemio hbmisc hbmlzo hbmxml hbmzip hbnetio hbnetio/utils/hbnetio hbnf hboslib hbpipeio hbsms hbsqlit3 hbtcpio hbtest hbtip hbtpathy hbunix hbxpp hbxdiff hbyaml hbzebra hbziparc rddbm rddmisc rddsql sddsqlt3 xhb %{?_with_cairo:hbcairo} %{?_with_cups:hbcups} %{?_with_curl:hbcurl} %{?_with_freeimage:hbfimage} %{?_with_gd:hbgd} %{?_with_openssl:hbssl} %{?_with_firebird:hbfbird sddfb} %{?_with_mysql:hbmysql sddmy} %{?_with_odbc:hbodbc sddodbc} %{?_with_pgsql:hbpgsql sddpg} %{?_with_rabbitmq:hbamqp} %{?_with_ads:rddads} hbdoc hbrun"
%define hb_env    %{hb_plat} ; %{hb_cc} ; %{hb_cflag} ; %{hb_lflag} ; %{hb_dflag} ; %{shl_path} ; %{hb_gpm} ; %{hb_crs} ; %{hb_sln} ; %{hb_x11} ; %{hb_local} ; %{hb_proot} ; %{hb_bdir} ; %{hb_idir} ; %{hb_ldir} ; %{hb_ddir} ; %{hb_edir} ; %{hb_cdir} ; %{hb_mdir} ; %{hb_tdir} ; %{hb_ctrb} ; %{hb_cmrc} ; %{hb_blds} ; %{hb_bldsh}
######################################################################
## Preamble.
######################################################################
Summary:        Free software Clipper compatible compiler
Summary(pl):    Darmowy kompilator kompatybilny z językiem Clipper.
Summary(pt_BR): Um compilador Clipper compativel Gratis
Summary(ru):    Свободный компилятор, совместимый с языком Clipper.
Summary(hu):    Szabad szoftver Clipper kompatibilis fordító
Name:           %{name}
Version:        %{version}
Release:        %{releasen}%{?verstat:.%{verstat}}%{?platform:.%{platform}}
License:        GPL (plus exception)
Group:          Development/Languages
URL:            https://github.com/vszakats/hb/
Source:         %{name}-%{version}.src.tar.gz
BuildRequires:  gcc binutils %{!?_without_curses: ncurses-devel} %{!?_without_gpm: gpm-devel}
Requires:       gcc binutils sh-utils %{name}-lib = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name} harbour lib%{name}.so
BuildRoot:      /tmp/%{name}-%{version}-root

%define         _noautoreq    'libharbour.*'

%description
%{dname} is a CA-Cl*pper compatible compiler for multiple platforms. This
package includes a compiler, pre-processor, header files, virtual machine
and documentation.

%description -l pl
%{dname} to kompatybilny z językiem CA-Cl*pper kompilator rozwijany na
wielu różnych platformach. Ten pakiet zawiera kompilator, preprocesor,
zbiory nagłówkowe, wirtualn+ maszynę oraz dokumentację.

%description -l pt_BR
%{dname} é um compilador Clipper compativel para multiplas plataformas.
Esse pacote contem um compilador, um pré-processador, arquivos de cabeçalho
uma maquina virtual e documentaçăo.

%description -l ru
%{dname} - многоплатформенный компилятор, совместимый с языком CA-Cl*pper.
Этот пакет содержит компилятор, препроцессор, файлы заголовков, виртуальную
машину и документацию.

%description -l hu
%{dname} egy több platformon is működő CA-Cl*pper kompatibilis
fordítóprogram. A csomag része a fordító maga, az előfordító, fejléc
állományok, a virtuális gép és függvénykönyvtárak, valamint a dokumentáció.

######################################################################
## main shared lib
######################################################################

%package lib
Summary:        Shared runtime libaries for %{dname} compiler
Summary(pl):    Dzielone bilioteki dla kompilatora %{dname}
Summary(ru):    Совместно используемые библиотеки для компилятора %{dname}
Summary(hu):    Megosztott könyvtárak a(z) %{dname} fordítóhoz
Group:          Development/Languages
Provides:       lib%{name}.so

%description lib
%{dname} is a Clipper compatible compiler.
This package provides %{dname} runtime shared libraries for programs
linked dynamically.

%description -l pl lib
%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.
Ten pakiet udostępnia dzielone bilioteki kompilatora %{dname}
dla programów konsolidowanych dynamicznie.

%description -l pt_BR lib
%{dname} é um compilador compativel com o Clipper.
Esse pacote %{dname} provem as bibliotecas compartilhadas para programas
linkados dinamicamente.

%description -l ru lib
%{dname} - компилятор, совместимый с языком CA-Cl*pper.
Этот пакет содержит совместно используемые библиотеки %{dname},
необходимые для работы динамически скомпонованных программ.

%description -l hu lib
A(z) %{dname} egy Clipper kompatibilis fordítóprogram.
Ez a csomag biztosítja a dinamikusan szerkesztett %{dname}
programokhoz szükséges megosztott (dinamikus) futtatókönyvtárakat.

######################################################################
## contrib libs (without package requirements)
######################################################################

%package contrib
Summary:        Contrib runtime libaries for %{dname} compiler
Summary(pl):    Bilioteki z drzewa contrib dla kompilatora %{dname}
Summary(pt_BR): Libs contrib para %{dname}
Summary(ru):    Библиотеки из дерева contrib для компилятора %{dname}
Summary(hu):    Kiegészítő könyvtárak a(z) %{dname} fordítóhoz
Group:          Development/Languages
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description contrib
%{dname} is a Clipper compatible compiler.
This package provides %{dname} contrib libraries for program linking.

%description -l pl contrib
%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.
Ten pakiet udostępnia statyczne bilioteki z drzewa contrib dla
kompilatora %{dname}.

%description -l pt_BR contrib
%{dname} é um compilador compativel com o clippe.
Esse pacote %{dname} provem as bibliotecas contrib para linkagem
dos programas.

%description -l ru contrib
%{dname} - компилятор, совместимый с языком CA-Cl*pper.
Этот пакет содержит статические библиотеки %{dname} из дерева contrib.

%description -l hu contrib
A(z) %{dname} egy Clipper kompatibilis fordítóprogram.
Ez a csomag kiegészítő (contrib) könyvtárakat biztosít
statikus szerkesztéshez.

######################################################################
## contrib libs (with package requirements)
######################################################################

## ADS RDD
%{?_with_ads:%package ads}
%{?_with_ads:Summary:        ADS RDDs for %{dname} compiler}
%{?_with_ads:Summary(pl):    Bilioteka sterowników (RDDs) ADS dla kompilatora %{dname}}
%{?_with_ads:Group:          Development/Languages}
%{?_with_ads:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_ads:%description ads}
%{?_with_ads:%{dname} is a Clipper compatible compiler.}
%{?_with_ads:This package provides %{dname} ADS RDDs for program linking.}

%{?_with_ads:%description -l pl ads}
%{?_with_ads:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_ads:Ten pakiet udostępnia sterowniki (RDD) ADS dla kompilatora %{dname}.}

## cairo library
%{?_with_cairo:%package cairo}
%{?_with_cairo:Summary:        Cairo library bindings for %{dname} compiler}
%{?_with_cairo:Summary(pl):    Bilioteka Cairo dla kompilatora %{dname}}
%{?_with_cairo:Group:          Development/Languages}
%{?_with_cairo:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_cairo:%description cairo}
%{?_with_cairo:%{dname} is a Clipper compatible compiler.}
%{?_with_cairo:This package provides %{dname} Cairo library for program linking.}

%{?_with_cairo:%description -l pl cairo}
%{?_with_cairo:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_cairo:Ten pakiet udostępnia statyczn+ biliotekę Cairo dla kompilatora %{dname}.}

## cups library
%{?_with_cups:%package cups}
%{?_with_cups:Summary:        CUPS library bindings for %{dname} compiler}
%{?_with_cups:Summary(pl):    Bilioteka CUPS dla kompilatora %{dname}}
%{?_with_cups:Group:          Development/Languages}
%{?_with_cups:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_cups:%description cups}
%{?_with_cups:%{dname} is a Clipper compatible compiler.}
%{?_with_cups:This package provides %{dname} CUPS library for program linking.}

%{?_with_cups:%description -l pl cups}
%{?_with_cups:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_cups:Ten pakiet udostępnia statyczn+ biliotekę CUPS dla kompilatora %{dname}.}

## curl library
%{?_with_curl:%package curl}
%{?_with_curl:Summary:        CURL library bindings for %{dname} compiler}
%{?_with_curl:Summary(pl):    Bilioteka CURL dla kompilatora %{dname}}
%{?_with_curl:Group:          Development/Languages}
%{?_with_curl:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_curl:%description curl}
%{?_with_curl:%{dname} is a Clipper compatible compiler.}
%{?_with_curl:This package provides %{dname} CURL library for program linking.}

%{?_with_curl:%description -l pl curl}
%{?_with_curl:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_curl:Ten pakiet udostępnia statyczn+ biliotekę CURL dla kompilatora %{dname}.}

## firebird library
%{?_with_firebird:%package firebird}
%{?_with_firebird:Summary:        Firebird library bindings for %{dname} compiler}
%{?_with_firebird:Summary(pl):    Bilioteka Firebird dla kompilatora %{dname}}
%{?_with_firebird:Group:          Development/Languages}
%{?_with_firebird:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_firebird:%description firebird}
%{?_with_firebird:%{dname} is a Clipper compatible compiler.}
%{?_with_firebird:This package provides %{dname} Firebird library for program linking.}

%{?_with_firebird:%description -l pl firebird}
%{?_with_firebird:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_firebird:Ten pakiet udostępnia statyczn+ biliotekę Firebird dla kompilatora %{dname}.}

## freeimage library
%{?_with_freeimage:%package freeimage}
%{?_with_freeimage:Summary:        FreeImage library bindings for %{dname} compiler}
%{?_with_freeimage:Summary(pl):    Bilioteka FreeImage dla kompilatora %{dname}}
%{?_with_freeimage:Group:          Development/Languages}
%{?_with_freeimage:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_freeimage:%description freeimage}
%{?_with_freeimage:%{dname} is a Clipper compatible compiler.}
%{?_with_freeimage:This package provides %{dname} FreeImage library for program linking.}

%{?_with_freeimage:%description -l pl freeimage}
%{?_with_freeimage:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_freeimage:Ten pakiet udostępnia statyczn+ biliotekę FreeImage dla kompilatora %{dname}.}

## gd library
%{?_with_gd:%package gd}
%{?_with_gd:Summary:        GD library bindings for %{dname} compiler}
%{?_with_gd:Summary(pl):    Bilioteka GD dla kompilatora %{dname}}
%{?_with_gd:Group:          Development/Languages}
%{?_with_gd:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_gd:%description gd}
%{?_with_gd:%{dname} is a Clipper compatible compiler.}
%{?_with_gd:This package provides %{dname} GD library for program linking.}

%{?_with_gd:%description -l pl gd}
%{?_with_gd:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_gd:Ten pakiet udostępnia statyczn+ biliotekę GD dla kompilatora %{dname}.}

## openssl library
%{?_with_openssl:%package openssl}
%{?_with_openssl:Summary:        OpenSSL library bindings for %{dname} compiler}
%{?_with_openssl:Summary(pl):    Bilioteka OpenSSL dla kompilatora %{dname}}
%{?_with_openssl:Group:          Development/Languages}
%{?_with_openssl:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_openssl:%description openssl}
%{?_with_openssl:%{dname} is a Clipper compatible compiler.}
%{?_with_openssl:This package provides %{dname} OpenSSL library for program linking.}

%{?_with_openssl:%description -l pl openssl}
%{?_with_openssl:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_openssl:Ten pakiet udostępnia statyczn+ biliotekę OpenSSL dla kompilatora %{dname}.}

## mysql library
%{?_with_mysql:%package mysql}
%{?_with_mysql:Summary:        MariaDB/MYSQL library bindings for %{dname} compiler}
%{?_with_mysql:Summary(pl):    Bilioteka MariaDB/MYSQL dla kompilatora %{dname}}
%{?_with_mysql:Group:          Development/Languages}
%{?_with_mysql:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_mysql:%description mysql}
%{?_with_mysql:%{dname} is a Clipper compatible compiler.}
%{?_with_mysql:This package provides %{dname} MariaDB/MYSQL library for program linking.}

%{?_with_mysql:%description -l pl mysql}
%{?_with_mysql:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_mysql:Ten pakiet udostępnia statyczn+ biliotekę MariaDB/MYSQL dla kompilatora %{dname}.}

## odbc library
%{?_with_odbc:%package odbc}
%{?_with_odbc:Summary:        ODBC library bindings for %{dname} compiler}
%{?_with_odbc:Summary(pl):    Bilioteka ODBC dla kompilatora %{dname}}
%{?_with_odbc:Group:          Development/Languages}
%{?_with_odbc:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_odbc:%description odbc}
%{?_with_odbc:%{dname} is a Clipper compatible compiler.}
%{?_with_odbc:This package provides %{dname} ODBC library for program linking.}

%{?_with_odbc:%description -l pl odbc}
%{?_with_odbc:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_odbc:Ten pakiet udostępnia statyczn+ biliotekę ODBC dla kompilatora %{dname}.}

## pgsql library
%{?_with_pgsql:%package pgsql}
%{?_with_pgsql:Summary:        PGSQL library bindings for %{dname} compiler}
%{?_with_pgsql:Summary(pl):    Bilioteka PGSQL dla kompilatora %{dname}}
%{?_with_pgsql:Group:          Development/Languages}
%{?_with_pgsql:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_pgsql:%description pgsql}
%{?_with_pgsql:%{dname} is a Clipper compatible compiler.}
%{?_with_pgsql:This package provides %{dname} PGSQL library for program linking.}

%{?_with_pgsql:%description -l pl pgsql}
%{?_with_pgsql:%{dname} to kompatybilny z językiem CA-Cl*pper kompilator.}
%{?_with_pgsql:Ten pakiet udostępnia statyczn+ biliotekę PGSQL dla kompilatora %{dname}.}

## rabbitmq-c library
%{?_with_rabbitmq:%package rabbitmq}
%{?_with_rabbitmq:Summary:        rabbitmq-c library bindings for %{dname} compiler}
%{?_with_rabbitmq:Summary(pl):    Bilioteka rabbitmq-c dla kompilatora %{dname}}
%{?_with_rabbitmq:Group:          Development/Languages}
%{?_with_rabbitmq:Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}}

%{?_with_rabbitmq:%description rabbitmq}
%{?_with_rabbitmq:%{dname} is a Clipper compatible compiler.}
%{?_with_rabbitmq:This package provides %{dname} rabbitmq-c bindings.}

######################################################################
## Preperation.
######################################################################

%prep
%setup -c %{name}
rm -rf "$RPM_BUILD_ROOT"

######################################################################
## Build.
######################################################################

%build
%{hb_env}

make %{?_smp_mflags}

######################################################################
## Install.
######################################################################

# Install Harbour itself.

%install
%{hb_env}

# necessary for shared linked hbmk2 used to execute postinst.hb
export LD_LIBRARY_PATH=$HB_INSTALL_LIB

make install %{?_smp_mflags}

%{?_without_curses:rm -f $HB_INSTALL_LIB/libgtcrs.a}
%{?_without_slang:rm -f $HB_INSTALL_LIB/libgtsln.a}
%{!?_with_localbz2:rm -f $HB_INSTALL_LIB/libbz2.a}
%{!?_with_localexpat:rm -f $HB_INSTALL_LIB/libexpat.a}
%{!?_with_locallibyaml:rm -f $HB_INSTALL_LIB/libyaml.a}
%{!?_with_localsqlite3:rm -f $HB_INSTALL_LIB/libsqlite3.a}
%{!?hb_ldconf:rm -fR $HB_INSTALL_ETC/ld.so.conf.d}
%{?hb_ldconf:rm -f $RPM_BUILD_ROOT/%{_libdir}/*.so*}
rm -f $RPM_BUILD_ROOT/%{_bindir}/{3rdpatch.hb,commit.hb,hb-uncrustify.cfg}
rm -f \
  $HB_INSTALL_LIB/libpng.a \
  $HB_INSTALL_LIB/libhpdf.a \
  $HB_INSTALL_LIB/liblzf.a \
  $HB_INSTALL_LIB/libminilzo.a \
  $HB_INSTALL_LIB/libsqlite3.a \
  $HB_INSTALL_LIB/libxdiff.a

######################################################################
## Post install/uninstall scripts
######################################################################
%post  lib
/sbin/ldconfig

%postun  lib
/sbin/ldconfig

%clean
######################################################################
## Clean.
######################################################################
rm -rf "$RPM_BUILD_ROOT"

######################################################################
## File list.
######################################################################
%files
%defattr(-,root,root,755)
%{_docdir}/*

%dir /
%dir /etc
%dir /usr
%dir %{hb_etcdir}
%verify(not md5 mtime) %config %{hb_etcdir}/hb-charmap.def
%{_bindir}/harbour
%{_bindir}/hbdoc
%{_bindir}/hbformat
%{_bindir}/hbi18n
%{_bindir}/hbmk2
%{_bindir}/hbnetio
%{_bindir}/hbpp
%{_bindir}/hbrun
%{_bindir}/hbspeed
%{_bindir}/hbtest
%{_mandir}/man1/*.1*
%dir %{_includedir}/%{name}
%attr(644,root,root) %{_includedir}/%{name}/*

%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libgt[^a]*.a
%{_libdir}/%{name}/libhbcommon.a
%{_libdir}/%{name}/libhbcpage.a
%{_libdir}/%{name}/libhbcplr.a
%{_libdir}/%{name}/libhbdebug.a
%{_libdir}/%{name}/libhbextern.a
%{_libdir}/%{name}/libhbhsx.a
%{_libdir}/%{name}/libhblang.a
%{_libdir}/%{name}/libhbmacro.a
%{_libdir}/%{name}/libhbnortl.a
%{_libdir}/%{name}/libhbnulrdd.a
%{_libdir}/%{name}/libhbpp.a
%{_libdir}/%{name}/libhbrdd.a
%{_libdir}/%{name}/libhbrtl.a
%{_libdir}/%{name}/libhbsix.a
%{_libdir}/%{name}/libhbusrrdd.a
%{_libdir}/%{name}/libhbvm.a
%{_libdir}/%{name}/libhbvmmt.a
%{_libdir}/%{name}/librddcdx.a
%{_libdir}/%{name}/librddfpt.a
%{_libdir}/%{name}/librddnsx.a
%{_libdir}/%{name}/librddntx.a
%{?_with_localpcre1:%{_libdir}/%{name}/libhbpcre.a}
%{?_with_localpcre2:%{_libdir}/%{name}/libhbpcre2.a}
%{?_with_localzlib:%{_libdir}/%{name}/libhbzlib.a}

%files lib
%defattr(755,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libharbour*.so*
%{!?hb_ldconf:%{_libdir}/libharbour*.so*}
%attr(644,root,root) %{?hb_ldconf:%{hb_ldconf}/%{name}.conf}

%files contrib
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/contrib
%{_datadir}/%{name}/contrib/contrib.hbr
%dir %{_datadir}/%{name}/contrib/3rd/sqlite3
%{_datadir}/%{name}/contrib/3rd/sqlite3/*
%{?_with_locallibyaml:%{_libdir}/%{name}/libsqlite3.a}
%dir %{_datadir}/%{name}/contrib/hbblink
%{_datadir}/%{name}/contrib/hbblink/*
%{_libdir}/%{name}/libhbblink.a
%dir %{_datadir}/%{name}/contrib/hbbz2
%{_datadir}/%{name}/contrib/hbbz2/*
%{?_with_localbz2:%{_libdir}/%{name}/libbz2.a}
%{_libdir}/%{name}/libhbbz2.a
%dir %{_datadir}/%{name}/contrib/hbbz2io
%{_datadir}/%{name}/contrib/hbbz2io/*
%{_libdir}/%{name}/libhbbz2io.a
%dir %{_datadir}/%{name}/contrib/hbcomio
%{_datadir}/%{name}/contrib/hbcomio/*
%{_libdir}/%{name}/libhbcomio.a
%dir %{_datadir}/%{name}/contrib/hbcomm
%{_datadir}/%{name}/contrib/hbcomm/*
%{_libdir}/%{name}/libhbcomm.a
%dir %{_datadir}/%{name}/contrib/hbct
%{_datadir}/%{name}/contrib/hbct/*
%{_libdir}/%{name}/libhbct.a
%dir %{_datadir}/%{name}/contrib/hbcrypto
%{_datadir}/%{name}/contrib/hbcrypto/*
%{_libdir}/%{name}/libhbcrypto.a
%{_libdir}/%{name}/libed25519.a
%{_libdir}/%{name}/libscrypt.a
%dir %{_datadir}/%{name}/contrib/hbexpat
%{_datadir}/%{name}/contrib/hbexpat/*
%{?_with_localexpat:%{_libdir}/%{name}/libexpat.a}
%{_libdir}/%{name}/libhbexpat.a
%dir %{_datadir}/%{name}/contrib/hbformat
%{_datadir}/%{name}/contrib/hbformat/*
%{_libdir}/%{name}/libhbformat.a
%dir %{_datadir}/%{name}/contrib/hbfoxpro
%{_datadir}/%{name}/contrib/hbfoxpro/*
%{_libdir}/%{name}/libhbfoxpro.a
%dir %{_datadir}/%{name}/contrib/hbfship
%{_datadir}/%{name}/contrib/hbfship/*
%{_libdir}/%{name}/libhbfship.a
%dir %{_datadir}/%{name}/contrib/hbgt
%{_datadir}/%{name}/contrib/hbgt/*
%{_libdir}/%{name}/libhbgt.a
%dir %{_datadir}/%{name}/contrib/hbgzio
%{_datadir}/%{name}/contrib/hbgzio/*
%{_libdir}/%{name}/libhbgzio.a
%dir %{_datadir}/%{name}/contrib/hbhpdf
%{_datadir}/%{name}/contrib/hbhpdf/*
%{_libdir}/%{name}/libhbhpdf.a
%dir %{_datadir}/%{name}/contrib/hbhttpd
%{_datadir}/%{name}/contrib/hbhttpd/*
%{_libdir}/%{name}/libhbhttpd.a
%dir %{_datadir}/%{name}/contrib/hblzf
%{_datadir}/%{name}/contrib/hblzf/*
%{_libdir}/%{name}/libhblzf.a
%dir %{_datadir}/%{name}/contrib/hbmemio
%{_datadir}/%{name}/contrib/hbmemio/*
%{_libdir}/%{name}/libhbmemio.a
%dir %{_datadir}/%{name}/contrib/hbmisc
%{_datadir}/%{name}/contrib/hbmisc/*
%{_libdir}/%{name}/libhbmisc.a
%dir %{_datadir}/%{name}/contrib/hbmlzo
%{_datadir}/%{name}/contrib/hbmlzo/*
%{_libdir}/%{name}/libhbmlzo.a
%dir %{_datadir}/%{name}/contrib/hbmxml
%{_datadir}/%{name}/contrib/hbmxml/*
%{_libdir}/%{name}/libhbmxml.a
%{_libdir}/%{name}/libmxml.a
%dir %{_datadir}/%{name}/contrib/hbmzip
%{_datadir}/%{name}/contrib/hbmzip/*
%{_libdir}/%{name}/libminizip.a
%{_libdir}/%{name}/libhbmzip.a
%dir %{_datadir}/%{name}/contrib/hbnetio
%{_datadir}/%{name}/contrib/hbnetio/*
%{_libdir}/%{name}/libhbnetio.a
%dir %{_datadir}/%{name}/contrib/hbnf
%{_datadir}/%{name}/contrib/hbnf/*
%{_libdir}/%{name}/libhbnf.a
%dir %{_datadir}/%{name}/contrib/hboslib
%{_datadir}/%{name}/contrib/hboslib/*
%{_libdir}/%{name}/libhboslib.a
%dir %{_datadir}/%{name}/contrib/hbpipeio
%{_datadir}/%{name}/contrib/hbpipeio/*
%{_libdir}/%{name}/libhbpipeio.a
%dir %{_datadir}/%{name}/contrib/hbsms
%{_datadir}/%{name}/contrib/hbsms/*
%{_libdir}/%{name}/libhbsms.a
%dir %{_datadir}/%{name}/contrib/hbsqlit3
%{_datadir}/%{name}/contrib/hbsqlit3/*
%{_libdir}/%{name}/libhbsqlit3.a
%dir %{_datadir}/%{name}/contrib/hbtcpio
%{_datadir}/%{name}/contrib/hbtcpio/*
%{_libdir}/%{name}/libhbtcpio.a
%dir %{_datadir}/%{name}/contrib/hbtest
%{_datadir}/%{name}/contrib/hbtest/*
%{_libdir}/%{name}/libhbtest.a
%dir %{_datadir}/%{name}/contrib/hbtip
%{_datadir}/%{name}/contrib/hbtip/*
%{_libdir}/%{name}/libhbtip.a
%dir %{_datadir}/%{name}/contrib/hbtpathy
%{_datadir}/%{name}/contrib/hbtpathy/*
%{_libdir}/%{name}/libhbtpathy.a
%dir %{_datadir}/%{name}/contrib/hbunix
%{_datadir}/%{name}/contrib/hbunix/*
%{_libdir}/%{name}/libhbunix.a
%dir %{_datadir}/%{name}/contrib/hbxpp
%{_datadir}/%{name}/contrib/hbxpp/*
%{_libdir}/%{name}/libhbxpp.a
%dir %{_datadir}/%{name}/contrib/hbxdiff
%{_datadir}/%{name}/contrib/hbxdiff/*
%{_libdir}/%{name}/libhbxdiff.a
%dir %{_datadir}/%{name}/contrib/hbyaml
%{_datadir}/%{name}/contrib/hbyaml/*
%{?_with_locallibyaml:%{_libdir}/%{name}/libyaml.a}
%{_libdir}/%{name}/libhbyaml.a
%dir %{_datadir}/%{name}/contrib/hbzebra
%{_datadir}/%{name}/contrib/hbzebra/*
%{_libdir}/%{name}/libhbzebra.a
%dir %{_datadir}/%{name}/contrib/hbziparc
%{_datadir}/%{name}/contrib/hbziparc/*
%{_libdir}/%{name}/libhbziparc.a
%dir %{_datadir}/%{name}/contrib/rddbm
%{_datadir}/%{name}/contrib/rddbm/*
%{_libdir}/%{name}/librddbm.a
%dir %{_datadir}/%{name}/contrib/rddmisc
%{_datadir}/%{name}/contrib/rddmisc/*
%{_libdir}/%{name}/librddmisc.a
%dir %{_datadir}/%{name}/contrib/rddsql
%{_datadir}/%{name}/contrib/rddsql/*
%{_libdir}/%{name}/librddsql.a
%dir %{_datadir}/%{name}/contrib/sddsqlt3
%{_datadir}/%{name}/contrib/sddsqlt3/*
%{_libdir}/%{name}/libsddsqlt3.a
%dir %{_datadir}/%{name}/contrib/xhb
%{_datadir}/%{name}/contrib/xhb/*
%{_libdir}/%{name}/libxhb.a

%{?_with_ads:%files ads}
%{?_with_ads:%defattr(644,root,root,755)}
%{?_with_ads:%dir %{_libdir}/%{name}}
%{?_with_ads:%dir %{_datadir}/%{name}}
%{?_with_ads:%dir %{_datadir}/%{name}/contrib}
%{?_with_ads:%dir %{_datadir}/%{name}/contrib/rddads}
%{?_with_ads:%{_libdir}/%{name}/librddads.a}
%{?_with_ads:%{_datadir}/%{name}/contrib/rddads/*}

%{?_with_cairo:%files cairo}
%{?_with_cairo:%defattr(644,root,root,755)}
%{?_with_cairo:%dir %{_libdir}/%{name}}
%{?_with_cairo:%dir %{_datadir}/%{name}}
%{?_with_cairo:%dir %{_datadir}/%{name}/contrib}
%{?_with_cairo:%dir %{_datadir}/%{name}/contrib/hbcairo}
%{?_with_cairo:%{_libdir}/%{name}/libhbcairo.a}
%{?_with_cairo:%{_datadir}/%{name}/contrib/hbcairo/*}

%{?_with_cups:%files cups}
%{?_with_cups:%defattr(644,root,root,755)}
%{?_with_cups:%dir %{_libdir}/%{name}}
%{?_with_cups:%dir %{_datadir}/%{name}}
%{?_with_cups:%dir %{_datadir}/%{name}/contrib}
%{?_with_cups:%dir %{_datadir}/%{name}/contrib/hbcups}
%{?_with_cups:%{_libdir}/%{name}/libhbcups.a}
%{?_with_cups:%{_datadir}/%{name}/contrib/hbcups/*}

%{?_with_curl:%files curl}
%{?_with_curl:%defattr(644,root,root,755)}
%{?_with_curl:%dir %{_libdir}/%{name}}
%{?_with_curl:%dir %{_datadir}/%{name}}
%{?_with_curl:%dir %{_datadir}/%{name}/contrib}
%{?_with_curl:%dir %{_datadir}/%{name}/contrib/hbcurl}
%{?_with_curl:%{_libdir}/%{name}/libhbcurl.a}
%{?_with_curl:%{_datadir}/%{name}/contrib/hbcurl/*}

%{?_with_firebird:%files firebird}
%{?_with_firebird:%defattr(644,root,root,755)}
%{?_with_firebird:%dir %{_libdir}/%{name}}
%{?_with_firebird:%dir %{_datadir}/%{name}}
%{?_with_firebird:%dir %{_datadir}/%{name}/contrib}
%{?_with_firebird:%dir %{_datadir}/%{name}/contrib/hbfbird}
%{?_with_firebird:%{_libdir}/%{name}/libhbfbird.a}
%{?_with_firebird:%{_libdir}/%{name}/libsddfb.a}
%{?_with_firebird:%{_datadir}/%{name}/contrib/sddfb/*}
%{?_with_firebird:%{_datadir}/%{name}/contrib/hbfbird/*}

%{?_with_freeimage:%files freeimage}
%{?_with_freeimage:%defattr(644,root,root,755)}
%{?_with_freeimage:%dir %{_libdir}/%{name}}
%{?_with_freeimage:%dir %{_datadir}/%{name}}
%{?_with_freeimage:%dir %{_datadir}/%{name}/contrib}
%{?_with_freeimage:%dir %{_datadir}/%{name}/contrib/hbfimage}
%{?_with_freeimage:%{_libdir}/%{name}/libhbfimage.a}
%{?_with_freeimage:%{_datadir}/%{name}/contrib/hbfimage/*}

%{?_with_gd:%files gd}
%{?_with_gd:%defattr(644,root,root,755)}
%{?_with_gd:%dir %{_libdir}/%{name}}
%{?_with_gd:%dir %{_datadir}/%{name}}
%{?_with_gd:%dir %{_datadir}/%{name}/contrib}
%{?_with_gd:%dir %{_datadir}/%{name}/contrib/hbgd}
%{?_with_gd:%{_libdir}/%{name}/libhbgd.a}
%{?_with_gd:%{_datadir}/%{name}/contrib/hbgd/*}

%{?_with_openssl:%files openssl}
%{?_with_openssl:%defattr(644,root,root,755)}
%{?_with_openssl:%dir %{_libdir}/%{name}}
%{?_with_openssl:%dir %{_datadir}/%{name}}
%{?_with_openssl:%dir %{_datadir}/%{name}/contrib}
%{?_with_openssl:%dir %{_datadir}/%{name}/contrib/hbssl}
%{?_with_openssl:%{_libdir}/%{name}/libhbssl.a}
%{?_with_openssl:%{_datadir}/%{name}/contrib/hbssl/*}

%{?_with_mysql:%files mysql}
%{?_with_mysql:%defattr(644,root,root,755)}
%{?_with_mysql:%dir %{_libdir}/%{name}}
%{?_with_mysql:%dir %{_datadir}/%{name}}
%{?_with_mysql:%dir %{_datadir}/%{name}/contrib}
%{?_with_mysql:%dir %{_datadir}/%{name}/contrib/hbmysql}
%{?_with_mysql:%dir %{_datadir}/%{name}/contrib/sddmy}
%{?_with_mysql:%{_libdir}/%{name}/libhbmysql.a}
%{?_with_mysql:%{_libdir}/%{name}/libsddmy.a}
%{?_with_mysql:%{_datadir}/%{name}/contrib/hbmysql/*}
%{?_with_mysql:%{_datadir}/%{name}/contrib/sddmy/*}

%{?_with_odbc:%files odbc}
%{?_with_odbc:%defattr(644,root,root,755)}
%{?_with_odbc:%dir %{_libdir}/%{name}}
%{?_with_odbc:%dir %{_datadir}/%{name}}
%{?_with_odbc:%dir %{_datadir}/%{name}/contrib}
%{?_with_odbc:%dir %{_datadir}/%{name}/contrib/hbodbc}
%{?_with_odbc:%dir %{_datadir}/%{name}/contrib/sddodbc}
%{?_with_odbc:%{_libdir}/%{name}/libhbodbc.a}
%{?_with_odbc:%{_libdir}/%{name}/libsddodbc.a}
%{?_with_odbc:%{_datadir}/%{name}/contrib/hbodbc/*}
%{?_with_odbc:%{_datadir}/%{name}/contrib/sddodbc/*}

%{?_with_pgsql:%files pgsql}
%{?_with_pgsql:%defattr(644,root,root,755)}
%{?_with_pgsql:%dir %{_libdir}/%{name}}
%{?_with_pgsql:%dir %{_datadir}/%{name}}
%{?_with_pgsql:%dir %{_datadir}/%{name}/contrib}
%{?_with_pgsql:%dir %{_datadir}/%{name}/contrib/hbpgsql}
%{?_with_pgsql:%dir %{_datadir}/%{name}/contrib/sddpg}
%{?_with_pgsql:%{_libdir}/%{name}/libhbpgsql.a}
%{?_with_pgsql:%{_libdir}/%{name}/libsddpg.a}
%{?_with_pgsql:%{_datadir}/%{name}/contrib/hbpgsql/*}
%{?_with_pgsql:%{_datadir}/%{name}/contrib/sddpg/*}

%{?_with_rabbitmq:%files rabbitmq}
%{?_with_rabbitmq:%defattr(644,root,root,755)}
%{?_with_rabbitmq:%dir %{_libdir}/%{name}}
%{?_with_rabbitmq:%dir %{_datadir}/%{name}}
%{?_with_rabbitmq:%dir %{_datadir}/%{name}/contrib}
%{?_with_rabbitmq:%dir %{_datadir}/%{name}/contrib/hbamqp}
%{?_with_rabbitmq:%{_libdir}/%{name}/libhbamqp.a}
%{?_with_rabbitmq:%{_datadir}/%{name}/contrib/hbamqp/*}

######################################################################
## Spec file Changelog.
######################################################################

%changelog
* Tue Mar 28 2017 Viktor Szakats (vsz.me/hb)
- lots of updates to sync with Harbour changes, see main ChangeLog.txt

* Tue Aug 05 2008 Viktor Szakats (vsz.me/hb)
- removed hbdot, hbverfix, hbpptest
- hbrun now fully replaces hbdot

* Thu Aug 23 2007 Przemyslaw Czerpak <druzus@priv.onet.pl>
+ added hbdot
- removed PP package

* Wed Mar 23 2005 Przemyslaw Czerpak <druzus@priv.onet.pl>
- removed bison and flex from dependences list

* Sat Aug 09 2003 Przemyslaw Czerpak <druzus@polbox.com>
- removed ${RPM_OPT_FLAGS} from HB_USER_CFLAGS

* Wed Jul 23 2003 Przemyslaw Czerpak <druzus@polbox.com>
- fixed file (user and group) owner for RPMs builded from non root account
- shared lib names changed from [x]harbour{mt,}.so to
  [x]harbour{mt,}-<version>.so and soft links with short names created
- 0.82 version set

* Wed Apr 30 2003 Przemyslaw Czerpak <druzus@polbox.com>
- new tool "hb-build" (hbcmp, hblnk, hbmk) added -
  compiler/linker wrapper.
- new tool "hb-mkdyn" (build shared libraries from static ones and object
  files).
- shared libraries added.
- binary package divided.

* Fri Mar 08 2002 Dave Pearson <davep@davep.org>
- Fixed gharbour so that it should work no matter the case of the name of
  the PRG file.

* Wed Feb 13 2002 Dave Pearson <davep@davep.org>
- Fixed a bug in harbour-link which meant that, since the environment
  changes of Jan 17 2002, users could not specify which GT library they
  wanted their application linked against.

* Tue Jan 22 2002 Dave Pearson <davep@davep.org>
- Used the "name" macro a lot more, especially in some paths.

* Thu Jan 17 2002 Dave Pearson <davep@davep.org>
- Removed the use of the /etc/profile.d scripts for setting the
  Harbour environment variables. The settings are now placed
  directly in gharbour and harbour-link. This means that this .spec
  file should be more useful on RPM using platforms other than RedHat.

* Wed Dec 19 2001 Dave Pearson <davep@davep.org>
- Added a platform ID to the name of the RPM.

* Mon Dec 17 2001 Dave Pearson <davep@davep.org>
- todo.txt is now called TODO.

* Tue Aug 21 2001 Dave Pearson <davep@davep.org>
- Added todo.txt as a doc file.

* Sun Jul 22 2001 Dave Pearson <davep@davep.org>
- harbour-link now fully respects the setting of $HB_GT_LIB.
- HB_GT_LIB wasn't set in the csh startup script. Fixed.

* Fri Jul 20 2001 Dave Pearson <davep@davep.org>
- Added the setting of $HB_GT_LIB to the environment (ncurses is used).
- Added support for installing hbmake.

* Thu Jun 28 2001 Dave Pearson <davep@davep.org>
- Changed the gharbour script so that it only invokes the C compiler if a C
  file was output. This stops any error messages when someone is using the
  -g option to output other target types.

* Mon Mar 19 2001 Dave Pearson <davep@davep.org>
- Reinstated hbrun in the files section.

* Tue Feb 20 2001 Dave Pearson <davep@davep.org>
- Added README.RPM to the documentation directory.

* Sat Jan 06 2001 Dave Pearson <davep@davep.org>
- The gharbour script now passes the Harbour include directory, using -I,
  to Harbour.

* Thu Aug 24 2000 Dave Pearson <davep@davep.org>
- Changed the files section so that hbrun doesn't get installed. It isn't
  useful on GNU/Linux systems.

* Tue Aug 22 2000 Dave Pearson <davep@davep.org>
- Changed the 'egcs' requirement to 'gcc'.

* Mon Aug 21 2000 Przemyslaw Czerpak <druzus@polbox.com>
- Polish translation added
- BuildRoot marco added. Now you can build the package from normal user
  account.
- bison and flex added to BuildPrereq list
- Debug information is stripped from installed files.

* Wed Aug 02 2000 Dave Pearson <davep@davep.org>
- Removed hbtest from the list of files installed into the bin directory.
- Added 'bash' and 'sh-utils' to the list of required packages.

* Tue Aug 01 2000 Dave Pearson <davep@davep.org>
- Added Harbour environment scripts to /etc/profile.d.
- Added generation of gharbour and harbour-link commands.

* Mon Jul 31 2000 Dave Pearson <davep@davep.org>
- Re-worked the layout of the spec file to make it cleaner and easier to
  read and maintain.
- The latest Harbour ChangeLog.txt is now installed into the RPM's doc
  directory.
- The content of the RPM's doc directory reflects the layout and content of
  the Harbour source's doc directory.
