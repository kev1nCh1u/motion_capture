/**************************************************************************************************
* FIND_MULTI_POINTS 
* search merge
***************************************************************************************************/


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
                   
                   output reg       [15:0] o_POINTS_LIST,
                   output reg       [15:0] o_POINTS_NUM,
                   output reg       [15:0] test
                   );

reg [5:0]i;
reg [5:0]j; 
reg [5:0]k;

reg     rVGA_HS = 0;
reg		rVGA_VS = 0;
reg		rBINARY_FLAG = 0;

reg		[6:0] POINTS_LIST = 0;
reg		[6:0] POINTS_NUM = 0;
reg     [3:0] POINTS_DATA = 5;
reg		[15:0] POINTS_H_ARR[0:100][0:50]; //[POINTS_LIST][POINTS_NUM] {num,mid,min,max,group,...}
reg		[15:0] POINTS_V_ARR[0:100][0:50];

reg		[2:0] POINT_COUNT = 0;
reg		[15:0] POINT_H[0:3]; //[POINT_COUNT]
reg		[15:0] POINT_V[0:3];
reg		[2:0] POINT_GROUP = 0;
reg		[7:0] POINT_GROUP_NUM[0:3];
reg		[15:0] POINT_RANGE[0:3][0:2]; // {h_min, h_max, v}

reg		[15:0] BUFF;

