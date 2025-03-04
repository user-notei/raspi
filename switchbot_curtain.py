# -*- coding: utf-8 -*-

#pip install bluepy argparse


import bluepy.btle as btle
import argparse

class SwitchBotCurtain:
    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.device = btle.Peripheral(mac_address)

    def send_command(self, command):
        service_uuid = "cba20d00-224d-11e6-9fb8-0002a5d5c51b"
        char_uuid = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
        service = self.device.getServiceByUUID(service_uuid)
        char = service.getCharacteristics(char_uuid)[0]
        char.write(command, withResponse=True)

    def open(self):
        self.send_command(b'\x57\x0F\x45\x01\x05\xFF\x00')

    def close(self):
        self.send_command(b'\x57\x0F\x45\x01\x05\xFF\x64')

    def set_position(self, position):
        if 0 <= position <= 100:
            command = bytes([0x57, 0x0F, 0x45, 0x01, 0x05, 0xFF, position])
            self.send_command(command)
        else:
            print("Position must be between 0 and 100.")

def main():
    parser = argparse.ArgumentParser(description="Control SwitchBot Curtain via BLE")
    parser.add_argument("action", choices=["open", "close", "m"], help="Action to perform")
    parser.add_argument("value", nargs="?", type=int, help="Position value (0-100) for 'm' action")
    args = parser.parse_args()

    mac_address = "XX:XX:XX:XX:XX:XX"  # SwitchBotカーテンデバイスのMACアドレスを入力してください
    curtain = SwitchBotCurtain(mac_address)

    if args.action == "open":
        curtain.open()
    elif args.action == "close":
        curtain.close()
    elif args.action == "m":
        if args.value is not None:
            curtain.set_position(args.value)
        else:
            print("Please provide a position value (0-100) for 'm' action.")

if __name__ == "__main__":
    main()
