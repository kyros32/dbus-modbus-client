import device
from register import *

class Reg_ver(Reg, int):
    def __new__(cls, *args):
        return int.__new__(cls)

    def __init__(self, base, name):
        Reg.__init__(self, base, 1, name)

    def __int__(self):
        v = self.value
        return v[0] << 16 | v[1] << 8 | v[2]

    def __str__(self):
        return '%d.%d.%d' % self.value

    def decode(self, values):
        v = values[0]
        return self.update((v >> 12, v >> 8 & 0xf, v & 0xff))

nr_phase_map = {
    0: 3, # 3P.n
    1: 3, # 3P.1
    2: 2, # 2P
    3: 1, # 1P
    4: 3, # 3P
}

class EM24_Meter(device.ModbusDevice):
    productid = 0xb002
    productname = 'Carlo Gavazzi EM24 Energy Meter'
    default_role = 'grid'
    default_instance = 40

    def __init__(self, *args):
        device.ModbusDevice.__init__(self, *args)

        self.info_regs = [
            Reg_ver(   0x0302,    '/HardwareVersion'),
            Reg_ver(   0x0304,    '/FirmwareVersion'),
            Reg_mapint(0x1002,    '/Phases', nr_phase_map),
            Reg_text(  0x5000, 7, '/Serial'),
        ]

    def phase_regs(self, n):
        s = 2 * (n - 1)
        return [
            Reg_int32(0x0000 + s, '/Ac/L%d/Voltage' % n,        10, '%.1f V'),
            Reg_int32(0x000c + s, '/Ac/L%d/Current' % n,      1000, '%.1f A'),
            Reg_int32(0x0012 + s, '/Ac/L%d/Power' % n,          10, '%.1f W'),
            Reg_int32(0x0040 + s, '/Ac/L%d/Energy/Forward' % n, 10, '%.1f kWh'),
        ]

    def init(self, *args):
        self.read_info()

        phases = int(self.info['/Phases'])

        regs = [
            Reg_int32( 0x0028, '/Ac/Power',          10, '%.1f W'),
            Reg_uint16(0x0033, '/Ac/Frequency',      10, '%.1f Hz'),
            Reg_int32( 0x0034, '/Ac/Energy/Forward', 10, '%.1f kWh'),
            Reg_int32( 0x004e, '/Ac/Energy/Reverse', 10, '%.1f kWh'),
        ]

        for n in range(1, phases + 1):
            regs += self.phase_regs(n)

        regs.sort(key=lambda r: r.base)
        self.data_regs = [regs]

        device.ModbusDevice.init(self, *args)

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']

models = {
    1648: {
        'model':    'EM24DINAV23XE1X',
        'handler':  EM24_Meter,
    },
    1649: {
        'model':    'EM24DINAV23XE1PFA',
        'handler':  EM24_Meter,
    },
    1650: {
        'model':    'EM24DINAV23XE1PFB',
        'handler':  EM24_Meter,
    },
    1651: {
        'model':    'EM24DINAV53XE1X',
        'handler':  EM24_Meter,
    },
    1652: {
        'model':    'EM24DINAV53XE1PFA',
        'handler':  EM24_Meter,
    },
    1653: {
        'model':    'EM24DINAV53XE1PFB',
        'handler':  EM24_Meter,
    },
}

device.add_handler(device.ModelRegister(0x000b, models))
