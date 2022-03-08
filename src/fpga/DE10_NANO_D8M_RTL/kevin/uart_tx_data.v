

module uart_tx_data (input TX_DONE,
                     input [15:0] BINARY_POINTS_H,
                     input [15:0] BINARY_POINTS_V,
                     output [7:0] TX_BYTE);

reg [3:0] DATA_CNT;
reg [7:0] DATA[10:0];
reg [7:0] r_TX_BYTE;
    
always @(posedge TX_DONE) begin
    DATA[0] = 8'h53; //S
    DATA[1] = 8'h54; //T
    
    DATA[2]           = BINARY_POINTS_H[15:8]; // point_x H
    DATA[3]           = BINARY_POINTS_H[7:0]; // point_x L
    DATA[4]           = BINARY_POINTS_V[15:8];  // point_y H
    DATA[5]           = BINARY_POINTS_V[7:0];  // point_y L
    
    DATA[6] = 8'h45; //E
    DATA[7] = 8'h4E; //N
    DATA[8] = 8'h44; //D

    r_TX_BYTE <= DATA[DATA_CNT];
    if (DATA_CNT < 8)
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
