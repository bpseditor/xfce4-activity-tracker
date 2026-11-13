import runpy,tempfile,json,time,contextlib,sys
from pathlib import Path
from unittest.mock import patch
import gi
gi.require_version('Gtk','3.0');gi.require_version('Gdk','3.0')
from gi.repository import Gtk,GLib,Gio,Gdk
m=runpy.run_path(str(Path(__file__).resolve().parents[1]/'activity-tracker'))
errors=[]
def walk(widget):
 yield widget
 if isinstance(widget,Gtk.Container):
  for child in widget.get_children(): yield from walk(child)
def save_image(win,path):
 window=win.get_window();p=Gdk.pixbuf_get_from_window(window,0,0,window.get_width(),window.get_height());p.savev(path,'png',[],[])
app=Gtk.Application(application_id='local.user.ActivityTrackerTest',flags=Gio.ApplicationFlags.NON_UNIQUE)
with tempfile.TemporaryDirectory() as d,patch.dict(m['settings'].__globals__,DATA=Path(d),CONFIG=Path(d)/'settings.json'):
 tid=m['add_timer']('A long timer name which must not force the window to grow',600)
 m['timer_action'](tid,'start')
 with contextlib.closing(m['database']()) as db,db:
  db.execute('INSERT INTO timer_usage VALUES(?,?,?,?)',(tid,'Firefox with a long application identifier',22,1))
  m['record'](db,time.time()-120,time.time(),'Firefox with a long application identifier',True)
 def fail(exc): errors.append(exc);app.quit()
 def timer_checks():
  try:
   win=app.get_active_window();widgets=list(walk(win));tabs=next(x for x in widgets if isinstance(x,Gtk.Notebook))
   assert tabs.get_current_page()==1
   def button(label): return next(x for x in widgets if isinstance(x,Gtk.Button) and x.get_label()==label)
   assert not button('Start').get_sensitive();assert button('Stop').get_sensitive()
   button('Pause').clicked();assert m['timers']()[0][5]=='paused';assert button('Resume').get_sensitive()
   button('Resume').clicked();assert m['timers']()[0][5]=='running'
   button('Stop').clicked();assert m['timers']()[0][5]=='stopped';assert m['timer_usage_rows'](tid)[0][1]==22
   with patch.object(Gtk.Dialog,'run',return_value=Gtk.ResponseType.CANCEL): button('Restart').clicked()
   assert m['timers']()[0][5]=='stopped'
   with patch.object(Gtk.Dialog,'run',return_value=Gtk.ResponseType.OK): button('Restart').clicked()
   assert m['timers']()[0][5]=='running';assert m['timer_usage_rows'](tid)==[]
   button('Pause').clicked()
   def settings_checks():
    try:
     save_image(win,'/tmp/tracker-timers.png');tabs.set_current_page(2)
     font=next(x for x in widgets if isinstance(x,Gtk.FontButton));font.set_font('Sans 12');font.emit('font-set')
     pause=button('Pause tracking');pause.set_active(True)
     order_view=next(x for x in widgets if isinstance(x,Gtk.TreeView) and x.get_model().get_n_columns()==3 and x.get_model().get_column_type(2).name=='gboolean')
     model=order_view.get_model();model.swap(model.get_iter_first(),model.get_iter(Gtk.TreePath.new_from_indices([1])))
     idle_combo=next(x for x in widgets if isinstance(x,Gtk.ComboBoxText) and x.get_active_id()=='media');idle_combo.set_active_id('foreground')
     assert button('Apply preferences').get_sensitive();button('Apply preferences').clicked()
     cfg=m['settings']();assert cfg['paused'];assert cfg['panel_font']=='Sans 12';assert cfg['panel_order'].startswith('app,timer');assert cfg['idle_mode']=='foreground'
     assert not button('Apply preferences').get_sensitive()
     def finish():
      save_image(win,'/tmp/tracker-settings.png');win.destroy();app.quit();return False
     GLib.timeout_add(200,finish)
    except Exception as e: fail(e)
    return False
   GLib.timeout_add(200,settings_checks)
  except Exception as e: fail(e)
  return False
 def activate(app):
  m['build_window'](app);GLib.timeout_add(200,timer_checks)
 app.connect('activate',activate);app.run([])
if errors: raise errors[0]
print('GTK: pause/resume/stop/restart confirmation, stats retention, font, order, idle mode and preference preservation verified')
