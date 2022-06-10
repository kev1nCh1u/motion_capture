

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
    
    DATA[1] = POINTS_H0[15:8]; 
    DATA[2] = POINTS_H0[7:0];  
    DATA[3] = POINTS_V0[15:8]; 
    DATA[4] = POINTS_V0[7:0];  

    DATA[5] = POINTS_H1[15:8];   
    DATA[6] = POINTS_H1[7:0];    
    DATA[7] = POINTS_V1[15:8];   
    DATA[8] = POINTS_V1[7:0];    

    DATA[9] = POINTS_H2[15:8];   
    DATA[10] = POINTS_H2[7:0];    
    DATA[11] = POINTS_V2[15:8];   
    DATA[12] = POINTS_V2[7:0];    

    DATA[13] = POINTS_H3[15:8];   
    DATA[14] = POINTS_H3[7:0];    
    DATA[15] = POINTS_V3[15:8];   
    DATA[16] = POINTS_V3[7:0];    

    DATA[17] = POINTS_H4[15:8];   
    DATA[18] = POINTS_H4[7:0];    
    DATA[19] = POINTS_V4[15:8];   
    DATA[20] = POINTS_V4[7:0];    

    DATA[21] = POINTS_H5[15:8];   
    DATA[22] = POINTS_H5[7:0];    
    DATA[23] = POINTS_V5[15:8];   
    DATA[24] = POINTS_V5[7:0];    

    DATA[25] = POINTS_H6[15:8];   
    DATA[26] = POINTS_H6[7:0];    
    DATA[27] = POINTS_V6[15:8];   
    DATA[28] = POINTS_V6[7:0];    

    DATA[29] = POINTS_H7[15:8];  
    DATA[30] = POINTS_H7[7:0];   
    DATA[31] = POINTS_V7[15:8];  
    DATA[32] = POINTS_V7[7:0];   

    DATA[33] = 8'h45; //E

    r_TX_BYTE <= DATA[DATA_CNT];
    if (DATA_CNT < 33)
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
