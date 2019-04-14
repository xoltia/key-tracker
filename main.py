import sqlite3
import keyboard
import mouse
import argparse
import time
import os
import shutil
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--log', '-log', '-l', help="Log key/mouse events", action="store_true")
parser.add_argument('--backup', '-b', type=float, required=False, help="How often a backup is made")
args = parser.parse_args()

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

current_recording = {}
record = False
last_dump = None
def start_recording():
    global record
    record = not record
    print('Started recording' if record else 'Stopped recording')
    if not record:
        dump_recording()
def dump_recording():
    global record
    global current_recording
    global last_dump
    log_folder = f'logs/{datetime.date.today()}'
    dump_file = f'keys-{time.time()}.log'
    with open(f'{ensure_dir(log_folder)}/{dump_file}', 'w+') as log:
        for k, v in current_recording.items():
            log.write(f'{k}: {v}\n')
    current_recording = {}
    record = False
    last_dump = f"{log_folder}/{dump_file}"
    print(f'Recording dumped to {dump_file}\nPress ctrl+shift+o to open last recording in notepad')

def open_dump():
    if not last_dump:
        print('You do not have any saved recordings this session')
    else:
        os.system(f'notepad {last_dump}')

keyboard.add_hotkey('ctrl+shift+a', start_recording)
keyboard.add_hotkey('ctrl+shift+o', open_dump)

being_held = []
def on_key_press(event):
    global record
    key = event.name.lower() if event.name.isalpha() else event.name
    if event.event_type == keyboard.KEY_UP:
        being_held.remove(key)
    if event.event_type != keyboard.KEY_DOWN or key in being_held:
        return
    being_held.append(key)
    with sqlite3.connect('keydata.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS keypresses (key varchar, scan_code int, times_pressed int)''')
        c.execute('''SELECT * FROM keypresses WHERE key = ?''', (key,))
        entry = c.fetchone()
        if entry:
            if args.log:
                print((entry[0], entry[1], entry[2] + 1))
            c.execute('''UPDATE keypresses SET times_pressed = ? WHERE key = ?''', (entry[2] + 1, entry[0]))
        else:
            if args.log:
                print((key, event.scan_code, 1))
            c.execute('''INSERT INTO keypresses VALUES (?, ?, ?)''', (key, event.scan_code, 1))
    if record:
        if key in current_recording:
            current_recording[key] += 1
        else:
            current_recording[key] = 1
        

def on_mouse_press(event):
    global record
    if type(event) != mouse.ButtonEvent or event.event_type != mouse.DOWN:
        return
    with sqlite3.connect('keydata.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS mouseclicks (button varchar, times_clicked int)''')
        c.execute('''SELECT * FROM mouseclicks WHERE button = ?''', (event.button,))
        button = c.fetchone()
        if button:
            if args.log:
                print((button[0], button[1] + 1))
            c.execute('''UPDATE mouseclicks SET times_clicked = ? WHERE button = ?''', (button[1] + 1, button[0]))
        else:
            if args.log:
                print((event.button, 1))
            c.execute('''INSERT INTO mouseclicks VALUES (?, ?)''', (event.button, 1))
    if record:
        btn = f'M-{event.button}'
        if btn in current_recording:
            current_recording[btn] += 1
        else:
            current_recording[btn] = 1

keyboard.hook(on_key_press)
mouse.hook(on_mouse_press)

print('Logging has begun')
print('Press ctrl+shift+a to start a seperate recording session that will be saved to a text file')

if args.backup:
    while True:
        time.sleep(args.backup * 60)
        shutil.copy('keydata.db', f'{ensure_dir("backups")}/backup-{time.time()}.db')
        print('Made backup of database.')
else:
    keyboard.wait()

