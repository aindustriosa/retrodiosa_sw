#! /home/nicoyiago/retrodiosa-sw/venv/bin/python

import os, sys, struct, time, fcntl, termios, signal,json
import curses, errno, re
import pyautogui
import psutil
import logging
from pyudev import Context


#    struct js_event {
#        __u32 time;     /* event timestamp in milliseconds */
#        __s16 value;    /* value */
#        __u8 type;      /* event type */
#        __u8 number;    /* axis/button number */
#    };

# os.kill(int(pid), signal.SIGTERM)  
# [p.info for p in psutil.process_iter(attrs=['pid', 'cmdline']) if '/home/nicoyiago/mightyLD37/desktop/build/libs/desktop-1.0.jar' in p.info['cmdline']]

# constant vars

JS_MIN = -32768
JS_MAX = 32768
JS_REP = 0.0

JS_THRESH = 0.75

JS_EVENT_BUTTON = 0x01
JS_EVENT_AXIS = 0x02
JS_EVENT_INIT = 0x80

CONFIG_DIR = '/opt/retropie/configs/'
RETROARCH_CFG = CONFIG_DIR + 'all/retroarch.cfg'


def ini_get(key, cfg_file):
    """ Search button values using regular expressions """
    
    pattern = r'[ |\t]*' + key + r'[ |\t]*=[ |\t]*'
    value_m = r'"*([^"\|\r]*)"*'
    value = ''
    with open(cfg_file, 'r') as ini_file:
        for line in ini_file:
            if re.match(pattern, line):
                value = re.sub(
                    pattern + value_m + '.*\n', r'\1', line)
                break
    return value

def get_btn_num(btn, cfg):
    """ Get the number of a button """
    num = ini_get(btn, cfg)
    if num: return num
    return ''

def sysdev_get(key, sysdev_path):
    value = ''
    for line in open(sysdev_path + key, 'r'):
        value = line.rstrip('\n')
        break
    return value

def get_button_codes(dev_path, button_key_codes, finish_js_codes):
    """ Obtain the button codes of a device """

    js_cfg_dir = CONFIG_DIR + 'all/retroarch-joypads/'
    js_cfg = ''
    dev_name = ''
    dev_button_codes = None
    axis_button_codes = None
    finish_button_codes = None

    logging.info("Device: {}".format(
        Context().list_devices(DEVNAME=dev_path)))

    # searching joystick real path
    for device in Context().list_devices(DEVNAME=dev_path):
        sysdev_path = (os.path.normpath(
            '/sys' + device.get('DEVPATH')) + '/')
        if not os.path.isfile(sysdev_path + 'name'):
            sysdev_path = (os.path.normpath(
                sysdev_path + '/../') + '/')
        # getting joystick name
        dev_name = sysdev_get('name', sysdev_path)
        # getting joystick vendor ID
        dev_vendor_id = int(sysdev_get(
            'id/vendor', sysdev_path), 16)
        # getting joystick product ID
        dev_product_id = int(
            sysdev_get('id/product', sysdev_path), 16)

    if not dev_name:
        logging.info("No buttons for {}".format(devpath))
        return (dev_button_codes, axis_button_codes,
                finish_button_codes)
    
    logging.info("Config dir {}".format(js_cfg_dir))

    # getting retroarch config file for joystick
    for f in os.listdir(js_cfg_dir):
        if f.endswith('.cfg'):
            input_device = ini_get('input_device', js_cfg_dir + f)
            input_vendor_id = ini_get('input_vendor_id', js_cfg_dir + f)
            input_product_id = ini_get('input_product_id', js_cfg_dir + f)
            if (input_device == dev_name and
                (input_vendor_id  == '' or int(input_vendor_id)  == dev_vendor_id) and
                (input_product_id == '' or int(input_product_id) == dev_product_id)):
                js_cfg = js_cfg_dir + f
                break
            
    if not js_cfg:
        # pick retroarch conf file only if the device config file does not exist
        js_cfg = RETROARCH_CFG

    # getting configs
    btn_map = [key for key in button_key_codes]
    btn_num = {}
    finish_num = []

    for btn in list(btn_map):
        btn_num[btn] = get_btn_num(btn, js_cfg)

        try:
            num = int(btn_num[btn])
            if btn_num[btn].startswith("-") and num==0:
                btn_num[btn] = int(btn_num[btn]) - 100
            else:
                btn_num[btn] = int(btn_num[btn])
        except ValueError:
            btn_map.pop(i) # FIXME: check this!
            btn_num.pop(btn, None)
            continue

    # picking finish js codes
    for btn in list(finish_js_codes):
        try:
            finish_num.append(int(get_btn_num(btn, js_cfg)))
        except ValueError:
            #finish_num.pop(-1)
            continue
        
    # building the button codes dict num -> key
    btn_codes = {}
    axis_codes = {}
    i = 0
    for btn in btn_map:
        if "axis" in btn:
            axis_codes[btn_num[btn]] = button_key_codes[btn]
        else:
            btn_codes[btn_num[btn]] = button_key_codes[btn]
        i += 1

    logging.info("Button codes {}".format(btn_codes))
    logging.info("Axis codes {}".format(axis_codes))
    logging.info("Finish key number {}".format(finish_num))

    return btn_codes, axis_codes, finish_num
        
