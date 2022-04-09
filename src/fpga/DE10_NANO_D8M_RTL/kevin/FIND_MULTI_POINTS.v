module FIND_MULTI_POINTS (
                   input        	CLK,
                   input            VGA_HS,
                   input            VGA_VS,
                   input        	BINARY_FLAG,
                   input        	[15:0] H_CNT,
                   input        	[15:0] V_CNT,
                   output reg		[15:0] o_POINTS_H_0,
                   output reg		[15:0] o_POINTS_V_0,
                   output reg		[15:0] o_POINTS_H_1,
                   output reg		[15:0] o_POINTS_V_1,
                   output reg		[15:0] o_POINTS_H_2,
                   output reg		[15:0] o_POINTS_V_2,
                   output reg		[15:0] o_POINTS_H_3,
                   output reg		[15:0] o_POINTS_V_3,
                   
                   output reg       [15:0] o_POINTS_GROUP,
                   output reg       [15:0] o_POINTS_NUM,
                   output reg       [15:0] test
                   );

integer i, j, k;

reg     rVGA_HS = 0;
reg		rVGA_VS = 0;
reg		rBINARY_FLAG = 0;

reg		[15:0] POINTS_GROUP = 0;
reg		[15:0] POINTS_NUM = 0;
reg		[15:0] POINTS_H_ARR[0:10][0:50]; //[POINTS_GROUP][POINTS_NUM]
reg		[15:0] POINTS_V_ARR[0:10][0:50];

reg		[15:0] POINT_COUNT;
reg		[15:0] POINT_H[0:3]; //[POINT_COUNT]
reg		[15:0] POINT_V[0:3];

reg		[15:0] BUFF;

//---kevin find multi points ----
always@(posedge CLK)begin
    // ===========================================
    // if(POINTS_NUM == 0)
    //     POINTS_NUM = 1;

    // ==============================================
    rBINARY_FLAG <= BINARY_FLAG;
    if (rBINARY_FLAG && !BINARY_FLAG) // lower edge, new point
    begin
        POINTS_NUM = POINTS_NUM / 2; // median num
        POINTS_H_ARR[POINTS_GROUP][0] = POINTS_H_ARR[POINTS_GROUP][POINTS_NUM]; // median point

        POINTS_GROUP = POINTS_GROUP + 1;
        POINTS_NUM = 0;
    end

    // ============================================
    if (BINARY_FLAG == 1) // find point
    begin
        POINTS_H_ARR[POINTS_GROUP][POINTS_NUM] = H_CNT; // save h
        POINTS_V_ARR[POINTS_GROUP][POINTS_NUM] = V_CNT; // save v

        POINTS_NUM = POINTS_NUM + 1;
    end
    
    // =============================================
    rVGA_HS <= VGA_HS;
    if (rVGA_HS && !VGA_HS) // lower edge, new line
    begin

    end
    
    // =============================================
    rVGA_VS <= VGA_VS;
    if (rVGA_VS && !VGA_VS) // lower edge, new frame
    begin
        POINT_COUNT = 0;
        for(i=0; i<POINTS_GROUP; i=i+1)
        begin
            POINTS_NUM = 0; // clean count sum
            POINT_H[POINT_COUNT] = 0;
            POINT_V[POINT_COUNT] = 0;
            if(POINTS_H_ARR[i][0] != ~16'd0) // have value
            begin
                for(j=i+1; j<POINTS_GROUP; j=j+1)
                begin
                    if(POINTS_H_ARR[j][0] != ~16'd0) // have value
                    begin
                        $display("G:%3d    N:%3d    SX:%3d    SY:%3d    DX:%3d    DY:%3d",
                         i, j, POINTS_H_ARR[i][0], POINTS_V_ARR[i][0], POINTS_H_ARR[j][0], POINTS_V_ARR[j][0]);
                        BUFF = POINTS_H_ARR[i][0] - POINTS_H_ARR[j][0]; // find two point distance
                        if(BUFF[15]) // if negative
                            BUFF = ~BUFF[15:0]+1; // abs
                        if(BUFF <= 2 && ((POINTS_V_ARR[j][0]-POINTS_V_ARR[i][0]) <= 2)) // close enough
                        begin
                            $display("merge");
                            POINT_H[POINT_COUNT] = POINT_H[POINT_COUNT] + POINTS_H_ARR[j][0]; // sum H
                            POINT_V[POINT_COUNT] = POINT_V[POINT_COUNT] + POINTS_V_ARR[j][0]; // sum V
                            POINTS_H_ARR[j][0] = -1; // clean H
                            POINTS_H_ARR[j][0] = -1; // clean V
                            POINTS_NUM = POINTS_NUM + 1; // count sum
                        end

                    end
                end

                if(POINTS_NUM > 0) // more than one point
                begin
                    POINT_H[POINT_COUNT] = POINT_H[POINT_COUNT] / POINTS_NUM; // average H
                    POINT_V[POINT_COUNT] = POINT_V[POINT_COUNT] / POINTS_NUM; // average V
                    POINT_COUNT = POINT_COUNT + 1; // count point
                end
            end
        end
        
        // output
        for(i=0; i<POINT_COUNT; i=i+1)
        begin
            $display("p:%3d    X:%3d    Y:%3d", i, POINT_H[i], POINT_V[i]);
        end
        o_POINTS_H_0 = POINT_H[0];
        o_POINTS_V_0 = POINT_V[0];
        o_POINTS_H_1 = POINT_H[1];
        o_POINTS_V_1 = POINT_V[1];
        o_POINTS_H_2 = POINT_H[2];
        o_POINTS_V_2 = POINT_V[2];
        o_POINTS_H_3 = POINT_H[3];
        o_POINTS_V_3 = POINT_V[3];

        POINTS_GROUP = 0;
        POINTS_NUM = 0;
    end

    o_POINTS_GROUP = POINTS_GROUP;
    o_POINTS_NUM = POINTS_NUM;    

    
end

endmodule
