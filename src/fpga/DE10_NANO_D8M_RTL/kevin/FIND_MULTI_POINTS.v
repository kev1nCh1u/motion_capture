module FIND_MULTI_POINTS (input        	CLK,
                   input            VGA_HS,
                   input            VGA_VS,
                   input        	BINARY_FLAG,
                   input        	[15:0] H_CNT,
                   input        	[15:0] V_CNT,
                   output reg		[15:0] BINARY_POINTS_H,
                   output reg		[15:0] BINARY_POINTS_V);

integer i, j;

reg		rVGA_VS;
reg     rVGA_HS;
reg		[15:0] BINARY_POINTS_H_ARR[0:10][0:50];
reg		[15:0] BINARY_POINTS_V_ARR[0:10][0:50];
reg		[15:0] BINARY_POINTS_NUM[0:10];

reg		POINTS_H_LAST [0:640];
reg		POINTS_H_NOW  [0:640];
reg		[15:0] POINTS_NUM;

reg     [15:0] POINTS_H_MIN[0:10];
reg     [15:0] POINTS_H_MAX[0:10];
reg     [15:0] POINTS_V_MIN[0:10];
reg     [15:0] POINTS_V_MAX[0:10];

//---kevin find multi points ----
always@(posedge CLK)begin
    // ===========================================
    if(POINTS_NUM == 0)
        POINTS_NUM = 1;

    // ============================================
    if (BINARY_FLAG == 1) // find point
    begin
        // BINARY_POINTS_H_ARR[BINARY_POINTS_NUM] = H_CNT; // save h
        // BINARY_POINTS_V_ARR[BINARY_POINTS_NUM] = V_CNT; // save v
        
        // BINARY_POINTS_NUM[0] = BINARY_POINTS_NUM[0] + 1; // point count

        if(POINTS_H_NOW[H_CNT-1] == 0 && POINTS_H_NOW[H_CNT] == 1)
            POINTS_NUM = POINTS_NUM + 1;

        POINTS_H_NOW[H_CNT] = POINTS_NUM;
    end
    else  // no point
    begin
        POINTS_H_NOW[H_CNT] = 0;
    end
    
    // =============================================
    rVGA_HS <= VGA_HS;
    if (rVGA_HS && !VGA_HS) // new line
    begin
        for(i=0; i<=640; i=i+1)
        begin
            POINTS_H_LAST[i] = POINTS_H_NOW[i];
            POINTS_H_NOW[i] = 0;
        end
    end
    
    // =============================================
    rVGA_VS <= VGA_VS;
    if (!rVGA_VS && VGA_VS) // new frame => point reset
    begin
        for(i=0; i<=10; i=i+1)
        begin
            BINARY_POINTS_H = 0;
            BINARY_POINTS_V = 0;
            if (BINARY_POINTS_NUM[i] > 0)
            begin
                BINARY_POINTS_NUM[i] = BINARY_POINTS_NUM[i] / 2;
                
                BINARY_POINTS_H = BINARY_POINTS_H_ARR[i][BINARY_POINTS_NUM[i]];
                BINARY_POINTS_V = BINARY_POINTS_V_ARR[i][BINARY_POINTS_NUM[i]];
                
                BINARY_POINTS_NUM[i] = 0;
            end
        end
        POINTS_NUM = 1;
    end

    
end

endmodule
