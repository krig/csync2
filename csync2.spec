# csync2 - cluster synchronization tool, 2nd generation
# Copyright (C) 2004 - 2015 LINBIT Information Technologies GmbH
# http://www.linbit.com; see also AUTHORS
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

#
# spec file for package csync2 (Version 2.0)
#

# norootforbuild
# neededforbuild  openssl openssl-devel

BuildRequires: sqlite-devel sqlite librsync gnutls-devel librsync-devel

Name:         csync2
License:      GPL
Group:        System/Monitoring
Requires:     sqlite openssl librsync
Autoreqprov:  on
Version: 2.0
Release:      1
Source0:      csync2-%{version}.tar.gz
URL:          http://oss.linbit.com/csync2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Summary:      Cluster sync tool

%description
Csync2 is a cluster synchronization tool. It can be used to keep files on
multiple hosts in a cluster in sync. Csync2 can handle complex setups with
much more than just 2 hosts, handle file deletions and can detect conflicts.
It is expedient for HA-clusters, HPC-clusters, COWs and server farms.

%prep
%setup
%{?suse_update_config:%{suse_update_config}}

%build
export CFLAGS="$RPM_OPT_FLAGS -I/usr/kerberos/include"
if ! [ -f configure ]; then ./autogen.sh; fi
%configure --enable-mysql --enable-postgres --enable-sqlite3

make all

%install
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/csync2
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d

%makeinstall

install -m 644 csync2.xinetd $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/csync2
install -m 644 doc/csync2.adoc $RPM_BUILD_ROOT%{_docdir}/csync2/csync2.adoc

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
make clean

%post
if ! grep -q "^csync2" %{_sysconfdir}/services ; then
     echo "csync2          30865/tcp" >>%{_sysconfdir}/services
fi

%files
%defattr(-,root,root)
%{_sbindir}/csync2
%{_sbindir}/csync2-compare
%{_var}/lib/csync2
%doc %{_mandir}/man1/csync2.1.gz
%doc %{_docdir}/csync2/csync2.adoc
%doc %{_docdir}/csync2/ChangeLog
%doc %{_docdir}/csync2/README
%doc %{_docdir}/csync2/AUTHORS
%config(noreplace) %{_sysconfdir}/xinetd.d/csync2
%config(noreplace) %{_sysconfdir}/csync2.cfg

%changelog
* Tue Jan 27 2015 Lars Ellenberg <lars.ellenberg@linbit.com> - 2.0-1
- New upstream release
