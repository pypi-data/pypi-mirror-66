# Automatic file, do not edit!

module_auto = None

import time
def get_mac_address():
    return module_auto.get_value("79b023fb7e007b2291a54784c3ab045f", ())
def get_battery():
    return module_auto.get_value("3988e0aab4777855379065fc8da2ba34", ())
def get_firmware_version():
    return module_auto.get_value("84130d80d8bd240c93e5809565d4fb93", ())
def get_ble():
    return module_auto.get_value("3636689f7387305b262ef85f68736204", ())
def get_name():
    return module_auto.get_value("974853ae311b0874fd141e4dbc7ea504", ())
def set_name(name):
    return module_auto.get_value("3d43914582aed35b01093bddb465dc5a", (name))
def get_brightness():
    return module_auto.get_value("69d00a7b2ddc1d85e7ed380663f01ecf", ())
def get_loudness(tp = "maximum"):  
    return module_auto.get_value("2469bdefeb4529102292af589e8a2efc", (tp ))
def is_tiltlup():
    return module_auto.get_value("c3910abbab3061ed954230add94561aa", ())
def is_tiltldown():
    return module_auto.get_value("26a3b30fbae290421438ed032828f6db", ())
def is_tiltleft():
    return module_auto.get_value("a4cf641a79cf925a87725098646118f9", ())
def is_tiltright():
    return module_auto.get_value("fec52f5ad18094161cec1b417c7e10f5", ())
def is_faceup():
    return module_auto.get_value("43c455ca4f76e8a737618fbef054bdbe", ())
def is_facedown():
    return module_auto.get_value("c6830cf56b1a4f9aaee9ab53e89a923d", ())
def is_stand():
    return module_auto.get_value("c1fb2bd86ac930a853470c2e99c81ea2", ())
def is_handstand():
    return module_auto.get_value("c6d9801ca9be3f1032f2be41538fa658", ())
def is_shake():
    return module_auto.get_value("c33fcd8e57ae1e3b4c513f6f3386b4b6", ())
def is_waveup():
    return module_auto.get_value("e880c1ca448156bf3f371490414e4ee8", ())
def is_wavedown():
    return module_auto.get_value("aefc483bd0bcd4561ee6d6d2abface7c", ())
def is_waveleft():
    return module_auto.get_value("2dd513e5fbaf94cfe7cafdc64ebbeb74", ())
def is_waveright():
    return module_auto.get_value("231b8c48c8b30f532899415153ce868e", ())
def is_clockwise():
    return module_auto.get_value("fe32241d6feac2a268f7eafa488761eb", ())
def is_anticlockwise():
    return module_auto.get_value("196145516d82a638b39657e5b657df7c", ())
def get_shakeval():
    return module_auto.get_value("8a5db13c5c596e0407aa4abbe4f1db48", ())
def get_wave_angle():
    return module_auto.get_value("1632d0eb591aed54c5762a5dcdab81ed", ())
def get_wave_speed():
    return module_auto.get_value("822687ed58d16f303cc79e0b03bb6ce4", ())
def get_roll():
    return module_auto.get_value("1ff145c62ee8412c628e0b0a16fd67fc", ())
def get_pitch():
    return module_auto.get_value("36119451128173ff12497681ec2502e4", ())
def get_yaw():
    return module_auto.get_value("6bc201e4c360195c6ef04a99c3adb982", ())
def get_acc(axis):
    return module_auto.get_value("c9f33e1c6b89d173924779a21a9b1019", (axis))
def get_gyro(axis):
    return module_auto.get_value("55ddb68e0c157494d0f7e9825815ed43", (axis))
def get_rotation(axis):
    return module_auto.get_value("57f3a0363bf3394221b09dd8c8667892", (axis))
def reset_rotation(axis= "all"):
    return module_auto.get_value("2e150de47aabc09be2cd468491e39a37", (axis))

class controller_c():
    def is_press(self, id):
        return module_auto.get_value("0f4008600f10c30d9500bf0896cb3945", ( id))
    def get_count(self, index):
        return module_auto.get_value("f57ae52200b5f46041c7804eec7e0423", ( index))
    def reset_count(self, index):
        module_auto.common_request("87aca6f56a1f74eab8abb4c29616ad3c", ( index))
controller=controller_c()

