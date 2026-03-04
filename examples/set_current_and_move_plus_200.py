#!/usr/bin/env python3
"""Minimal example: set P41 current, then move +200.

このスクリプトは argparse を使わず、固定値で実行します。
必要なら DEVICE / MODULE / AXIS / CURRENT を直接書き換えてください。
"""

from phytron_phymotion.factory import PhytronFactory
from phytron_phymotion.messages.parameter import PARAMETER_CURRENT

# ====== ここを必要に応じて変更 ======
DEVICE = '/dev/ttyUSB0'
MODULE = 0
AXIS = 0
CURRENT = 50  # P41 に設定する値
# ================================


def main():
    driver = PhytronFactory().create_driver(device=DEVICE)
    driver.set_axis(MODULE, AXIS)

    # P41(電流値) を設定
    driver.set_parameter(PARAMETER_CURRENT, CURRENT)

    # +200 ステップ相対移動
    driver.move_relative(200)

    print('Done: sent P41={} and move +200 on M{}.{} via {}.'.format(CURRENT, MODULE, AXIS, DEVICE))


if __name__ == '__main__':
    main()
