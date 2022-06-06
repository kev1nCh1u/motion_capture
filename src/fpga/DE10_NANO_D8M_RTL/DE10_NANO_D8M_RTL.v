
//=======================================================
//  This code is generated by Terasic System Builder
//=======================================================

module  DE10_NANO_D8M_RTL(

	//////////// CLOCK //////////
	input 		          		FPGA_CLK1_50,
	input 		          		FPGA_CLK2_50,
	input 		          		FPGA_CLK3_50,

	//////////// HDMI //////////
	inout 		          		HDMI_I2C_SCL,
	inout 		          		HDMI_I2C_SDA,
	inout 		          		HDMI_I2S,
	inout 		          		HDMI_LRCLK,
	inout 		          		HDMI_MCLK,
	inout 		          		HDMI_SCLK,
	output		          		HDMI_TX_CLK,
	output		          		HDMI_TX_DE,
	output		    [23:0]		HDMI_TX_D,
	output		          		HDMI_TX_HS,
	input 		          		HDMI_TX_INT,
	output		          		HDMI_TX_VS,

	//////////// KEY //////////
	input 		     [1:0]		KEY,

	//////////// LED //////////
	output		     [7:0]		LED,

	//////////// SW //////////
	input 		     [3:0]		SW,

	//////////// GPIO_0, GPIO connect to D8M-GPIO //////////
	inout 		          		CAMERA_I2C_SCL,
	inout 		          		CAMERA_I2C_SDA,
	output		          		CAMERA_PWDN_n,
	output		          		MIPI_CS_n,
	inout 		          		MIPI_I2C_SCL,
	inout 		          		MIPI_I2C_SDA,
	output		          		MIPI_MCLK,
	input 		          		MIPI_PIXEL_CLK,
	input 		     [9:0]		MIPI_PIXEL_D,
	input 		          		MIPI_PIXEL_HS,
	input 		          		MIPI_PIXEL_VS,
	output		          		MIPI_REFCLK,
	output		          		MIPI_RESET_n,

	//////////// kevin TEST_IO //////////
	output		     [7:0]		TEST_IO,
	output		     [15:0]		TEST_IO_2,

	//////////// kevin uart //////////
	input UART_RX,
	output UART_TX
);

//=======================================================
//  REG/WIRE declarations
//=======================================================
// 50,000,000 / 115,200 = 434...
localparam BAUD_RATE = 435;

wire        READ_Request ;
wire 	[7:0] BLUE;
wire 	[7:0] GREEN;
wire 	[7:0] RED;

wire 	[7:0] VGA_R;
wire 	[7:0] VGA_G;
wire 	[7:0] VGA_B;
wire        VGA_VS;
wire        VGA_HS;
wire        VGA_CLK  ;
wire        RESET_N  ; 
wire        RESET_N_DELAY  ; 

wire        I2C_RELEASE ;  
wire        CAMERA_I2C_SCL_MIPI ; 
wire        CAMERA_I2C_SCL_AF;
wire        CAMERA_MIPI_RELAESE ;
wire        MIPI_BRIDGE_RELEASE ;  
wire        VCM_RELAESE ; 
wire        AUTO_FOC ;
wire        D8M_CK_HZ  ;
wire        TX_DE ;

wire 	[7:0] R_AUTO;
wire 	[7:0] G_AUTO;
wire 	[7:0] B_AUTO;


wire [9:0]  RD_DATA ; 
wire [19:0] WR_ADDR ;
wire [19:0] RD_ADDR ;  

wire        HDMI_READY  ; 
wire        HDMI_I2S_;

wire        LUT_MIPI_PIXEL_HS;
wire        LUT_MIPI_PIXEL_VS;
wire [9:0]  LUT_MIPI_PIXEL_D  ;

//////////////// kevin find point /////////////////
// wire 	[7:0]  VGA_GRAY;
wire 	BINARY_FLAG;
wire 	[23:0] VGA_BINARY;
wire 	[15:0] H_CNT;
wire 	[15:0] V_CNT;

