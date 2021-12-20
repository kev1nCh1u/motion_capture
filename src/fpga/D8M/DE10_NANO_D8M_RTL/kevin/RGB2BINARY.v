module RGB2BINARY (input CLK,
                 input [7:0] VGA_R,
                 input [7:0] VGA_G,
                 input [7:0] VGA_B,
                 input [7:0] THRESHOLD,
                 output reg [23:0] VGA_GRAY,
                 output BINARY_FLAG,
                 output [23:0] VGA_BINARY);
    
    //---kevin cvt rgb to gray ----
    always@(posedge CLK)begin
        VGA_GRAY = (VGA_R * 299 + VGA_G * 587 + VGA_B * 114) / 1000;
    end
    //---kevin gray to mono ----
    assign BINARY_FLAG = (VGA_GRAY > THRESHOLD) ? 1 : 0;
    assign VGA_BINARY = (BINARY_FLAG == 1) ? 24'hFFFFFF : 0;
endmodule