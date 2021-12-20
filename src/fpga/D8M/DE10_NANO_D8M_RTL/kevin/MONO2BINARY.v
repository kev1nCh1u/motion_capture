module MONO2BINARY (input CLK,
                 input [7:0] VGA_MONO,
                 input [7:0] THRESHOLD,
                 output BINARY_FLAG,
                 output [23:0] VGA_BINARY);
    
    //---kevin mono to binary ----
    assign BINARY_FLAG = (VGA_MONO > THRESHOLD) ? 1 : 0;
    assign VGA_BINARY = (BINARY_FLAG == 1) ? 24'hFFFFFF : 0;
endmodule