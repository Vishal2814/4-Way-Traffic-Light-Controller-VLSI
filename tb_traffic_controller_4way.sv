`timescale 1s/1ms

module tb_traffic_controller_4way;

    logic clk;
    logic rst_n;

    logic NS_red, NS_yellow, NS_green;
    logic EW_red, EW_yellow, EW_green;

    // DUT
    traffic_controller_4way #(
        .T_GREEN(10),
        .T_YELLOW(3)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),

        .NS_red(NS_red),
        .NS_yellow(NS_yellow),
        .NS_green(NS_green),

        .EW_red(EW_red),
        .EW_yellow(EW_yellow),
        .EW_green(EW_green)
    );

    // ======================
    // 1 Hz Clock
    // ======================
    initial clk = 0;
    always #0.5 clk = ~clk;

    // ======================
    // Reset
    // ======================
    initial begin
        rst_n = 0;
        #2;
        rst_n = 1;
    end

    // ======================
    // Console Monitor
    // ======================
    initial begin
        $display("TIME | STATE | TIMER | NS | EW");
        $display("-------------------------------");

        @(posedge rst_n);

        forever begin
            @(posedge clk);

            $display("%4t | %2d    | %2d    | %s  | %s",
                $time,
                dut.current_state,   // numeric state
                dut.timer,
                light(NS_red, NS_yellow, NS_green),
                light(EW_red, EW_yellow, EW_green)
            );
        end
    end

    // ======================
    // Light encoder
    // ======================
    function string light(input logic r, y, g);
        if (g)      light = "G";
        else if (y) light = "Y";
        else if (r) light = "R";
        else        light = "-";
    endfunction

    // ======================
    // Stop simulation
    // ======================
    initial begin
        #100;
        $stop;
    end

endmodule
