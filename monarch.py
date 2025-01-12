import struct
import device
import probe
from register import *
from device import BaseDevice
from vedbus import VeDbusService, ServiceContext
from utils import private_bus
import logging

log = logging.getLogger('Monarch_BMS')

class Monarch_BMS(BaseDevice):
    vendor_id = 'solarbaron'
    vendor_name = 'SOLAR BARON'
    productid = 0xB0414
    productname = 'MONARCH BMS'
    device_type = 'battery'
    min_timeout = 0.5
    custom_name = 'monarch'

    def device_init(self):
        log.info("Initializing Monarch BMS device")
        # Register information about the device
        self.info_regs = [
            Reg_text(0, 8, '/Serial', access='input'),
            Reg_text(4, 8, '/HardwareVersion', access='input'),
            Reg_text(8, 1, '/FirmwareVersion', access='input'),
        ]

	# Register data points for the battery
        self.data_regs = [
            Reg_f32b(20, '/Info/MaxChargeCurrent', 1, '%.0f A', access='input'),
            Reg_f32b(22, '/Info/MaxDischargeCurrent', 1, '%.0f A', access='input'),
            Reg_f32b(24, '/Info/MaxChargeVoltage', 1, '%.0f V', access='input'),
            Reg_f32b(26, '/Info/BatteryLowVoltage', 1, '%.0f V', access='input'),
            Reg_bit(28, '/Info/ChargeRequest', bit=0, access='input'),
        ]

    def init_dbus(self):
        log.info("Initializing D-Bus for Monarch BMS")
        super().init_dbus()
        svcname = f'com.victronenergy.battery.{self.custom_name}'
        self._dbus = VeDbusService(svcname, private_bus())
        self.dbus = ServiceContext(self._dbus)

        # Add management paths
        self.dbus.add_path('/Mgmt/ProcessName', 'Monarch_BMS')
        self.dbus.add_path('/Mgmt/ProcessVersion', '1.0')
        self.dbus.add_path('/Mgmt/Connection', self.connection())

        # Add device paths
        self.dbus.add_path('/DeviceInstance', 0)
        self.dbus.add_path('/ProductId', self.productid)
        self.dbus.add_path('/ProductName', self.productname)
        self.dbus.add_path('/Model', 'AA')
        self.dbus.add_path('/Connected', 1)

        # Add info paths dynamically from data_regs
        for reg in self.data_regs:
            self.dbus.add_path(reg.name, None)

        log.info("D-Bus initialization complete")

# Define the models
models = {
    16705: {  # Monarch_v1
            'model': 'AA',
        'handler': Monarch_BMS,
    }
}

# Add the Monarch BMS to the probe system
probe.add_handler(probe.ModelRegister(
    Reg_u16(12, 1, access='input'),  # Adjusted register and size for model identification
    models,
    methods=['tcp'],  # Communication method
    units=[154],  # Modbus unit ID
))
