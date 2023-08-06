
from lib.driver.nvme import NVMe
from lib.driver.pcie import PCIe


class Rout(object):

    def __init__(self, rout_type="rdma"):
        self.rout_type = rout_type
        if rout_type == "rdma":
            print("Rout is rdma")
            self.tool = NVMe()
        else:
            print("Rout is pcie")
            self.tool = PCIe()

    def write(self, offset, value):
        if self.rout_type == "rdma":
            self.tool.rdma_write(offset, value)
        else:
            self.tool.write_bar_uint32(offset, value)

    def read(self, offset):
        if self.rout_type == "rdma":
            value = self.tool.rdma_read(offset)
        else:
            value = self.tool.read_bar_uint32(offset)
        print("Read register: 0x{:x} value 0x{:x}".format(offset, value))
        return value

