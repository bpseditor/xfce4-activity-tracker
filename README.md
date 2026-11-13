# Activity Tracker

XFCE/X11 Genmon widget using Python 3, GTK3/PyGObject, Wnck, Xfconf, libX11, libXss, SQLite and notify-send.

```sh
python3 install.py
```

Run in the logged-in XFCE session. The installer adds Genmon and session autostart. It needs xfce4-genmon-plugin and the dependencies above; no sudo is used.

Wnck identifies the active application once per second. The panel shows its accumulated time today. The window lists application usage and lets you mark distracting apps. Tracking stops after 60 seconds without input and during XFCE screen lock. Browsers are counted as whole apps. Window titles, URLs and keystrokes are not recorded.

Named timers support start, pause, reset and completion notifications. Deadlines continue during idle and sleep; notifications are delivered when the collector runs. System clock changes affect running timers. Timers appear in the tooltip and Timers tab.

Data stays in `~/.local/share/xfce4-activity-tracker/` (or XDG_DATA_HOME). Panel backups: `~/.local/state/xfce4-activity-tracker/`. `activity-tracker --report` prints 30 days as JSON. Remove the Genmon item and autostart entry to disable startup. Existing statistics remain local.

Tests: `python3 -m unittest discover`. Optional panel CSS: `panel.css`.
