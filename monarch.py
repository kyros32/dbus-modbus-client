import struct
import device
import probe
from register import *


class Monarch_BMS(device.Battery):
    vendor_id = 'solarbaron'
    vendor_name = 'SOLAR BARON'
    productid = 0xB0414
    productname = 'MONARCH BMS'
    min_timeout = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._custom_name = 'monarch'

    def device_init(self):
        # Register information about the device
        self.info_regs = [
            Reg_text(30001, 8, '/Serial'),
            Reg_text(30005, 8, '/HardwareVersion'),
            Reg_text(30009, 1, '/FirmwareVersion'),
        ]

        # Register data points for the battery
        self.data_regs = [
            Reg_f32b(30021, '/Info/MaxChargeCurrent', 1, '%.0f A'),
            Reg_f32b(30023, '/Info/MaxDischargeCurrent', 1, '%.0f A'),
            Reg_f32b(30025, '/Info/MaxChargeVoltage', 1, '%.0f V'),
            Reg_f32b(30027, '/Info/BatteryLowVoltage', 1, '%.0f V'),
            Reg_bit(30029, '/Info/ChargeRequest', bit=0),
        ]


# Define the models
models = {
    'Monarch_v1': {  # Monarch_v1
        'model': 'AA',
        'handler': Monarch_BMS,
    }
}

# Add the Monarch BMS to the probe system
probe.add_handler(probe.ModelRegister(
    Reg_text(30013, 8),  # Adjusted register and size for model identification
    models,
    methods=['tcp'],  # Communication method
    units=[154],  # Modbus unit ID
    port=503  # Port number
))
