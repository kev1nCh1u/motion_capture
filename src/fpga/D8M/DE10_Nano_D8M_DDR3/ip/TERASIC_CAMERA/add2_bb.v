// megafunction wizard: %PARALLEL_ADD%VBB%
// GENERATION: STANDARD
// VERSION: WM1.0
// MODULE: parallel_add 

// ============================================================
// File Name: add2.v
// Megafunction Name(s):
// 			parallel_add
//
// Simulation Library Files(s):
// 			
// ============================================================
// ************************************************************
// THIS IS A WIZARD-GENERATED FILE. DO NOT EDIT THIS FILE!
//
// 16.0.2 Build 222 07/20/2016 SJ Standard Edition
// ************************************************************

//Copyright (C) 1991-2016 Altera Corporation. All rights reserved.
//Your use of Altera Corporation's design tools, logic functions 
//and other software and tools, and its AMPP partner logic 
//functions, and any output files from any of the foregoing 
//(including device programming or simulation files), and any 
//associated documentation or information are expressly subject 
//to the terms and conditions of the Altera Program License 
//Subscription Agreement, the Altera Quartus Prime License Agreement,
//the Altera MegaCore Function License Agreement, or other 
//applicable license agreement, including, without limitation, 
//that your use is for the sole purpose of programming logic 
//devices manufactured by Altera and sold by Altera or its 
//authorized distributors.  Please refer to the applicable 
//agreement for further details.

module add2 (
	data0x,
	data1x,
	result);

	input	[11:0]  data0x;
	input	[11:0]  data1x;
	output	[12:0]  result;

endmodule

// ============================================================
// CNX file retrieval info
// ============================================================
// Retrieval info: PRIVATE: INTENDED_DEVICE_FAMILY STRING "Stratix V"
// Retrieval info: PRIVATE: SYNTH_WRAPPER_GEN_POSTFIX STRING "0"
// Retrieval info: LIBRARY: altera_mf altera_mf.altera_mf_components.all
// Retrieval info: CONSTANT: MSW_SUBTRACT STRING "NO"
// Retrieval info: CONSTANT: PIPELINE NUMERIC "0"
// Retrieval info: CONSTANT: REPRESENTATION STRING "UNSIGNED"
// Retrieval info: CONSTANT: RESULT_ALIGNMENT STRING "LSB"
// Retrieval info: CONSTANT: SHIFT NUMERIC "0"
// Retrieval info: CONSTANT: SIZE NUMERIC "2"
// Retrieval info: CONSTANT: WIDTH NUMERIC "12"
// Retrieval info: CONSTANT: WIDTHR NUMERIC "13"
// Retrieval info: USED_PORT: data0x 0 0 12 0 INPUT NODEFVAL "data0x[11..0]"
// Retrieval info: USED_PORT: data1x 0 0 12 0 INPUT NODEFVAL "data1x[11..0]"
// Retrieval info: USED_PORT: result 0 0 13 0 OUTPUT NODEFVAL "result[12..0]"
// Retrieval info: CONNECT: @data 0 0 12 0 data0x 0 0 12 0
// Retrieval info: CONNECT: @data 0 0 12 12 data1x 0 0 12 0
// Retrieval info: CONNECT: result 0 0 13 0 @result 0 0 13 0
// Retrieval info: GEN_FILE: TYPE_NORMAL add2.v TRUE
// Retrieval info: GEN_FILE: TYPE_NORMAL add2.inc FALSE
// Retrieval info: GEN_FILE: TYPE_NORMAL add2.cmp FALSE
// Retrieval info: GEN_FILE: TYPE_NORMAL add2.bsf FALSE
// Retrieval info: GEN_FILE: TYPE_NORMAL add2_inst.v FALSE
// Retrieval info: GEN_FILE: TYPE_NORMAL add2_bb.v TRUE