wire 	[15:0] POINTS_H_0; // point_x_0
wire 	[15:0] POINTS_V_0; // point_y_0
wire 	[15:0] POINTS_H_1; // point_x_1
wire 	[15:0] POINTS_V_1; // point_y_1
wire 	[15:0] POINTS_H_2; // point_x_2
wire 	[15:0] POINTS_V_2; // point_y_2
wire 	[15:0] POINTS_H_3; // point_x_3
wire 	[15:0] POINTS_V_3; // point_y_3

wire 	[15:0] POINTS_H_4; // point_x_4
wire 	[15:0] POINTS_V_4; // point_y_4
wire 	[15:0] POINTS_H_5; // point_x_5
wire 	[15:0] POINTS_V_5; // point_y_5
wire 	[15:0] POINTS_H_6; // point_x_6
wire 	[15:0] POINTS_V_6; // point_y_6
wire 	[15:0] POINTS_H_7; // point_x_7
wire 	[15:0] POINTS_V_7; // point_y_7

////////////////// kevin tx ////////////////////////
wire [7:0] TX_BYTE;
reg r_TX_DV;
wire TX_ACTIVE;
wire TX_DONE;
wire [2:0] TX_STATE;

/////////////////// kevin rx ///////////////////
wire [7:0] RX_BYTE;
wire r_RX_DV;
wire COLOR_FLAG;
wire [7:0] BINARY_THRESHOLD;
wire [2:0] RX_STATE;

//=======================================================
// Structural coding
//=======================================================

//--D8M INPUT Gamma Correction 
 D8M_LUT  g_lut(
	.enable           (0),//SW[0]            ),
	.PIXEL_CLK        (MIPI_PIXEL_CLK   ),
	.MIPI_PIXEL_HS    (MIPI_PIXEL_HS    ),
	.MIPI_PIXEL_VS    (MIPI_PIXEL_VS    ),
	.MIPI_PIXEL_D     (MIPI_PIXEL_D     ),
	.NEW_MIPI_PIXEL_HS(LUT_MIPI_PIXEL_HS),
	.NEW_MIPI_PIXEL_VS(LUT_MIPI_PIXEL_VS),
	.NEW_MIPI_PIXEL_D (LUT_MIPI_PIXEL_D )
);

//------ MIPI BRIGE & CAMERA RESET  --
assign CAMERA_PWDN_n  = 1; 
assign MIPI_CS_n      = 0 ; 
assign MIPI_RESET_n   = RESET_N ;


//------ CAMERA MODULE I2C SWITCH  --
assign I2C_RELEASE    =  CAMERA_MIPI_RELAESE & MIPI_BRIDGE_RELEASE; 
assign CAMERA_I2C_SCL = ( I2C_RELEASE  )?  CAMERA_I2C_SCL_AF  : CAMERA_I2C_SCL_MIPI ;   

//-- RESET  --
//-- RESET  --
RESET_DELAY  dl(
           .RESET_N      ( KEY[0] ) ,
           .CLK          ( FPGA_CLK1_50) , 
           .READY0       ( RESET_N),
			  .READY1       ( RESET_N_DELAY ) 
); 

 //------ MIPI BRIGE & CAMERA SETTING  --   
MIPI_BRIDGE_CAMERA_Config    cfin(
          .RESET_N           ( RESET_N_DELAY ), 
          .CLK_50            ( FPGA_CLK1_50 ), 
          .MIPI_I2C_SCL      ( MIPI_I2C_SCL ), 
          .MIPI_I2C_SDA      ( MIPI_I2C_SDA ), 
          .MIPI_I2C_RELEASE  ( MIPI_BRIDGE_RELEASE ),  
          .CAMERA_I2C_SCL    ( CAMERA_I2C_SCL_MIPI ),
          .CAMERA_I2C_SDA    ( CAMERA_I2C_SDA ),
          .CAMERA_I2C_RELAESE( CAMERA_MIPI_RELAESE ),
			 .VCM_RELAESE       ( VCM_RELAESE )
 );

