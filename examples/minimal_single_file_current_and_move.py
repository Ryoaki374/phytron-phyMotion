#!/usr/bin/env python3
"""Minimal single-file control script (no classes).

実施内容:
1) シリアル接続確立(open)
2) P17/P40/P42/P41 を設定
3) 相対パルス移動（カウンターと上限下限チェック付き）
4) 最後にclose

必要ライブラリ:
    pip install pyserial
"""

import serial

# ===== 設定値（必要に応じて編集） =====
DEVICE = '/dev/ttyUSB0'
BAUDRATE = 115200
TIMEOUT = 0.5
ADDRESS = '0'   # 0..9,A..F,@  (後で切り替える前提)
MODULE = 0
AXIS = 0
CURRENT = 50

PULSE_MAX = 10000
PULSE_MIN = -10000
# ====================================

STX = '\x02'
ETX = '\x03'
SEP = ':'

# 符号付きで積算されるパルスカウンター
pulse_counter = 0


def checksum(payload: str) -> str:
    x = 0
    for ch in payload:
        x ^= ord(ch)
    return format(x, '02X')


def build_command(address: str, cmd: str) -> bytes:
    body = f"{address}{cmd}{SEP}"
    chksum = checksum(body)
    return (STX + body + chksum + ETX).encode('latin1')


def read_response(port: serial.Serial) -> str:
    raw = port.read_until(ETX.encode('latin1'))
    if not raw:
        return ''
    return raw.decode('latin1', errors='ignore')


def send_cmd(port: serial.Serial, cmd: str) -> str:
    frame = build_command(ADDRESS, cmd)
    port.write(frame)
    return read_response(port)


def set_drive_parameters(port: serial.Serial):
    # 要望: P17=0, P40=0, P42=0, P41=CURRENT
    print('P17 response:', send_cmd(port, f"M{MODULE}.{AXIS}P17=0"))
    print('P40 response:', send_cmd(port, f"M{MODULE}.{AXIS}P40=0"))
    print('P42 response:', send_cmd(port, f"M{MODULE}.{AXIS}P42=0"))
    print('P41 response:', send_cmd(port, f"M{MODULE}.{AXIS}P41={CURRENT}"))


def move_relative_with_limit(port: serial.Serial, pulse: int):
    global pulse_counter

    next_counter = pulse_counter + pulse
    if next_counter > PULSE_MAX or next_counter < PULSE_MIN:
        print(
            f'ABORT: pulse_counter={pulse_counter}, request={pulse}, '
            f'next={next_counter} is out of range [{PULSE_MIN}, {PULSE_MAX}]'
        )
        return False

    sign = '+' if pulse >= 0 else '-'
    cmd = f"M{MODULE}.{AXIS}{sign}{abs(pulse)}"
    resp = send_cmd(port, cmd)
    pulse_counter = next_counter

    print('Move response:', resp)
    print('pulse_counter:', pulse_counter)
    return True


def main():
    port = serial.Serial(DEVICE, BAUDRATE, timeout=TIMEOUT)
    try:
        # 1) 必要パラメータ設定
        set_drive_parameters(port)

        # 2) +200 パルス移動（上限下限チェック付き）
        move_relative_with_limit(port, 200)
    finally:
        # 3) 最後にclose
        port.close()


if __name__ == '__main__':
    main()
