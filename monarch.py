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
            Reg_text(30001, 8, '/Serial'),
            Reg_text(30005, 8, '/HardwareVersion'),
            Reg_text(30009, 8, '/FirmwareVersion'),
            Reg_text(30013, 8, '/CustomName'),

        ]

        self.data_regs = [
          
            Reg_f32b(30015, '/Info/MaxChargeCurrent',      1, '%.0f A'),
            Reg_f32b(30017, '/Info/MaxDischargeCurrent ',   1, '%.0f A'),
            Reg_f32b(30019, '/Info/MaxChargeVoltage',   1, '%.0f V'),
            Reg_f32b(30021, '/Info/BatteryLowVoltage',   1, '%.0f V'),
            Reg_text(30023, 8, '/Info/ChargeRequest'),
        ]



models = {
    'Monarch_v1': { # Monarch_v1
        'model': 'v_1.01',
        'handler': Monarch_BMS,
    }
}

probe.add_handler(probe.ModelRegister(Reg_text(30011, 8), models,
                                      methods=['tcp'],
                                      units=[3]))
