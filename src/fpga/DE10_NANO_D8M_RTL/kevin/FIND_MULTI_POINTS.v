module FIND_MULTI_POINTS (
                   input        	CLK,
                   input            VGA_HS,
                   input            VGA_VS,
                   input        	BINARY_FLAG,
                   input        	[15:0] H_CNT,
                   input        	[15:0] V_CNT,
                   output reg		[15:0] POINTS_H_0,
                   output reg		[15:0] POINTS_V_0,
                   output reg		[15:0] POINTS_H_1,
                   output reg		[15:0] POINTS_V_1,
                   output reg		[15:0] POINTS_H_2,
                   output reg		[15:0] POINTS_V_2,
                   output reg		[15:0] POINTS_H_3,
                   output reg		[15:0] POINTS_V_3,

                   output reg       [15:0] test
                   );

integer i, j, k;

reg     rVGA_HS = 0;
reg		rVGA_VS = 0;
reg		rBINARY_FLAG;

reg		[15:0] POINTS_GROUP;
reg		[15:0] POINTS_NUM;
reg		[15:0] POINTS_H_ARR[0:10][0:50]; //[POINTS_GROUP][POINTS_NUM]
reg		[15:0] POINTS_V_ARR[0:10][0:50];

reg		[15:0] o_POINT_COUNT;
reg		[15:0] o_POINT_H[0:3]; //[o_POINT_COUNT]
reg		[15:0] o_POINT_V[0:3];

reg		[15:0] BUFF;

//---kevin find multi points ----
always@(posedge CLK)begin
    // ===========================================
    // if(POINTS_NUM == 0)
    //     POINTS_NUM = 1;

    // test = 1;

    // ==============================================
    rBINARY_FLAG <= BINARY_FLAG;
    if (!rBINARY_FLAG && BINARY_FLAG) // new point
    begin
        POINTS_NUM = POINTS_NUM / 2;
        POINTS_H_ARR[POINTS_GROUP][0] = POINTS_H_ARR[POINTS_GROUP][POINTS_NUM];

        test = POINTS_H_ARR[POINTS_GROUP][0];

        POINTS_GROUP = POINTS_GROUP + 1;
        POINTS_NUM = 0;

        
    end

    // ============================================
    if (BINARY_FLAG == 1) // find point
    begin
        POINTS_H_ARR[POINTS_GROUP][POINTS_NUM] = H_CNT; // save h
        POINTS_V_ARR[POINTS_GROUP][POINTS_NUM] = V_CNT; // save v

        // test = POINTS_H_ARR[POINTS_GROUP][POINTS_NUM];

        POINTS_NUM = POINTS_NUM + 1;
    end

    // test = H_CNT;
    
    // =============================================
    rVGA_HS <= VGA_HS;
    if (!rVGA_HS && VGA_HS) // new line
    begin

    end
    
    // =============================================
    rVGA_VS <= VGA_VS;
    if (!rVGA_VS && VGA_VS) // new frame
    begin
        o_POINT_COUNT = 0;
        for(i=0; i<POINTS_GROUP; i=i+1)
        begin
            POINTS_NUM = 0;
            for(j=0; j<POINTS_GROUP; j=j+1)
            begin
                if(POINTS_H_ARR[i][0] && POINTS_H_ARR[j][0])
                begin
                    BUFF = POINTS_H_ARR[i][0] - POINTS_H_ARR[j][0];
                    if(BUFF[15])
                        BUFF = ~BUFF[15:0]+1;
                    if(BUFF < 10)
                    begin
                        POINTS_NUM = POINTS_NUM + 1;
                        POINTS_H_ARR[i][0] = POINTS_H_ARR[i][0] + POINTS_H_ARR[j][0];
                        POINTS_V_ARR[i][0] = POINTS_V_ARR[i][0] + POINTS_V_ARR[j][0];
                        POINTS_H_ARR[j][0] = 0;
                        POINTS_H_ARR[j][0] = 0;
                    end

                end
            end
            POINTS_H_ARR[i][0] = POINTS_H_ARR[i][0] / POINTS_NUM;
            POINTS_V_ARR[i][0] = POINTS_V_ARR[i][0] / POINTS_NUM;

            o_POINT_H[o_POINT_COUNT] = POINTS_H_ARR[i][0];
            o_POINT_V[o_POINT_COUNT] = POINTS_V_ARR[i][0];

            o_POINT_COUNT = o_POINT_COUNT + 1;
        end
        
        // output
        POINTS_H_0 = o_POINT_H[0];
        POINTS_V_0 = o_POINT_V[0];
        POINTS_H_1 = o_POINT_H[1];
        POINTS_V_1 = o_POINT_V[1];
        POINTS_H_2 = o_POINT_H[2];
        POINTS_V_2 = o_POINT_V[2];
        POINTS_H_3 = o_POINT_H[3];
        POINTS_V_3 = o_POINT_V[3];

        POINTS_GROUP = 0;
        POINTS_NUM = 0;
    end

    
end

endmodule
