

module uart_tx_data (input TX_DONE,
                     input [15:0] POINTS_H_0,
                     input [15:0] POINTS_V_0,
                     input [15:0] POINTS_H_1,
                     input [15:0] POINTS_V_1,
                     input [15:0] POINTS_H_2,
                     input [15:0] POINTS_V_2,
                     input [15:0] POINTS_H_3,
                     input [15:0] POINTS_V_3,
                     output [7:0] TX_BYTE);

reg [7:0] DATA_CNT;
reg [7:0] DATA[0:20];
reg [7:0] r_TX_BYTE;
    
always @(posedge TX_DONE) begin
    DATA[0] = 8'h53; //S
    DATA[1] = 8'h54; //T
    
    DATA[2] = POINTS_H_0[15:8];   // point_x H 0
    DATA[3] = POINTS_H_0[7:0];    // point_x L 0
    DATA[4] = POINTS_V_0[15:8];   // point_y H 0
    DATA[5] = POINTS_V_0[7:0];    // point_y L 0

    DATA[6] = POINTS_H_1[15:8];   // point_x H 1
    DATA[7] = POINTS_H_1[7:0];    // point_x L 1
    DATA[8] = POINTS_V_1[15:8];   // point_y H 1
    DATA[9] = POINTS_V_1[7:0];    // point_y L 1

    DATA[10] = POINTS_H_2[15:8];   // point_x H 2
    DATA[11] = POINTS_H_2[7:0];    // point_x L 2
    DATA[12] = POINTS_V_2[15:8];   // point_y H 2
    DATA[13] = POINTS_V_2[7:0];    // point_y L 2

    DATA[14] = POINTS_H_3[15:8];   // point_x H 3
    DATA[15] = POINTS_H_3[7:0];    // point_x L 3
    DATA[16] = POINTS_V_3[15:8];   // point_y H 3
    DATA[17] = POINTS_V_3[7:0];    // point_y L 3
    
    DATA[18] = 8'h45; //E
    DATA[19] = 8'h4E; //N
    DATA[20] = 8'h44; //D

    r_TX_BYTE <= DATA[DATA_CNT];
    if (DATA_CNT < 20)
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
