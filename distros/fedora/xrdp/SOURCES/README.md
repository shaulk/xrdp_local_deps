Downgrade from 0.10.x to 0.9.x
==

Version 0.10.x requires different permissions of `/run/xrdp` directory than
version 0.9.x. When 0.10.x is fully uninstalled, this directory is removed
and subsequent installation of 0.9.x should work fine.

However, if 0.10.x is downgraded to 0.9.x, the directory is preserved,
because we could have xrdp and its sessions still running, so subsequent start
or restart will fail, unless the permissions of `/run/xrdp` directory are
changed to 1777 beforehand.

Unprivileged xrdp user in 0.10.2 and up
==

Recent builds of xrdp (0.10.2 and above) create local unprivileged xrdp user,
which is used to run xrdp daemon. Script `/usr/share/xrdp/xrdp-chkpriv` checks
whether `/etc/xrdp/key.pem`, `/etc/xrdp/cert.pem` and `/etc/xrdp/rsakeys.ini`
files have correct ownership and permissions. It also makes sure
`/etc/xrdp/xrdp.ini` and `/etc/xrdp/sesman.ini` agree on which group is used
for unprivileged user.

If you are upgrading from previous version of xrdp and you already have all
these files, you may need to adjust them by hand after running this script.
For clean installs, these files should be created with correct ownership and
permissions.

Restarts
==

Service restarts after RPM package upgrades have been disabled on purpose.
This is to avoid a situation where an update is performed from within a
session running on xrdp, which can then cause dnf to only perform part of the
transaction and leave the system in a state that requires further manual
intervention, including removal of duplicate packages etc.

So, it will be up to the user/admin to restart xrdp service after any RPM
package upgrade. This is in line with what other GUI systems like Xorg and
Wayland do.

xorgxrdp
==

Note that xorgxrdp is not installed and configured by default. Each build
depends on specific binary version of Xorg. If you wish to use it, install
it by hand or its glamor build.

SELinux
==

You may need to install xrdp-selinux package in order to get the required
SELinux policy that will allow xrdp and associated processes to run
successfully if SELinux is enabled. On versions of Fedora and RHEL that support
weak dependencies, xrdp-selinux will be a recommended package.

**WARNING**: The policy module contains a rule that permits
unconfined_service_t processes to transition into unconfined_t. If xrdp is not
the only service that runs as unconfined_service_t on your system, this policy
will allow any other such service to transition as well.

Default configuration in `/etc/pam.d/xrdp-sesman` uses password-auth for auth,
account, password and session. This may result in an incorrect context for the
processes in the session. Please adjust this file to match your desktop
environment. An example for Gnome desktop is given in the file.

TigerVNC >= 1.8.0
==

TigerVNC 1.8.0 enables clipboard support by default (i.e. no need to run
vncconfig), which may cause disconnections in xrdp. To avoid the issue, these
can be added to [Xvnc] stanza in `/etc/xrdp/sesman.ini`:
```
param=-AcceptCutText=0
param=-SendCutText=0
param=-SendPrimary=0
param=-SetPrimary=0
```

Of course, cut and paste support will not work with these set.

Runlevel
==

If the system is configured to boot into graphical target, you may experience
problems with xrdp Gnome sessions. In order to avoid this, put the system into
multi user target. Like this:
```
systemctl set-default multi-user.target
```

Then reboot.

VSOCK
==

An example of a how to set up xrdp with VSOCK can be found here:

https://bugzilla.redhat.com/show_bug.cgi?id=1787953#c22

Polkit rules for active sessions, allowing access to colord and repository
updates are already shipped, but in a current, JavaScript format.

KDE Plasma
==

If you are using plasma-workspace package with xrdp, be sure to install
plasma-workspace-x11 to get full functionality. See this for more details:

https://github.com/neutrinolabs/xrdp/issues/3395
