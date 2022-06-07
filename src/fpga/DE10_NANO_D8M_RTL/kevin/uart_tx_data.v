

module uart_tx_data (input TX_DONE,
                     input [15:0] POINTS_H0,
                     input [15:0] POINTS_V0,
                     input [15:0] POINTS_H1,
                     input [15:0] POINTS_V1,
                     input [15:0] POINTS_H2,
                     input [15:0] POINTS_V2,
                     input [15:0] POINTS_H3,
                     input [15:0] POINTS_V3,
                     input [15:0] POINTS_H4,
                     input [15:0] POINTS_V4,
                     input [15:0] POINTS_H5,
                     input [15:0] POINTS_V5,
                     input [15:0] POINTS_H6,
                     input [15:0] POINTS_V6,
                     input [15:0] POINTS_H7,
                     input [15:0] POINTS_V7,
                     input [15:0] POINTS_H8,
                     input [15:0] POINTS_V8,
                     input [15:0] POINTS_H9,
                     input [15:0] POINTS_V9,
                     input [15:0] POINTS_H10,
                     input [15:0] POINTS_V10,
                     input [15:0] POINTS_H11,
                     input [15:0] POINTS_V11,
                     input [15:0] POINTS_H12,
                     input [15:0] POINTS_V12,
                     input [15:0] POINTS_H13,
                     input [15:0] POINTS_V13,
                     input [15:0] POINTS_H14,
                     input [15:0] POINTS_V14,
                     input [15:0] POINTS_H15,
                     input [15:0] POINTS_V15,
                     output [7:0] TX_BYTE);

reg [7:0] DATA_CNT;
reg [7:0] DATA[0:100];
reg [7:0] r_TX_BYTE;
    
always @(posedge TX_DONE) begin
    DATA[0] = 8'h53; //S
    DATA[1] = 8'h54; //T
    
    DATA[2] = POINTS_H0[15:8]; 
    DATA[3] = POINTS_H0[7:0];  
    DATA[4] = POINTS_V0[15:8]; 
    DATA[5] = POINTS_V0[7:0];  

    DATA[6] = POINTS_H1[15:8];   
    DATA[7] = POINTS_H1[7:0];    
    DATA[8] = POINTS_V1[15:8];   
    DATA[9] = POINTS_V1[7:0];    

    DATA[10] = POINTS_H2[15:8];   
    DATA[11] = POINTS_H2[7:0];    
    DATA[12] = POINTS_V2[15:8];   
    DATA[13] = POINTS_V2[7:0];    

    DATA[14] = POINTS_H3[15:8];   
    DATA[15] = POINTS_H3[7:0];    
    DATA[16] = POINTS_V3[15:8];   
    DATA[17] = POINTS_V3[7:0];    

    DATA[18] = POINTS_H4[15:8];   
    DATA[19] = POINTS_H4[7:0];    
    DATA[20] = POINTS_V4[15:8];   
    DATA[21] = POINTS_V4[7:0];    

    DATA[22] = POINTS_H5[15:8];   
    DATA[23] = POINTS_H5[7:0];    
    DATA[24] = POINTS_V5[15:8];   
    DATA[25] = POINTS_V5[7:0];    

    DATA[26] = POINTS_H6[15:8];   
    DATA[27] = POINTS_H6[7:0];    
    DATA[28] = POINTS_V6[15:8];   
    DATA[29] = POINTS_V6[7:0];    

    DATA[30] = POINTS_H7[15:8];  
    DATA[31] = POINTS_H7[7:0];   
    DATA[32] = POINTS_V7[15:8];  
    DATA[33] = POINTS_V7[7:0];   

    DATA[34] = POINTS_H8[15:8]; 
    DATA[35] = POINTS_H8[7:0];  
    DATA[36] = POINTS_V8[15:8]; 
    DATA[37] = POINTS_V8[7:0];  

    DATA[38] = POINTS_H9[15:8];   
    DATA[39] = POINTS_H9[7:0];    
    DATA[40] = POINTS_V9[15:8];   
    DATA[41] = POINTS_V9[7:0];    

    DATA[42] = POINTS_H10[15:8];   
    DATA[43] = POINTS_H10[7:0];    
    DATA[44] = POINTS_V10[15:8];   
    DATA[45] = POINTS_V10[7:0];    

    DATA[46] = POINTS_H11[15:8];   
    DATA[47] = POINTS_H11[7:0];    
    DATA[48] = POINTS_V11[15:8];   
    DATA[49] = POINTS_V11[7:0];    

    DATA[50] = POINTS_H12[15:8];   
    DATA[51] = POINTS_H12[7:0];    
    DATA[52] = POINTS_V12[15:8];   
    DATA[53] = POINTS_V12[7:0];    

    DATA[54] = POINTS_H13[15:8];   
    DATA[55] = POINTS_H13[7:0];    
    DATA[56] = POINTS_V13[15:8];   
    DATA[57] = POINTS_V13[7:0];    

    DATA[58] = POINTS_H14[15:8];   
    DATA[59] = POINTS_H14[7:0];    
    DATA[60] = POINTS_V14[15:8];   
    DATA[61] = POINTS_V14[7:0];    

    DATA[62] = POINTS_H15[15:8];  
    DATA[63] = POINTS_H15[7:0];   
    DATA[64] = POINTS_V15[15:8];  
    DATA[65] = POINTS_V15[7:0];   
    
    DATA[66] = 8'h45; //E
    DATA[67] = 8'h4E; //N
    DATA[68] = 8'h44; //D

    r_TX_BYTE <= DATA[DATA_CNT];
    if (DATA_CNT < 68)
    begin
        DATA_CNT <= DATA_CNT + 1;
    end
    else
    begin
        DATA_CNT <= 0;
    end
end

assign TX_BYTE = r_TX_BYTE;

endmodule
