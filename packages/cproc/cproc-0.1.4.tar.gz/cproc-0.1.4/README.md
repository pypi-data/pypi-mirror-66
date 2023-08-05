# Capture Process (cproc)

Capture the environment and other key values about a running process into an cproc
info file (JSON).
It is meant as a tool for system administration to do system probing.
A captured process info file can be used as input to another program or do other
things like respawning the process in the same type of environment.

## Capture
```json
$ cproc `pidof inkscape` -p
{
    "target": {
        "pid": 20334,
        "name": "inkscape",
        "cmdline": [
            "/usr/bin/inkscape"
        ],
        "cwd": "/home/jakob",
        "environ": {
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
            "DEFAULTS_PATH": "/usr/share/gconf//usr/share/xsessions/plasma.default.path",
            "DESKTOP_SESSION": "/usr/share/xsessions/plasma",
            "DISPLAY": ":0",
            "GPG_AGENT_INFO": "/run/user/1000/gnupg/S.gpg-agent:0:1",
            "HOME": "/home/jakob",
            "KDE_FULL_SESSION": "true",
            "KDE_SESSION_UID": "1000",
            "KDE_SESSION_VERSION": "5",
            "LANG": "da_DK.UTF-8",
            "LOGNAME": "jakob",
            "MANDATORY_PATH": "/usr/share/gconf//usr/share/xsessions/plasma.mandatory.path",
            "PAM_KWALLET5_LOGIN": "/run/user/1000/kwallet5.socket",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin",
            "PWD": "/home/jakob",
            "QT_ACCESSIBILITY": "1",
            "QT_AUTO_SCREEN_SCALE_FACTOR": "0",
            "SHELL": "/bin/bash",
            "SHLVL": "0",
            "SSH_AGENT_PID": "3154",
            "SSH_AUTH_SOCK": "/tmp/ssh-dqusF25dBMTe/agent.3073",
            "USER": "jakob",
            "XAUTHORITY": "/tmp/xauth-1000-_0",
            "XCURSOR_THEME": "breeze_cursors",
            "XDG_CONFIG_DIRS": "/etc/xdg/xdg-/usr/share/xsessions/plasma:/etc/xdg",
            "XDG_CURRENT_DESKTOP": "KDE",
            "XDG_DATA_DIRS": "/usr/share//usr/share/xsessions/plasma:/home/jakob/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share:/var/lib/snapd/desktop",
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "XDG_SEAT": "seat0",
            "XDG_SEAT_PATH": "/org/freedesktop/DisplayManager/Seat0",
            "XDG_SESSION_CLASS": "user",
            "XDG_SESSION_DESKTOP": "KDE",
            "XDG_SESSION_ID": "4",
            "XDG_SESSION_PATH": "/org/freedesktop/DisplayManager/Session1",
            "XDG_SESSION_TYPE": "x11",
            "XDG_VTNR": "1",
            "GTK_RC_FILES": "/etc/gtk/gtkrc:/home/jakob/.gtkrc:/home/jakob/.config/gtkrc",
            "GTK2_RC_FILES": "/etc/gtk-2.0/gtkrc:/home/jakob/.gtkrc-2.0:/home/jakob/.config/gtkrc-2.0",
            "SESSION_MANAGER": "local/jakob-hp-zbook:@/tmp/.ICE-unix/3224,unix/jakob-hp-zbook:/tmp/.ICE-unix/3224",
            "LANGUAGE": "",
            "DESKTOP_STARTUP_ID": "jakob-hp-zbook;1587202863;324799;12856_TIME10556835"
        },
        "uids": [
            1000,
            1000,
            1000
        ],
        "gids": [
            1000,
            1000,
            1000
        ],
        "exe": "/usr/bin/inkscape"
    },
    "toplevel": {
        "pid": 3174,
        "name": "kdeinit5",
        "cmdline": [
            "kdeinit5: Running...",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "cwd": "/home/jakob",
        "environ": {},
        "uids": [
            1000,
            1000,
            1000
        ],
        "gids": [
            1000,
            1000,
            1000
        ],
        "exe": "/usr/bin/kdeinit5"
    },
    "parent": {
        "pid": 12856,
        "name": "krunner",
        "cmdline": [
            "/usr/bin/krunner"
        ],
        "cwd": "/home/jakob",
        "environ": {
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
            "DEFAULTS_PATH": "/usr/share/gconf//usr/share/xsessions/plasma.default.path",
            "DESKTOP_SESSION": "/usr/share/xsessions/plasma",
            "DISPLAY": ":0",
            "GPG_AGENT_INFO": "/run/user/1000/gnupg/S.gpg-agent:0:1",
            "HOME": "/home/jakob",
            "KDE_FULL_SESSION": "true",
            "KDE_SESSION_UID": "1000",
            "KDE_SESSION_VERSION": "5",
            "LANG": "da_DK.UTF-8",
            "LOGNAME": "jakob",
            "MANDATORY_PATH": "/usr/share/gconf//usr/share/xsessions/plasma.mandatory.path",
            "PAM_KWALLET5_LOGIN": "/run/user/1000/kwallet5.socket",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin",
            "PWD": "/home/jakob",
            "QT_ACCESSIBILITY": "1",
            "QT_AUTO_SCREEN_SCALE_FACTOR": "0",
            "SHELL": "/bin/bash",
            "SHLVL": "0",
            "SSH_AGENT_PID": "3154",
            "SSH_AUTH_SOCK": "/tmp/ssh-dqusF25dBMTe/agent.3073",
            "USER": "jakob",
            "XAUTHORITY": "/tmp/xauth-1000-_0",
            "XCURSOR_THEME": "breeze_cursors",
            "XDG_CONFIG_DIRS": "/etc/xdg/xdg-/usr/share/xsessions/plasma:/etc/xdg",
            "XDG_CURRENT_DESKTOP": "KDE",
            "XDG_DATA_DIRS": "/usr/share//usr/share/xsessions/plasma:/home/jakob/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share:/var/lib/snapd/desktop",
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "XDG_SEAT": "seat0",
            "XDG_SEAT_PATH": "/org/freedesktop/DisplayManager/Seat0",
            "XDG_SESSION_CLASS": "user",
            "XDG_SESSION_DESKTOP": "KDE",
            "XDG_SESSION_ID": "4",
            "XDG_SESSION_PATH": "/org/freedesktop/DisplayManager/Session1",
            "XDG_SESSION_TYPE": "x11",
            "XDG_VTNR": "1",
            "GTK_RC_FILES": "/etc/gtk/gtkrc:/home/jakob/.gtkrc:/home/jakob/.config/gtkrc",
            "GTK2_RC_FILES": "/etc/gtk-2.0/gtkrc:/home/jakob/.gtkrc-2.0:/home/jakob/.config/gtkrc-2.0",
            "SESSION_MANAGER": "local/jakob-hp-zbook:@/tmp/.ICE-unix/3224,unix/jakob-hp-zbook:/tmp/.ICE-unix/3224"
        },
        "uids": [
            1000,
            1000,
            1000
        ],
        "gids": [
            1000,
            1000,
            1000
        ],
        "exe": "/usr/bin/krunner"
    }
}
```

## Spawn
Re-spawn a process based on cproc output.
First capture the process:
```
cproc `pidof inkscape` -p > inkscape.cproc
```
Then re-spawn it using rproc:
```
rproc inkscape.cproc
```
It is also possible to invoke the parent that started the process:
```
rproc inkscape.cproc -p
```
Or even the toplevel process that invoked the captured process:
```
rproc inkscape.cproc -t
```
In some cases (mainly if starting a GUI application) you want to enherit your current environment. This is possible like
this:
```
rproc inkscape.cproc -e
```
Environment variables captured by cproc will override existing environment keys.