//---kevin find multi points ----
always@(posedge CLK)begin
    // ================= new point =============================
    rBINARY_FLAG <= BINARY_FLAG;
    if (rBINARY_FLAG && !BINARY_FLAG) // lower edge, new point
    begin
        POINTS_H_ARR[POINTS_LIST][0] = POINTS_NUM+ POINTS_DATA; // save POINTS_NUM
        POINTS_V_ARR[POINTS_LIST][0] = POINTS_NUM+ POINTS_DATA; // save POINTS_NUM

        POINTS_H_ARR[POINTS_LIST][1] = POINTS_H_ARR[POINTS_LIST][(POINTS_NUM >> 1)+ POINTS_DATA]; // save MID
        POINTS_V_ARR[POINTS_LIST][1] = POINTS_V_ARR[POINTS_LIST][(POINTS_NUM >> 1)+ POINTS_DATA]; // save MID

        POINTS_H_ARR[POINTS_LIST][2] = POINTS_H_ARR[POINTS_LIST][POINTS_DATA]; // save MIN
        POINTS_V_ARR[POINTS_LIST][2] = POINTS_V_ARR[POINTS_LIST][POINTS_DATA]; // save MIN

        POINTS_H_ARR[POINTS_LIST][3] = POINTS_H_ARR[POINTS_LIST][POINTS_NUM + POINTS_DATA - 1]; // save MAX
        POINTS_V_ARR[POINTS_LIST][3] = POINTS_V_ARR[POINTS_LIST][POINTS_NUM + POINTS_DATA - 1]; // save MAX
        
        // find group
        $display("================= new_point ====================");
        for(i=0; i<=POINT_GROUP; i=i+1)
        begin
            $display("i:%3d  h_min:%3d  h_max:%3d  h_point:%3d  v:%3d  v_point:%3d ", 
            i, POINT_RANGE[i][0], POINT_RANGE[i][1], POINTS_H_ARR[POINTS_LIST][1], POINT_RANGE[i][2], POINTS_V_ARR[POINTS_LIST][1]);
            if((POINTS_H_ARR[POINTS_LIST][1] > POINT_RANGE[i][0] // in h min
            && POINTS_H_ARR[POINTS_LIST][1] < POINT_RANGE[i][1] // in h max
            && (POINTS_V_ARR[POINTS_LIST][1] - POINT_RANGE[i][2]) <= 1) // in v
            || i == POINT_GROUP )
            begin // in range
                POINTS_H_ARR[POINTS_LIST][4] = i;
                POINTS_V_ARR[POINTS_LIST][4] = i;

                POINT_RANGE[i][0] = POINTS_H_ARR[POINTS_LIST][2]; // inherit h min
                POINT_RANGE[i][1] = POINTS_H_ARR[POINTS_LIST][3]; // inherit h max
                POINT_RANGE[i][2] = POINTS_V_ARR[POINTS_LIST][1]; // inherit v mid

                POINT_H[POINTS_H_ARR[i][4]] = POINT_H[POINTS_H_ARR[i][4]] + POINTS_H_ARR[POINTS_LIST][1]; // h mid sum
                POINT_V[POINTS_V_ARR[i][4]] = POINT_V[POINTS_V_ARR[i][4]] + POINTS_V_ARR[POINTS_LIST][1]; // v mid sum
                POINT_GROUP_NUM[POINTS_H_ARR[i][4]] = POINT_GROUP_NUM[POINTS_H_ARR[i][4]] + 1; // count point group

                $display("link list:%d to group:%d", POINTS_LIST, i);
                if(i == POINT_GROUP)
                begin
                    $display("new_group:%d POINT_GROUP:%d ", i, POINT_GROUP);
                    POINT_GROUP = POINT_GROUP + 1;
                end
                i = POINT_GROUP+1;  
            end
        end

        POINTS_LIST = POINTS_LIST + 1;
        POINTS_NUM = 0;
    end

    // ================== find point ==========================
    if (BINARY_FLAG == 1) // find point
    begin
        POINTS_H_ARR[POINTS_LIST][POINTS_NUM+ POINTS_DATA] = H_CNT; // save h
        POINTS_V_ARR[POINTS_LIST][POINTS_NUM+ POINTS_DATA] = V_CNT; // save v

        POINTS_NUM = POINTS_NUM + 1;
    end
    
    // ================= new line ============================
    rVGA_HS <= VGA_HS;
    if (rVGA_HS && !VGA_HS) // lower edge, new line
    begin

    end
    
    // ================== new frame ===========================
    rVGA_VS <= VGA_VS;
    if (!rVGA_VS && VGA_VS) // upper edge, new frame
    begin
        // reset
        POINT_COUNT = 0;
        for(i=0; i<=3; i=i+1)
        begin
            POINT_H[i] = 0;
            POINT_V[i] = 0;
            POINT_GROUP_NUM[i] = 0;
        end
    end

    // ================== new frame ===========================
    rVGA_VS <= VGA_VS;
    if (rVGA_VS && !VGA_VS) // lower edge, new frame
    begin
        // reset
        // POINT_COUNT = 0;
        // for(i=0; i<=3; i=i+1)
        // begin
        //     POINT_H[i] = 0;
        //     POINT_V[i] = 0;
        //     POINT_GROUP_NUM[i] = 0;
        // end

        // for(i=0; i<POINTS_LIST; i=i+1)
        // begin

        //     POINTS_NUM = 0; // clean count sum
        //     if(POINTS_H_ARR[i][0] != ~16'd0) // have value
        //     begin
        //         $display("========== LIST:%3d ====================", i);
        //         for(j=i+1; j<POINTS_LIST; j=j+1)
        //         begin
        //             if(POINTS_H_ARR[j][0] != ~16'd0) // have value
        //             begin
        //                 $display("N:%3d    SX:%3d    SY:%3d    DX:%3d    DY:%3d",
        //                  j, POINTS_H_ARR[i][1], POINTS_V_ARR[i][1], POINTS_H_ARR[j][1], POINTS_V_ARR[j][1]);
        //                 BUFF = POINTS_H_ARR[i][1] - POINTS_H_ARR[j][1]; // find two point distance
        //                 if(BUFF[15]) // if negative
        //                     BUFF = ~BUFF[15:0]+1; // abs
        //                 if(BUFF <= 20 && ((POINTS_V_ARR[j][1]-POINTS_V_ARR[i][1]) <= 1)) // close enough
        //                 begin
        //                     $display("merge");
        //                     POINT_H[POINT_COUNT] = POINT_H[POINT_COUNT] + POINTS_H_ARR[j][1]; // sum H
        //                     POINT_V[POINT_COUNT] = POINT_V[POINT_COUNT] + POINTS_V_ARR[j][1]; // sum V
        //                     POINTS_H_ARR[j][0] = -1; // clean H
        //                     POINTS_H_ARR[j][0] = -1; // clean V
        //                     POINTS_NUM = POINTS_NUM + 1; // count sum
        //                     POINTS_V_ARR[i][1] = POINTS_V_ARR[j][1]; // inherit V
        //                 end
        //             end
        //         end

        //         if(POINTS_NUM > 0) // more than one point
        //         begin
        //             POINT_H[POINT_COUNT] = POINT_H[POINT_COUNT] / POINTS_NUM; // average H
        //             POINT_V[POINT_COUNT] = POINT_V[POINT_COUNT] / POINTS_NUM; // average V
        //             POINT_COUNT = POINT_COUNT + 1; // count point
        //         end
        //     end

        // end

        // link
        $display("POINT_GROUP: %d", POINT_GROUP);
        for(i=0; i<POINT_GROUP; i=i+1)
        begin
            POINT_H[i] = POINT_H[i] / POINT_GROUP_NUM[i]; // average H
            POINT_V[i] = POINT_V[i] / POINT_GROUP_NUM[i]; // average V
        end
        POINT_COUNT = POINT_GROUP;

        // output
        $display("============= result =================");
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

        POINTS_LIST = 0;
        POINTS_NUM = 0;
        POINT_GROUP = 0;

    end

    o_POINTS_LIST = POINTS_LIST;
    o_POINTS_NUM = POINTS_NUM;    

    
end

endmodule
