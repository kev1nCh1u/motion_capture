

module uart_rx_data (input r_RX_DV,
                     input RX_BYTE,
                     output reg r_RX_FLAG);
    
    always @(posedge r_RX_DV) begin
        
        if (RX_BYTE == 8'h01)
            r_RX_FLAG <= 1;
        
        else if (RX_BYTE == 8'h00)
        r_RX_FLAG <= 0;
        
    end
    
endmodule
