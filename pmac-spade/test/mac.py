# top = mac::mac

from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from spade import SpadeExt
import cocotb


@cocotb.test()
async def test_mac_accumulation(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    s.i.rst_n = "false"
    s.i.en_n = "false"
    s.i.bias = "0"
    s.i.di_a = "0"
    s.i.di_b = "0"
    await Timer(1, units="ns")
    cocotb.start_soon(Clock(clk, period=31.25, units="ns").start())
    await RisingEdge(clk)
    await FallingEdge(clk)
    assert int(dut.output__.value) == 0
