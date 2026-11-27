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
    await Timer(1, unit="ns")
    cocotb.start_soon(Clock(clk, period=31.25, unit="ns").start())
    await RisingEdge(clk)
    await FallingEdge(clk)
    assert int(dut.output__.value) == 0

@cocotb.test()
async def test_mac_accumulate_and_hold(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    s.i.rst_n = "false"
    s.i.en_n = "true"
    s.i.bias = "0"
    s.i.di_a = "0"
    s.i.di_b = "0"
    await Timer(1, unit="ns")
    cocotb.start_soon(Clock(clk, period=31.25, unit="ns").start())
    await RisingEdge(clk)
    await FallingEdge(clk)
    s.i.rst_n = "true"
    s.i.di_a = "1"
    s.i.di_b = "3"
    s.i.bias = "2"
    s.i.en_n = "false"

    test_list = [5, 10, 15]

    for i in range(len(test_list)):
        await RisingEdge(clk)
        await FallingEdge(clk)
        assert int(dut.output__.value) == test_list[i]

    s.i.en_n = "true"

    assert int(dut.output__.value) == 15

@cocotb.test()
async def test_mac_overflow(dut):
    s = SpadeExt(dut)
    clk = dut.clk_i
    s.i.rst_n = "false"
    s.i.en_n = "true"
    s.i.bias = "0"
    s.i.di_a = "0"
    s.i.di_b = "0"
    await Timer(1, unit="ns")
    cocotb.start_soon(Clock(clk, period=31.25, unit="ns").start()) 
    await RisingEdge(clk)
    await FallingEdge(clk)  
    s.i.rst_n = "true"
    s.i.en_n = "false"
    s.i.di_a = "-128"
    s.i.di_b = "-128"
    s.i.bias = "127"

    expected_value = 0
    for i in range(508):
        expected_value += 16511
        await RisingEdge(clk)
        await FallingEdge(clk)
        assert int(dut.output__.value) == expected_value

    s.i.di_a = "8"
    s.i.di_b = "127"
    s.i.bias = "3"

    expected_value += 1019

    await RisingEdge(clk)
    await FallingEdge(clk)
    assert int(dut.output__.value) == 8388607

    s.i.di_a = "1"
    s.i.di_b = "1"
    s.i.bias = "0"

    await RisingEdge(clk)
    await FallingEdge(clk)

    assert int(dut.output__.value.to_signed()) == -8388608



    