class audio_c():
    def play(self, file_name):
        module_auto.common_request("99350cd953df88e5f025bcef34113717", ( file_name))
    def play_until(self, file_name):
        module_auto.common_request("0fd6e3524a5e7c70ccb4ae7194c3ebd4", ( file_name))
    def record(self, t):
        module_auto.common_request("8bd7053a4dd190e81637918be72deb46", ( t))
    def play_record(self, speed):
        module_auto.common_request("a8d3656533d5343390a4545985c40c5d", ( speed))
    def play_tone(self, fre, t):
        module_auto.common_request("611cfa431119957e2345e9db178252c6", ( fre, t))
    def play_note(self, note, beat):
        module_auto.common_request("487b1f0a257ab4cad6edd09ea1df35a0", ( note, beat))
    def add_tempo(self, val):
        module_auto.common_request("7cf9bc83ad4148ac607d266d30a4d873", ( val))
    def set_tempo(self, val):
        module_auto.common_request("97f80d0c8e36537051d6c9b21e8a7e56", ( val))
    def get_tempo():
        return module_auto.get_value("0b4dbd2d04bdaac5cf2f578c6087d58d", ())
    def add_vol(self, val):
        module_auto.common_request("f4b0497ab889a85a865a7486dc9c3b20", ( val))
    def set_vol(self, val):
        module_auto.common_request("c2e5e981c561ba61d2d757a61ff17baa", ( val))
    def get_vol(self):
        return module_auto.get_value("4dedceaadf514a624dea51612e1d3f31", ())
    def stop(self):
        module_auto.common_request("510b2145fdd0714503879cc98c435d81", ())
audio=audio_c()

class display_c():
    def set_brush(self, r, g, b):
        module_auto.common_request("3b6fa373ef8ec0614b60949d7a6498eb", ( r, g, b))
    def set_title_color(self, r, g, b):
        module_auto.common_request("f5d5d6501e3afd18d87e81b0ec5eadb4", ( r, g, b))
    def rotate_to(self, angle):
        module_auto.common_request("702530b11223d816f2a79852a5298b7c", ( angle))
    def off(self):
        module_auto.common_request("064b32a98954fee5dba9c08ce8e9ad37", ())
display=display_c()

class console_c():
    def clear(self):
        module_auto.common_request("dbeeb276871d7a91b2466c5fc9c02222", ())
    def print(self, mes):
        module_auto.common_request("5d64cc86824e28e871fb85902181ff18", ( mes))
    def println(self, mes):
        module_auto.common_request("778c0e54274e093926b2012fa3cc6ba4", ( mes))
console=console_c()

class chart_c():
    def set_name(self, name):
        module_auto.common_request("fb465e33a0d73e1ff32e945c30f12836", ( name))
    def clear(self):
        module_auto.common_request("e2c4c0b767853bfb5254e88235ce635b", ())
chart=chart_c()

class linechart_c():
    def add(self, value):
        module_auto.common_request("9c7c0606827e5299122c6b71119a8bab", ( value))
linechart=linechart_c()

class barchart_c():
    def add(self, value):
        module_auto.common_request("953af5bbd66750092d3a1406d53399f3", ( value))
barchart=barchart_c()

class excel_c():
    def add(self, r, c, data):
        module_auto.common_request("619c6b6529423a26de285696190a8c5c", ( r, c, data))
excel=excel_c()

class led_c():
    def on(self, r, g, b, id = "all"):
        module_auto.common_request("5119428dbfeb589dac36fb628ca9248d", ( r, g, b, id ))
    def play(self, name = "rainbow"):
        module_auto.common_request("0c6872183c51d59d859becb64667c349", ( name ))
    def show(self, color, offset = 0):
        module_auto.common_request("c1de77fafa5b4a4e059515b451a5378d", ( color, offset ))
    def move(self, offset = 1):
        module_auto.common_request("3164e897ffb74c0994c83a84f4938989", ( offset ))
    def off(self, id = "all"):
        module_auto.common_request("883bd62fb06060130e7da7ef5eb29eb6", ( id ))
led=led_c()

class wifi_c():
    def connect(self, ssid, password):
        module_auto.common_request("bd1de88cc76a8dbff3a0adea09a34234", ( ssid, password))
    def is_connect(self):
        return module_auto.get_value("f0b19cff8669fd061bf3bf8d755a9eee", ())
wifi=wifi_c()

class cloud_c():
    def setkey(self, key):
        module_auto.common_request("8161e0b45af7e1d12e2bd714b8b3d47f", ( key))
    def weather(self, location):
        module_auto.common_request("434de984f1ad299d904e3deb2cb002e2", ( location))
    def air(self, option, location):
        module_auto.common_request("402dae9adbacff802492236ba6c977c2", ( option, location))
    def time(self, location):
        module_auto.common_request("70279bf87312616ec7e74ab28530fb32", ( location))
    def listen(self, lan, t):
        module_auto.common_request("97adee4bd25bc6c77195451d5e7a42d6", ( lan, t))
    def get_speech(self):
        module_auto.common_request("55fd7c5344384232ee1c40c7581f6b57", ())
    def tts(self, message):
        module_auto.common_request("093cf48163eb9ae0997ea9f6a521c2f2", ( message))