wire  PLL_TEST_OK ;   
  
//------MIPI-AUDIO-VGA REF CLOCK
AUDIO_PLL pll1(
	       .refclk       ( FPGA_CLK1_50),
	       .rst          ( 0 ),
          .outclk_0     ( AUD_CTRL_CLK ),	//1.536MHz			 
			 .locked       ( PLL_TEST_OK  )   	
);

VIDEO_PLL pll2(
	       .refclk       ( FPGA_CLK2_50),
	       .rst          ( 0 ),
	       .outclk_0     ( MIPI_REFCLK ),  //20Mhz
	       .outclk_1     ( VGA_CLK  )      //25Mhz,			 		  
);   
	
	
//--FRAME BUFFER using ON-CHIP SRAM---
ON_CHIP_FRAM  fra( 
         .W_CLK        ( MIPI_PIXEL_CLK ),   
         .W_DE         ( LUT_MIPI_PIXEL_HS & LUT_MIPI_PIXEL_VS  ),  
         .W_DATA       ( LUT_MIPI_PIXEL_D[9:0] ), 
         .W_CLR        ( LUT_MIPI_PIXEL_VS ), 	      
	      .R_CLK        ( VGA_CLK), 
         .R_DATA       ( RD_DATA), 
         .R_CLR        ( VGA_VS ), 
         .R_DE         ( READ_Request)

 );
//-- RAW TO RGB ---
RAW2RGB_J				u4	(	
	      .RST          ( VGA_VS  ),
         .CCD_PIXCLK   ( VGA_CLK ),
	      .mCCD_DATA    ( RD_DATA[9:0] ),
         .VGA_CLK      ( VGA_CLK      ),
         .READ_Request ( READ_Request ),
         .VGA_VS       ( VGA_VS ),	
	      .VGA_HS       ( VGA_HS ) , 	      			
	      .oRed         ( RED  [7:0] ),
	      .oGreen       ( GREEN[7:0] ),
	      .oBlue        ( BLUE [7:0] ),
	      .oDVAL        ( )
			);
//------AOTO FOCUS ENABLE  --
// AUTO_FOCUS_ON  u9( 
//           .CLK_50      ( FPGA_CLK1_50 ), 
//           .I2C_RELEASE ( I2C_RELEASE ), 
//           .AUTO_FOC    ( AUTO_FOC )
//                ) ; 
//------AOTO FOCUS ADJ  --
FOCUS_ADJ adl(
          .CLK_50        ( FPGA_CLK1_50) , 
          .RESET_N       ( I2C_RELEASE ), 
          .RESET_SUB_N   ( I2C_RELEASE ), 
        //   .AUTO_FOC      ( KEY[1] & AUTO_FOC ),
          .SW_Y          ( 0 ),
          .SW_H_FREQ     ( 0 ),   
          .SW_FUC_LINE   ( SW[3] ),   
          .SW_FUC_ALL_CEN( SW[3] ),   
          .VIDEO_HS      ( VGA_HS),
          .VIDEO_VS      ( VGA_VS),
	       .VIDEO_DE      (READ_Request) ,
          .VIDEO_CLK     ( VGA_CLK),
          .iR            ( RED  [7:0]),
          .iG            ( GREEN[7:0]),
          .iB            ( BLUE [7:0]),
          .oR            ( VGA_R[7:0]), 
          .oG            ( VGA_G[7:0]), 
          .oB            ( VGA_B[7:0]),    
          .READY         ( READY),
          .SCL           ( CAMERA_I2C_SCL_AF ), 
          .SDA           ( CAMERA_I2C_SDA ) ,

		  .H_CNT		 ( H_CNT[15:0] ) ,
		  .V_CNT		 ( V_CNT[15:0] )
);  

    
//----- VGA Controller ---
VGA_Controller u1(
	       .iCLK       ( VGA_CLK),		 				 
	       .oVGA_HS    ( VGA_HS  ),
	       .oVGA_VS    ( VGA_VS  ),	       		 
	       .iRST_N      ( 1 ) ,
			 .oRequest	 (TX_DE 	  )
); 
assign READ_Request = TX_DE ; 
	