def signal_handler(signum, frame):
    close_fds(js_fds)

    logging.info("Closing Device")
    sys.exit(0)

    
def get_hex_chars(key_str):
    if (key_str.startswith("0x")):
        return key_str[2:].decode('hex')
    else:
        return curses.tigetstr(key_str)

def get_devices():
    devs = []
    if sys.argv[1] == '/dev/input/jsX':
        for dev in os.listdir('/dev/input'):
            if dev.startswith('js'):
                devs.append('/dev/input/' + dev)
    else:
        devs.append(sys.argv[1])
                
    return devs
    
def open_devices(player_js_map,
                 button_key_codes,
                 button_num_codes,
                 axis_num_codes,
                 finish_js_codes,
                 finish_num_codes):

    devs = get_devices()
    
    fds = []
    for player_map, dev in zip(
            player_js_map, devs):

        try:
            fds.append(os.open(dev, os.O_RDONLY | os.O_NONBLOCK ))
            (button_num_codes[fds[-1]],
             axis_num_codes[fds[-1]],
             finish_num_codes[fds[-1]]) = get_button_codes(
                 dev,
                 button_key_codes[player_js_map[player_map]],
                 finish_js_codes)
                        
        except (OSError, ValueError):
            pass
        
    return devs, fds

def close_fds(fds):
    for fd in fds:
        os.close(fd)

def read_event(fd):
    while True:
        try:
            event = os.read(fd, event_size)
        except OSError as e:
            if e.errno == errno.EWOULDBLOCK:
                return None
            return False

        else:
            return event

def process_event(event, button_codes, axis_codes,
                  finish_codes, keystroke_finish):

    (js_time, js_value, js_type, js_number) = struct.unpack(event_format, event)

    #logging.info("JS_TYPE {}".format(js_type))
    
    # ignore init events
    if js_type & JS_EVENT_INIT:
        return False

    hex_chars = ""
    axis_chars = ""
    
    if js_type == JS_EVENT_BUTTON:
        if js_number in button_codes and js_value == 1:
            hex_chars = button_codes[js_number]
            pyautogui.keyDown(hex_chars)
            logging.info("KEYDOWN {} - {} ".format(hex_chars, js_number))

        elif js_number in button_codes and js_value == 0:
            hex_chars = button_codes[js_number]
            pyautogui.keyUp(hex_chars)
            logging.info("KEYUP {}".format(hex_chars))
        else:
            logging.info("JSVALUE (unrecognized option) {}".format(js_value))

        if js_number in finish_codes and js_value == 1:
            keystroke_finish.append(js_number)
            logging.info("KEYSTROKE {}".format(keystroke_finish))

        elif js_number in finish_codes and js_value == 0:
            keystroke_finish.remove(js_number)
            logging.info("KEYSTROKE {}".format(keystroke_finish))

    if js_type == JS_EVENT_AXIS:

        logging.info("AXIS JS_VALUE {}".format(js_value))
        
        if js_value <= JS_MIN * JS_THRESH:
            
            if js_number == 0:
                axis_chars = axis_codes[-100]
            else:
                axis_chars = axis_codes[-js_number]

            pyautogui.keyDown(axis_chars)

        elif js_value >= JS_MAX * JS_THRESH:
            axis_chars = axis_codes[js_number]

            pyautogui.keyDown(axis_chars)

        else:
            # Event: axis is not active
            logging.info("JS_NUMBER {}".format(js_number))

            # +0 and -0 (-0 is also 0 in int => changing to -100)
            if js_number == 0:
                axis_chars = axis_codes[-100]
            else:
                axis_chars = axis_codes[-js_number]
                
            pyautogui.keyUp(axis_chars)
            axis_chars = axis_codes[js_number]
            pyautogui.keyUp(axis_chars)
        
    if hex_chars or axis_chars or len(keystroke_finish) > 0:
        # there is a new accepted event
        return True

    return False


