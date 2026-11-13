# Activity Tracker

Local XFCE/X11 application tracking and named countdown timers. Requires Python 3, GTK3/PyGObject, Wnck, Xfconf, libX11, libXss, Genmon and notify-send.

```sh
python3 install.py
python3 -m unittest discover
```

The panel shows shortened application/timer names and compact counters. Hover for full names, daily totals, session statistics, tracking state and other running timers. Names are limited in both timer and ordinary modes. The Panel tab controls the font and size, maximum name length, visible fields and their order (drag or arrows). Display/idle preferences use an explicit Apply button and atomic saving. Closing with pending changes offers to keep editing or discard them. Tracking pause and distracting-app flags take effect immediately.

## Tracking

Only the focused application is counted. By default, 60 seconds without keyboard/mouse input becomes idle **unless that application reports playing media over MPRIS**. This allows Firefox video playback to count without moving the mouse. Playback in another application does not keep the focused app active. Media status is read asynchronously; no media titles, window titles, URLs or keystrokes are stored.

The Tracking tab provides three modes: foreground media support (default), input-only, and always count the focused application. The last mode also counts reading without input, even if the person has walked away. The idle timeout is configurable. Screen lock and manual tracking pause override every mode. Apps that do not expose MPRIS playback need focused-app mode for passive viewing. Playback changes take up to a few seconds to be detected.

The collector excludes suspend gaps and clock jumps from application accounting. The Activity table supports application search and numeric sorting of time/visits; full truncated names are available on hover. Daily totals and timer totals remain independent.

## Timers

Create a named timer or use a preset; the new timer is selected automatically. Enter in the name field also creates a timer. Clicking the panel opens the existing window and selects the timer tab on initial opening when a timer is running or paused.

- **Start / Resume**: begin counting down or continue a paused session.
- **Pause**: freeze the countdown and keep session statistics; paused timers remain visible on the panel.
- **Stop**: end the session early and keep its remaining time and application statistics for inspection.
- **Restart**: start a fresh full-duration session after stopping or finishing; asks before clearing that timer's previous statistics.
- **Reset / Delete**: clear a timer session or remove the timer, with confirmation. Daily application totals are preserved.

Buttons reflect the selected timer's state. Each running timer independently counts application activity inside its start/resume intervals. Multiple timers are supported; the first running timer appears in the panel and others appear in its tooltip. If none runs, the first paused timer is shown. The panel's app counter is session time during a timer; its independent daily counter remains in the tooltip.

Countdowns continue during sleep, input inactivity and tracking pause. Completion notifications require the collector; after suspend they arrive when it resumes. Wall-clock changes affect countdown deadlines.

Data and settings stay in `~/.local/share/xfce4-activity-tracker/` (or XDG_DATA_HOME). Existing history and timers are preserved on schema upgrade. Reinstalling files does not replace an already running collector; restart that process or log back into XFCE after an upgrade. `activity-tracker --report` prints 30 days as JSON. Remove the panel item and autostart entry to disable startup without deleting statistics.

Optional GTK interaction check (opens temporary test windows without touching user data): `python3 tests/gui_smoke.py`.

## Daily history and statistics

The date controls above the tabs apply to both Activity and Statistics. Choose Today, Last 7/30 days, or a specific calendar date; the arrows move by one day. The Statistics tab shows recorded time, application counts and horizontal bars with each app’s share. Hover for exact time and visit counts. Empty days are explicitly identified. History exists only for days when the collector was running.