//--FREQUNCY TEST--
CLOCKMEM  ck3 ( .CLK(MIPI_PIXEL_CLK ),.CLK_FREQ  (25000000 ),.CK_1HZ (D8M_CK_HZ  ));

//--LED STATUS-----
assign LED = {D8M_CK_HZ   , HDMI_TX_INT , CAMERA_MIPI_RELAESE ,MIPI_BRIDGE_RELEASE  } ; 

//---HDMI TX RECONFIG ---- 
HDMI_TX_AD7513 hdmi (
         .RESET_N         (RESET_N  ),
         .CLK_50          ( FPGA_CLK1_50 ),			 
         .AUD_CTRL_CLK    ( AUD_CTRL_CLK ),
         .PLL_TEST_OK     ( PLL_TEST_OK  ) ,    
         .HDMI_I2C_SCL    ( HDMI_I2C_SCL),
         .HDMI_I2C_SDA    ( HDMI_I2C_SDA),		   
         .HDMI_I2S        ( HDMI_I2S_  ),
         .HDMI_LRCLK      ( HDMI_LRCLK ),
         .HDMI_MCLK       ( HDMI_MCLK  ),
         .HDMI_SCLK       ( HDMI_SCLK  ),			
         .HDMI_TX_INT     ( HDMI_TX_INT),
			.READY           ( HDMI_READY )
 );

//-----------MONO2BINARY
MONO2BINARY m2b1(.CLK			(FPGA_CLK1_50),
                 .VGA_MONO		(VGA_R[7:0]),
                 .THRESHOLD		(BINARY_THRESHOLD[7:0]),
                 .BINARY_FLAG	(BINARY_FLAG),
                 .VGA_BINARY	(VGA_BINARY[23:0])
				 );

//-----------FIND_POINT
// FIND_POINT fp1 (
// 	.CLK				(FPGA_CLK1_50),
//     .VGA_VS				(VGA_VS),
//     .BINARY_FLAG		(BINARY_FLAG),
//     .H_CNT				(H_CNT),
//     .V_CNT				(V_CNT),
//     .BINARY_POINTS_H	(POINTS_H_0[15:0]),
//     .BINARY_POINTS_V	(POINTS_V_0[15:0])
// );

FIND_MULTI_POINTS fmp1 (
	.CLK				(FPGA_CLK1_50),
	.VGA_HS				(VGA_HS),
    .VGA_VS				(VGA_VS),
    .BINARY_FLAG		(BINARY_FLAG),
    .H_CNT				(H_CNT),
    .V_CNT				(V_CNT),
	.o_POINTS_H_0		(POINTS_H_0[15:0]),
	.o_POINTS_V_0		(POINTS_V_0[15:0]),
	.o_POINTS_H_1		(POINTS_H_1[15:0]),
	.o_POINTS_V_1		(POINTS_V_1[15:0]),
	.o_POINTS_H_2		(POINTS_H_2[15:0]),
	.o_POINTS_V_2		(POINTS_V_2[15:0]),
	.o_POINTS_H_3		(POINTS_H_3[15:0]),
	.o_POINTS_V_3		(POINTS_V_3[15:0]),
	.o_POINTS_H_4		(POINTS_H_4[15:0]),
	.o_POINTS_V_4		(POINTS_V_4[15:0]),
	.o_POINTS_H_5		(POINTS_H_5[15:0]),
	.o_POINTS_V_5		(POINTS_V_5[15:0]),
	.o_POINTS_H_6		(POINTS_H_6[15:0]),
	.o_POINTS_V_6		(POINTS_V_6[15:0]),
	.o_POINTS_H_7		(POINTS_H_7[15:0]),
	.o_POINTS_V_7		(POINTS_V_7[15:0])
);