def get_js_device_configuration(data, player, js_button_codes):
    js_button_codes[player] = {}
    for key in data[player]:
        js_button_codes[player][key] = data[player][key]
        
    return js_button_codes


def get_js_configuration(data):
    """ Obtain button codes for all the devices """
    js_button_codes = {}
    
    # read player 1 keys
    if "player1_keys" in data:
        js_button_codes = get_js_device_configuration(
            data, "player1_keys", js_button_codes)
    if "player2_keys" in data:
        js_button_codes = get_js_device_configuration(
            data, "player2_keys", js_button_codes)

    return js_button_codes

def send_kill_signal(process_name):

    #process_name = os.path.basename(process_name)
    print ("ALL", [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline'])])

    
    pid_list = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline']) if process_name in p.info['cmdline'] or "./" + os.path.basename(process_name) in p.info['cmdline']]

    print ("PIDLIST", pid_list, "PROCESS", process_name)
    
    logging.info("Sending kill signal to {}".format(process_name))
    
    for pid_dict in pid_list:
        if pid_dict['name'] == "java" or pid_dict['name'] == "fuse" or pid_dict['name'] == os.path.basename(process_name):
            pid = pid_dict['pid']
            os.kill(int(pid), signal.SIGTERM)

if __name__ == "__main__":

    print("HELLO")
    
    # set up logging to file
    logging.basicConfig(level=logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # simpler format for console
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

    # use this logging format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger('basic')

    # Disabling FAILSAFE of autogui
    pyautogui.FAILSAFE = False
    
    signal.signal(signal.SIGINT, signal_handler)

    # the first parameter is the json config file
    json_config_file = sys.argv[2]

    # picking rom
    process_name = sys.argv[3]

    logging.info("Playing {}".format(process_name))

    with open(json_config_file, "r") as f_in:
        data = json.load(f_in)

    # get button codes
    button_key_codes = get_js_configuration(data)
    button_num_codes = {}
    axis_num_codes = {}
    finish_js_codes = []
    keystroke_finish = {} # store finish strokes
    if "hotkey_finish" in data:
        finish_js_codes = data["hotkey_finish"]
        
    finish_num_codes = {}
    player_js_map = {0: "player1_keys",
                     1: "player2_keys",
                     2: "player1_keys",
                     3: "player2_keys",
                     4: "player1_keys",
                     5: "player2_keys"}    
    #curses.setupterm()

    event_format = 'IhBB'

    event_size = struct.calcsize(event_format)
    
    # open input devices
    js_fds = []
    rescan_time = time.time()

    # infinite loop
    while True:
        do_sleep = True
        if not js_fds:
            js_devs, js_fds = open_devices(
                player_js_map,
                button_key_codes,
                button_num_codes,
                axis_num_codes,
                finish_js_codes,
                finish_num_codes)

            if js_fds:
                i = 0
                current = time.time()
                js_last = [None] * len(js_fds)

                for js  in js_fds:
                    js_last[i] = current
                    i += 1
                else:
                    time.sleep(1)

        else:
            i = 0
            for fd in js_fds:
                event = read_event(fd)
                if event:
                    do_sleep = False
                    if time.time() - js_last[i] > JS_REP:
                        if fd in button_num_codes:
                            button_codes = button_num_codes[fd]
                            
                            axis_codes = axis_num_codes[fd]
                            finish_codes = finish_num_codes[fd]

                            if fd not in keystroke_finish:
                                keystroke_finish[fd] = []
                        else:
                            if fd not in keystroke_finish:
                                keystroke_finish[fd] = []
                            
                            button_codes = None
                            axis_codes = None
                            finish_codes = None
                        if process_event(event,
                                         button_codes,
                                         axis_codes,
                                         finish_codes,
                                         keystroke_finish[fd]):
                            js_last[i] = time.time()

                            # check for finish code
                            if len(keystroke_finish[fd]) > 0:
                                if len(finish_codes) == len(keystroke_finish[fd]):
                                    send_kill_signal(process_name)
                            
                elif event == False:
                    close_fds(js_fds)
                    js_fds = []
                    break
                i += 1

        if time.time() - rescan_time > 2:
            rescan_time = time.time()
            if js_devs != get_devices():
                close_fds(js_fds)
                js_fds = []

        if do_sleep:
            time.sleep(0.01)

            
