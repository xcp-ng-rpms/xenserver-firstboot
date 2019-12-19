Summary: XenServer scripts to run first time machine is booted
Name: xenserver-firstboot
Version: 1.0.14
Release: 1
License: GPL
Group: System Environment/Base
URL: http://www.citrix.com

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/xenserver-firstboot/archive?at=v1.0.14&format=tar.gz&prefix=xenserver-firstboot-1.0.14#/xenserver-firstboot-1.0.14.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/xenserver-firstboot/archive?at=v1.0.14&format=tar.gz&prefix=xenserver-firstboot-1.0.14#/xenserver-firstboot-1.0.14.tar.gz) = 093ea93d9fd5ba9d4aff17216406e40363560e45

BuildArch: noarch
Requires(post): systemd
Requires: /opt/xensource/bin/xe systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: security-tools
BuildRequires: systemd-units

%description
XenServer scripts to run first time machine is booted


%prep
%autosetup -p1

%build
true

%install
mkdir -p -m 755 %{buildroot}/opt/xensource/lib
mkdir -p -m 755 %{buildroot}/etc/firstboot.d/{data,state,log}
mkdir -p -m 755 %{buildroot}/%{_unitdir}
mkdir -p -m 755 %{buildroot}/sbin

install -m 644 -t %{buildroot}/opt/xensource/lib    lib/*
install -m 755 -t %{buildroot}/etc/firstboot.d      firstboot.d/??-*
install -m 644 -t %{buildroot}/etc/firstboot.d/data firstboot.d/data/*
install -m 644 -t %{buildroot}/%{_unitdir} systemd/xs-firstboot.service
install -m 755 -t %{buildroot}/sbin/ sbin/xs-firstboot

%post
%systemd_post xs-firstboot.service

%preun
%systemd_preun xs-firstboot.service

%postun
%systemd_postun_with_restart xs-firstboot.service

%files
%defattr(-,root,root,-)
/etc/firstboot.d/??-*
%dir /etc/firstboot.d/state
%dir /etc/firstboot.d/log
/opt/xensource/lib/storage-creation-utils.sh
%config /etc/firstboot.d/data/*
%{_unitdir}/xs-firstboot.service
/sbin/xs-firstboot

%changelog
* Thu Oct 24 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.14-1
- CA-327140: Make plugging of PIFs best-effort

* Thu Jul 04 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.13-1
- CA-322079: Reinstate PBIS nsswitch changes after dom0 upgrade

* Tue May 28 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.12-1
- CA-260176: Use DNS settings after network reset

* Thu Dec 06 2018 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.0.11-1
- CA-303371 Use NetApp standard NFS ports in CC firewall rules

* Fri Oct 12 2018 Deli Zhang <deli.zhang@citrix.com> - 1.0.10-1
- CP-29090: CC configuration for firewall, network label, xapi client and pool secret
