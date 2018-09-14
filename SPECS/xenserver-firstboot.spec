Summary: XenServer scripts to run first time machine is booted
Name: xenserver-firstboot
Version: 1.0.9
Release: 1.1.xcp
License: GPL
Group: System Environment/Base
URL: http://www.citrix.com
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
BuildArch: noarch
Requires(post): systemd
Requires: /opt/xensource/bin/xe systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd-units

%description
XenServer scripts to run first time machine is booted


%prep
%autosetup -p1

%build

%install
mkdir -p -m 755 %{buildroot}/opt/xensource/lib
mkdir -p -m 755 %{buildroot}/etc/firstboot.d/{data,state,log}
mkdir -p -m 755 %{buildroot}/%{_unitdir}
mkdir -p -m 755 %{buildroot}/sbin
mkdir -p -m 755 %{buildroot}%{_datadir}/xenserver-firstboot

install -m 644 -t %{buildroot}/opt/xensource/lib    lib/*
install -m 755 -t %{buildroot}/etc/firstboot.d      firstboot.d/??-*
install -m 644 -T firstboot.d/data/firstboot_in_progress %{buildroot}%{_datadir}/xenserver-firstboot/firstboot_in_progress.dist
install -m 644 -t %{buildroot}/%{_unitdir} systemd/xs-firstboot.service
install -m 755 -t %{buildroot}/sbin/ sbin/xs-firstboot

%post
%systemd_post xs-firstboot.service
if [ $1 = 1 ]; then
    # initial installation
    install -m 644 %{_datadir}/xenserver-firstboot/firstboot_in_progress.dist /etc/firstboot.d/data/firstboot_in_progress || :
fi

%preun
%systemd_preun xs-firstboot.service

%postun
%systemd_postun_with_restart xs-firstboot.service

%triggerun -- xenserver-firstboot < 1.0.7
# Fix warning due to xenserver-firstboot 1.0.6 owning a file
# that another program removed: /etc/firstboot.d/data/firstboot_in_progress
# We add the file back just in time for it to be removed cleanly
touch /etc/firstboot.d/data/firstboot_in_progress || :

%files
%defattr(-,root,root,-)
/etc/firstboot.d/??-*
%dir /etc/firstboot.d/state
%dir /etc/firstboot.d/log
/opt/xensource/lib/storage-creation-utils.sh
%{_datadir}/xenserver-firstboot/firstboot_in_progress.dist
%{_unitdir}/xs-firstboot.service
/sbin/xs-firstboot