//-----------uart_tx
uart_tx #(.CLKS_PER_BIT(BAUD_RATE)) ut0 (
.i_Clock(FPGA_CLK1_50),
.i_Tx_DV(r_TX_DV),
.i_Tx_Byte(TX_BYTE),
.o_Tx_Active(TX_ACTIVE),
.o_Tx_Serial(UART_TX),
.o_Tx_Done(TX_DONE),
.o_Tx_State(TX_STATE)
);

// -----------uart_tx_data
uart_tx_data utd (
	.TX_DONE			(TX_DONE),
	.POINTS_H_0			(POINTS_H_0[15:0]),
	.POINTS_V_0			(POINTS_V_0[15:0]),
	.POINTS_H_1			(POINTS_H_1[15:0]),
	.POINTS_V_1			(POINTS_V_1[15:0]),
	.POINTS_H_2			(POINTS_H_2[15:0]),
	.POINTS_V_2			(POINTS_V_2[15:0]),
	.POINTS_H_3			(POINTS_H_3[15:0]),
	.POINTS_V_3			(POINTS_V_3[15:0]),
	.POINTS_H_4			(POINTS_H_4[15:0]),
	.POINTS_V_4			(POINTS_V_4[15:0]),
	.POINTS_H_5			(POINTS_H_5[15:0]),
	.POINTS_V_5			(POINTS_V_5[15:0]),
	.POINTS_H_6			(POINTS_H_6[15:0]),
	.POINTS_V_6			(POINTS_V_6[15:0]),
	.POINTS_H_7			(POINTS_H_7[15:0]),
	.POINTS_V_7			(POINTS_V_7[15:0]),
	.TX_BYTE			(TX_BYTE)
);

//-----------uart_rx
uart_rx #(.CLKS_PER_BIT(BAUD_RATE)) ur0 (
.i_Clock(FPGA_CLK1_50),
.i_Rx_Serial(UART_RX),
.o_Rx_DV(r_RX_DV),
.o_Rx_Byte(RX_BYTE),
.o_Rx_State(RX_STATE)
);

//-----------uart_rx_data
uart_rx_data urd (
	.r_RX_DV		(r_RX_DV),
	.RX_BYTE		(RX_BYTE),
	.or_COLOR_FLAG	(COLOR_FLAG),
	.o_THRESHOLD	(BINARY_THRESHOLD),
	.o_State 		()
);

//-----------setting
always @(posedge FPGA_CLK1_50) begin
	r_TX_DV = 1'b1;
end

//---VGA TIMG TO HDMI  ----  
assign HDMI_TX_CLK =   VGA_CLK;
// assign HDMI_TX_D   = TX_DE? { VGA_R, VGA_G, VGA_B  }  :0 ;  
// assign HDMI_TX_D   = TX_DE? { VGA_GRAY, VGA_GRAY, VGA_GRAY  }  :0 ;  
assign HDMI_TX_D   = TX_DE? COLOR_FLAG? VGA_BINARY: { VGA_R, VGA_G, VGA_B  }  :0 ;  
assign HDMI_TX_DE  = READ_Request;           
assign HDMI_TX_HS  = VGA_HS                 ;
assign HDMI_TX_VS  = VGA_VS                 ;

//-- HDMI SOUND ON -OFF
assign HDMI_I2S=SW[0]?HDMI_I2S_:0;
	
//-- kevin debug TEST_IO STATUS-----
assign TEST_IO = {MIPI_PIXEL_VS, MIPI_PIXEL_HS, MIPI_PIXEL_CLK, BINARY_FLAG, VGA_VS, VGA_HS, VGA_CLK} ; 
assign TEST_IO_2 = {UART_RX, UART_TX} ; 

//-- kevin debug issp
sources source1 (
	.probe  (POINTS_H_0[15:0])   //  probes.probe
);
sources source2 (
	.probe  (POINTS_V_0[15:0])   //  probes.probe
);

endmodule

