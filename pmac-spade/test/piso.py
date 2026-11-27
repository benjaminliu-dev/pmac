# top = piso::piso

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from spade import SpadeExt
import cocotb

@cocotb.test()
async def test_piso(dut):
    received = []
    s = SpadeExt(dut)
    clk = dut.clk_i
    s.i.rst_n = "false"
    s.i.en_n = "true"
    s.i.load_n = "true"
    s.i.di = "0x123456"

    await Timer(1, unit="ns")

    cocotb.start_soon(Clock(clk, period=31.25, unit="ns").start())

    await RisingEdge(clk)
    await FallingEdge(clk)

    assert int(dut.output__.value) == 0
    s.i.rst_n = "true"

    s.i.load_n = "false"

    await RisingEdge(clk)
    await FallingEdge(clk)

    s.i.load_n = "true"

    s.i.en_n = "false"

    assert int(dut.output__.value) == 2

    received.append(int(dut.output__.value))

    for i in range(11):
        await RisingEdge(clk)
        await FallingEdge(clk)
        assert int(dut.output__.value) == ((0x123456 >> 2 * (i + 1)) & 0b11)
        received.append(int(dut.output__.value))

    dut._log.info(f"received: {received}")


    

