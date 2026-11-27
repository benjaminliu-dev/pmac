# top = serial::sipo

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from spade import SpadeExt
import cocotb


@cocotb.test()
async def test_sipo(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    s.i.rst_n = "false"
    s.i.en_n = "false"
    input_values = [0, 1, 0, 3, 0, 2] 
    await Timer(1, unit="ns")
    cocotb.start_soon(Clock(clk, period=31.25, unit="ns").start())
    await RisingEdge(clk)
    await FallingEdge(clk)

    for i in range(len(input_values)):
        s.i.sdi = str(input_values[i])
        await RisingEdge(clk)
        await FallingEdge(clk)
        s.i.rst_n = "true"

    s.i.en_n = "true"
    assert int(dut.output__.value) == 0x010302
