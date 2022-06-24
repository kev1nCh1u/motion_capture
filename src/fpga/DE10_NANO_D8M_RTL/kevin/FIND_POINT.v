module FIND_POINT (input        	CLK,
                   input            VGA_VS,
                   input        	BINARY_FLAG,
                   input        	[15:0] H_CNT,
                   input        	[15:0] V_CNT,
                   output reg		[15:0] BINARY_POINTS_H,
                   output reg		[15:0] BINARY_POINTS_V);

reg		[15:0] BINARY_POINTS_H_ARR[15:0];
reg		[15:0] BINARY_POINTS_V_ARR[15:0];
reg		[15:0] BINARY_POINTS_NUM;
reg		rVGA_VS;

//---kevin find point ----
always@(posedge CLK)begin
    if (BINARY_FLAG == 1) // find point
    begin
        BINARY_POINTS_H_ARR[BINARY_POINTS_NUM] = H_CNT; // save h
        BINARY_POINTS_V_ARR[BINARY_POINTS_NUM] = V_CNT; // save v
        
        BINARY_POINTS_NUM = BINARY_POINTS_NUM + 1; // point count
    end
    
    rVGA_VS <= VGA_VS;
    if (!rVGA_VS && VGA_VS) // upper edge, point reset
    begin
        BINARY_POINTS_H = 0;
        BINARY_POINTS_V = 0;
        if (BINARY_POINTS_NUM > 0)
        begin
            BINARY_POINTS_NUM = BINARY_POINTS_NUM / 2; // median num
            
            BINARY_POINTS_H = BINARY_POINTS_H_ARR[BINARY_POINTS_NUM]; // median point H
            BINARY_POINTS_V = BINARY_POINTS_V_ARR[BINARY_POINTS_NUM]; // median point V
            
            BINARY_POINTS_NUM = 0;
        end
    end
end

endmodule
