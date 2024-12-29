import struct
import device
import probe
from register import *


class Monarch_BMS(device.CustomName, device.battery):
    vendor_id = 'solarbaron'
    vendor_name = 'SOLAR BARON'
    productid = 0xB0414
    productname = 'MONARCH BMS'
    min_timeout = 0.5

    def device_init(self):
        self.info_regs = [
            Reg_text(1323, 8, '/FirmwareVersion'),
            Reg_text(3000, 8, '/CustomName'),
            Reg_serial(0x8900, '/Serial'),
            Reg_text(0x2002, 32, '/CustomName', encoding='utf-8'),
        ]

        self.data_regs = [
          
            Reg_s16(1020, '/Info/MaxChargeCurrent',      1, '%.0f A'),
            Reg_s16(1021, '/Info/MaxDischargeCurrent ',   1, '%.0f A'),
            Reg_s16(1022, '/Info/MaxChargeVoltage',   0.001, '%.0f V'),
            Reg_s16(1023, '/Info/BatteryLowVoltage',   10, '%.0f V'),
            Reg_text(3000, 8, '/Info/ChargeRequest'),
        ]



models = {
    'Monarch_v1': { # Monarch_v1
        'model': 'Monarch_v1',
        'handler': Monarch_BMS,
    }
}

probe.add_handler(probe.ModelRegister(Reg_u16(0x1000), models,
                                      methods=['tcp'],
                                      units=[3]))
