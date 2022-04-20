// test banch FIND_MULTI_POINTS

`timescale 1ns/1ns

module T;
    reg CLK;
    reg VGA_HS;
    reg VGA_VS;
    reg BINARY_FLAG;
    reg [15:0] H_CNT;
    reg [15:0] V_CNT;

    wire [15:0] POINTS_H_0;
    wire [15:0] POINTS_V_0;
    wire [15:0] POINTS_H_1;
    wire [15:0] POINTS_V_1;
    wire [15:0] POINTS_H_2;
    wire [15:0] POINTS_V_2;
    wire [15:0] POINTS_H_3;
    wire [15:0] POINTS_V_3;

    wire [15:0] POINTS_LIST;
    wire [15:0] POINTS_NUM;
    wire [15:0] test;

    reg BINARY_FRAME[0:99][0:199]; // [y][x]

    integer i, j;

    FIND_MULTI_POINTS UUT (
        .CLK            (CLK),
        .VGA_HS         (VGA_HS),
        .VGA_VS         (VGA_VS),
        .BINARY_FLAG    (BINARY_FLAG),
        .H_CNT          (H_CNT),
        .V_CNT          (V_CNT),
        .o_POINTS_H_0     (POINTS_H_0),
        .o_POINTS_V_0     (POINTS_V_0),
        .o_POINTS_H_1     (POINTS_H_1),
        .o_POINTS_V_1     (POINTS_V_1),
        .o_POINTS_H_2     (POINTS_H_2),
        .o_POINTS_V_2     (POINTS_V_2),
        .o_POINTS_H_3     (POINTS_H_3),
        .o_POINTS_V_3     (POINTS_V_3),
        .o_POINTS_LIST    (POINTS_LIST),
        .o_POINTS_NUM     (POINTS_NUM),
        .test           (test)
    );

    initial
    begin
        $display("================== start ===========================");

        CLK = 1;

        $readmemb("BINARY_FRAME_DATA.txt", BINARY_FRAME);

        ///////////////////// a frame
        VGA_HS = 0;
        VGA_VS = 0;
        #100;

        VGA_VS = 1;
        for(i=0; i<100; i=i+1) // y
        begin
            VGA_HS = 1;
            V_CNT = i;
            for(j=0; j<200; j=j+1) // x
            begin
                H_CNT = j;
                BINARY_FLAG = BINARY_FRAME[i][j];
                #100;
            end
            VGA_HS = 0;
            BINARY_FLAG = 0;
            #100;
        end

        VGA_HS = 0;
        VGA_VS = 0;
        #100;

        ////////////////////// a frame
        VGA_HS = 0;
        VGA_VS = 0;
        #100;

        VGA_VS = 1;
        for(i=0; i<100; i=i+1) // y
        begin
            VGA_HS = 1;
            V_CNT = i;
            for(j=0; j<200; j=j+1) // x
            begin
                H_CNT = j;
                BINARY_FLAG = BINARY_FRAME[i][j];
                #100;
            end
            VGA_HS = 0;
            BINARY_FLAG = 0;
            #100;
        end

        VGA_HS = 0;
        VGA_VS = 0;
        #100;

        $stop;
    end

    always #50 CLK = ~CLK;


endmodule