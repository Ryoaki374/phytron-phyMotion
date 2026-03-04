#!/usr/bin/env python3
"""Minimal single-file control script (no classes).

実施内容:
1) シリアル接続確立
2) P41 (current) を設定
3) 相対 +200 パルス移動

必要ライブラリ:
    pip install pyserial
"""

import serial

# ===== 設定値（必要に応じて編集） =====
DEVICE = '/dev/ttyUSB0'
BAUDRATE = 115200
TIMEOUT = 0.5
ADDRESS = '0'   # 0..9,A..F,@
MODULE = 0
AXIS = 0
CURRENT = 50
# ====================================

STX = '\x02'
ETX = '\x03'
SEP = ':'


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


def main():
    # 1) 通信確立
    with serial.Serial(DEVICE, BAUDRATE, timeout=TIMEOUT) as ser:
        # 2) 電流設定 P41=<CURRENT>  (軸コマンド: M<module>.<axis>P41=<val>)
        resp1 = send_cmd(ser, f"M{MODULE}.{AXIS}P41={CURRENT}")

        # 3) +200 パルス相対移動 (軸コマンド: M<module>.<axis>+200)
        resp2 = send_cmd(ser, f"M{MODULE}.{AXIS}+200")

        print('P41 response:', resp1)
        print('+200 response:', resp2)


if __name__ == '__main__':
    main()
