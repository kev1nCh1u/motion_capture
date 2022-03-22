

module uart_rx_data (input r_RX_DV,
                     input [7:0] RX_BYTE,
                     output reg or_COLOR_FLAG,
                     output [7:0] o_THRESHOLD,
                     output [3:0] o_State);
    
    reg [3:0] STATE = 4'd0;
    reg RX_BINARY_FLAG = 0;
    reg r_THRESHOLD = 100;
    
    always @(posedge r_RX_DV) begin
        
        case (STATE)
            4'd0:
            begin
                if (RX_BYTE == 8'h53) //S
                    STATE <= STATE + 1;
                else
                    STATE <= 4'd0;
            end
            
            4'd1:
            begin
                if (RX_BYTE == 8'h54) //T
                    STATE <= STATE + 1;
                else
                    STATE <= 4'd0;
            end
            
            4'd2:
            begin
                if (RX_BYTE == 8'h01)
                begin
                    RX_BINARY_FLAG <= 1;
                    STATE <= STATE + 1;
                end
                else if (RX_BYTE == 8'h00)
                begin
                    RX_BINARY_FLAG <= 0;
                    STATE <= STATE + 1;
                end
                else
                    STATE <= 4'd0;
                // or_COLOR_FLAG <= RX_BINARY_FLAG;
            end

            4'd3:
            begin
                r_THRESHOLD <= RX_BYTE;
                STATE          <= 4'd10;
            end
            
            4'd10:
            begin
                if (RX_BYTE == 8'h45) //E
                    STATE <= STATE + 1;
                else
                    STATE <= 4'd0;
            end
            
            4'd11:
            begin
                if (RX_BYTE == 8'h4E) //N
                    STATE <= STATE + 1;
                else
                    STATE <= 4'd0;
            end
            
            4'd12:
            begin
                if (RX_BYTE == 8'h44) //D
                begin
                    or_COLOR_FLAG <= RX_BINARY_FLAG;
                end
                STATE     <= 4'd0;
            end
        endcase
    end
    assign o_State = STATE;
    assign o_THRESHOLD = r_THRESHOLD;
    
endmodule