cloud=cloud_c()

class timer_c():
    def get(self):
        return module_auto.get_value("5535075a55d873b7450bad031ba3ba72", ())
    def reset(self):
        module_auto.common_request("e5359d1a429dbef33644fa7d5e450ab2", ())
def broadcast(message):
    module_auto.request("973eab065d5f700522b11bff0540f19a", (message))
def broadcast_and_wait(message):
    module_auto.request("fe662895f3ea37bdb913466a5b6ba520", (message))
timer=timer_c()

class wifi_broadcast_c():
    def set(self, message, value):
        module_auto.common_request("e0b9fb05284e48b4d7a4a97c25eca5de", ( message, value))
    def get(self, message):
        module_auto.common_request("f125d69e4401eb06e48ccd6bb3d6c895", ( message))
wifi_broadcast=wifi_broadcast_c()

class upload_broadcast_c():
    def set(self, message, value):
        module_auto.common_request("71de891af2a5dcbb9a8f4ed958060137", ( message, value))
    def get(self, message):
        module_auto.common_request("4b09d734021e25bcf990c7896f0ed816", ( message))
upload_broadcast=upload_broadcast_c()

class cloud_broadcast_c():
    def set(self, message, value):
        module_auto.common_request("91f7a4c19cdcf0592e368049f5cb04ea", ( message, value))
    def get(self, message):
        module_auto.common_request("d51ad9449c1a722b7df593a3ea603ee0", ( message))
def stop_this():
    module_auto.request("026f484ae8d9f995e168172504962a25", ())
def stop_other():
    module_auto.request("1b05ec802d435cdc23aa16b23bbbc083", ())
def stop_all():
    module_auto.request("b74a8ad1b60ed48e72f89272dbfe394d", ())
def restart():
    module_auto.request("7801409efa2cbc182d240320f247cf63", ())
cloud_broadcast=cloud_broadcast_c()

class event_c():
    def start(self):
        module_auto.common_request("adc31e0c8c68dd42ab1dad5714a694e2", ())
    def is_shake(self):
        module_auto.common_request("858fcd1af422110143a648486c603c09", ())
    def is_press(self, id):
        module_auto.common_request("e139a21c5116ec7210dbba7476adda02", ( id))
    def is_tiltup(self):
        module_auto.common_request("ed60fa45fd0a9e980401c53e708ded47", ())
    def is_tiltdown(self):
        module_auto.common_request("ba90bda5350a58507a3599c6b0bc8e70", ())
    def is_tiltleft(self):
        module_auto.common_request("357740cb5c8e299bb56f973fddc041f0", ())
    def is_tiltright(self):
        module_auto.common_request("bc4c66390735049c9915db0ceb54dfd2", ())
    def is_faceup(self):
        module_auto.common_request("3a522da87cc3efd0a39364f5bab8d86b", ())
    def is_facedown(self):
        module_auto.common_request("c00c1e0ef54e7541ce8d12b330c3018d", ())
    def is_stand(self):
        module_auto.common_request("68f2fb7b73828e5f82f60501b3aca418", ())
    def is_handstand(self):
        module_auto.common_request("7a4a712ee73877568abfffab4c6a4472", ())
    def is_waveup(self):
        module_auto.common_request("1a1d952a390a09afdab69ba96723a857", ())
    def is_wavedown(self):
        module_auto.common_request("3f5f8108a707d50c9c595b1309913a35", ())
    def is_waveleft(self):
        module_auto.common_request("b0ca4b07b50a6b349fa87608422df1de", ())
    def is_waveright(self):
        module_auto.common_request("ceb37edb2c7c03556f529e45c46a6c79", ())
    def is_clockwise(self):
        module_auto.common_request("a522c41acb057a0eb3955717cfe03993", ())
    def is_anticlockwise(self):
        module_auto.common_request("b6cb8d513b6ac15230e2168434464c70", ())
    def receive(self, message):
        module_auto.common_request("089f1a7ab3ce3d81be1bd167099877bc", ( message))
    def upload_broadcast(self, message):
        module_auto.common_request("92778f090ede75693ab02b31cd72f817", ( message))
    def cloud_broadcast(self, message):
        module_auto.common_request("6a8f93e101547247fb551785ed082bfe", ( message))
    def wifi_broadcast(self, message):
        module_auto.common_request("7027f95df86eacceb065ef8a0493625f", ( message))
    def greater_than(self, threshold, type):
        module_auto.common_request("894ec6719c94b519c18ef380a57d9d82", ( threshold, type))
    def samller_than(self, threshold, type):
        module_auto.common_request("0f372307778f6e742402125956b6e7f4", ( threshold, type))
