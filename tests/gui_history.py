import runpy,tempfile,contextlib,datetime,json
from pathlib import Path
from unittest.mock import patch
import gi
gi.require_version('Gtk','3.0');gi.require_version('Gdk','3.0')
from gi.repository import Gtk,GLib,Gio,Gdk
m=runpy.run_path(str(Path(__file__).resolve().parents[1]/'activity-tracker'))
art=Path.home()/'.local/state/widget-ui-review';art.mkdir(exist_ok=True)
errors=[]
def walk(w):
 yield w
 if isinstance(w,Gtk.Container):
  for c in w.get_children():yield from walk(c)
def shot(w,name):
 x=w.get_window();p=Gdk.pixbuf_get_from_window(x,0,0,x.get_width(),x.get_height());p.savev(str(art/name),'png',[],[])
app=Gtk.Application(application_id='local.user.HistoryVisualTest',flags=Gio.ApplicationFlags.NON_UNIQUE)
with tempfile.TemporaryDirectory() as d,patch.dict(m['settings'].__globals__,DATA=Path(d),CONFIG=Path(d)/'settings.json'):
 with contextlib.closing(m['database']()) as db,db:
  db.executemany('INSERT INTO usage VALUES(?,?,?,?)',[('2026-11-10',name,secs,visits) for name,secs,visits in [('Firefox',7200,24),('Visual Studio Code — a very long application name',3600,12),('Terminal',1800,8),('Telegram',900,15),('Files',300,4)] ]+[('2026-11-09','Editor',3600,2)])
 def activate(app):
  m['build_window'](app)
  def check():
   try:
    win=app.get_active_window();ws=list(walk(win));tabs=next(w for w in ws if isinstance(w,Gtk.Notebook));cal=next(w for w in ws if isinstance(w,Gtk.Calendar)) if any(isinstance(w,Gtk.Calendar) for w in ws) else None
    # Popovers are attached widgets, not normal container descendants.
    date=next(w for w in ws if isinstance(w,Gtk.MenuButton));cal=date.get_popover().get_child()
    cal.select_month(10,2026);cal.select_day(10)
    summary=next(w for w in ws if isinstance(w,Gtk.Label) and 'Recorded:' in w.get_text())
    assert '03:50:00' in summary.get_text(),summary.get_text()
    tabs.set_current_page(0)
    def table():
     shot(win,'activity-day.png');tabs.set_current_page(4)
     def graph():
      shot(win,'activity-statistics.png')
      bars=[w for w in walk(win) if isinstance(w,Gtk.ProgressBar)]
      assert len(bars)==5;assert abs(sum(w.get_fraction() for w in bars)-1)<1e-8
      cal.select_day(1)
      def empty():
       shot(win,'activity-empty.png');assert any(w.get_visible() and 'No recorded activity' in w.get_text() for w in walk(win) if isinstance(w,Gtk.Label))
       date.set_active(True)
       def calendar():
        shot(win,'activity-calendar.png');win.destroy();app.quit();return False
       GLib.timeout_add(200,calendar);return False
      GLib.timeout_add(200,empty);return False
     GLib.timeout_add(200,graph);return False
    GLib.timeout_add(200,table)
   except Exception as exc: errors.append(exc);app.quit()
   return False
  GLib.timeout_add(250,check)
 app.connect('activate',activate);app.run([])
if errors:raise errors[0]
print('Specific date, totals, graph fractions, calendar and empty day verified; screenshots:',art)
