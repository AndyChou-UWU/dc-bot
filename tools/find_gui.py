import psutil
found=False
for p in psutil.process_iter(['pid','name','cmdline']):
    try:
        cmd = p.info.get('cmdline') or []
        if any('gui_monitor.py' in s for s in cmd):
            print('PID', p.info['pid'], 'cmdline=', cmd)
            found=True
    except Exception:
        pass
if not found:
    print('No gui_monitor.py process found')
