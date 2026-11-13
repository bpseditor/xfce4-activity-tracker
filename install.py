#!/usr/bin/python3
import pathlib, shutil, subprocess, json, datetime
root=pathlib.Path(__file__).resolve().parent
home=pathlib.Path.home()
binary=home/'.local/bin/activity-tracker'; binary.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'activity-tracker',binary)
for folder,args,name in [('.config/autostart','--daemon','Activity Tracker collector'),('.local/share/applications','--window','Activity Tracker')]:
    path=home/folder/'activity-tracker.desktop'; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'[Desktop Entry]\nType=Application\nName={name}\nExec="{binary}" {args}\nIcon=preferences-system-time\nTerminal=false\nOnlyShowIn=XFCE;\nCategories=Utility;\n')
import gi
gi.require_version('Xfconf','0')
from gi.repository import Xfconf
Xfconf.init(); ch=Xfconf.Channel.get('xfce4-panel'); props=ch.get_properties('/')
backup=home/'.local/state/xfce4-activity-tracker'; backup.mkdir(parents=True,exist_ok=True)
(backup/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.json')).write_text(json.dumps({k:v if isinstance(v,(str,int,bool,float)) else list(ch.get_arrayv(k)) for k,v in props.items()},indent=2))
if str(binary) not in props.values():
    ids=[int(k.split('/')[2][7:]) for k in props if k.startswith('/plugins/plugin-')]
    plugin=max(ids,default=0)+1; prefix=f'/plugins/plugin-{plugin}'
    def setprop(key,typ,val): subprocess.run(['xfconf-query','-c','xfce4-panel','-p',key,'-n','-t',typ,'-s',str(val)],check=True)
    setprop(prefix,'string','genmon')
    for key,typ,val in [('command','string',binary),('use-label','bool','false'),('update-period','int',1000),('font','string','Inter Medium 10'),('enable-single-row','bool','true')]: setprop(prefix+'/'+key,typ,val)
    panel=sorted(k for k in props if k.startswith('/panels/') and k.endswith('/plugin-ids'))[0]
    values=list(ch.get_arrayv(panel)); values.append(plugin)
    cmd=['xfconf-query','-c','xfce4-panel','-p',panel,'--force-array']
    for value in values: cmd+=['-t','int','-s',str(value)]
    subprocess.run(cmd,check=True)
    subprocess.Popen(['xfce4-panel','--restart'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
log=open(backup/'collector.log','a')
subprocess.Popen([str(binary),'--daemon'],stdout=log,stderr=log,start_new_session=True)
print('Installed activity tracker and enabled session autostart.')
