transcript on
if ![file isdirectory DE10_NANO_D8M_RTL_iputf_libs] {
	file mkdir DE10_NANO_D8M_RTL_iputf_libs
}

if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

###### Libraries for IPUTF cores 
###### End libraries for IPUTF cores 
###### MIF file copy and HDL compilation commands for IPUTF cores 


vlog "/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/VIDEO_PLL_sim/VIDEO_PLL.vo"
vlog "/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/AUDIO_PLL_sim/AUDIO_PLL.vo"

vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/VIDEO_PLL.vo}
vlib VIDEO_PLL
vmap VIDEO_PLL VIDEO_PLL
vlog -vlog01compat -work VIDEO_PLL +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/VIDEO_PLL.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/AUDIO_PLL.vo}
vlib AUDIO_PLL
vmap AUDIO_PLL AUDIO_PLL
vlog -vlog01compat -work AUDIO_PLL +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/AUDIO_PLL.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/FIND_MULTI_POINTS.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/uart_tx_data.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/uart_rx_data.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/uart_rx.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/uart_tx.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/D8M_LUT.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/R_GAIN.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/G_GAIN.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/I2C_READ_DATA.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/I2C_RESET_DELAY.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/I2C_WRITE_PTR.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/I2C_WRITE_WDATA.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI/I2C_HDMI_Config.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI/I2C_Controller.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI/HDMI_TX_AD7513.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI/HDMI_I2C_WRITE_WDATA.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_HDMI/AUDIO_IF.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/int_line.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/RAW2RGB_J.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/RAW_RGB_BIN.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/ON_CHIP_FRAM.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/MIPI_CAMERA_CONFIG.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/MIPI_BRIDGE_CONFIG.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/MIPI_BRIDGE_CAMERA_Config.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/Line_Buffer_J.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/FRM_COUNTER.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/B_GAIN.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_D8M/FRAM_BUFF.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/VCM_I2C.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/VCM_CTRL_P.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/RESET_DELAY.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/MODIFY_SYNC.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/LCD_COUNTER.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/I2C_DELAY.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/FOCUS_ADJ.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/F_VCM.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/CLOCKMEM.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/AUTO_SYNC_MODIFY.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V_Auto/AUTO_FOCUS_ON.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/VGA_Controller {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/VGA_Controller/VGA_Controller.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/kevin/MONO2BINARY.v}
vlog -vlog01compat -work work +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/DE10_NANO_D8M_RTL.v}
vlog -vlog01compat -work VIDEO_PLL +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/VIDEO_PLL {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/VIDEO_PLL/VIDEO_PLL_0002.v}
vlog -vlog01compat -work AUDIO_PLL +incdir+/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/AUDIO_PLL {/home/kevin/src/motion_capture/src/fpga/DE10_NANO_D8M_RTL/V/AUDIO_PLL/AUDIO_PLL_0002.v}

