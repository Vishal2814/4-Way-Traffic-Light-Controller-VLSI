module traffic_controller_4way #(
    parameter int T_GREEN  = 10,
    parameter int T_YELLOW = 3
)(
    input  logic clk,
    input  logic rst_n,

    output logic NS_red,
    output logic NS_yellow,
    output logic NS_green,

    output logic EW_red,
    output logic EW_yellow,
    output logic EW_green
);

    // ==============================
    // STATE TYPE (DECLARE FIRST!)
    // ==============================
    typedef enum logic [1:0] {
        S_NS_GREEN,
        S_NS_YELLOW,
        S_EW_GREEN,
        S_EW_YELLOW
    } state_t;

    state_t current_state, next_state;

    // ==============================
    // TIMER
    // ==============================
    logic [$clog2(T_GREEN+1)-1:0] timer;
    logic timer_done;

    // ==============================
    // STATE REGISTER
    // ==============================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= S_NS_GREEN;
        else
            current_state <= next_state;
    end

    // ==============================
    // TIMER LOGIC
    // ==============================
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            timer <= '0;
        else if (current_state != next_state)
            timer <= '0;
        else
            timer <= timer + 1'b1;
    end

    // ==============================
    // TIMER DONE
    // ==============================
    always_comb begin
        case (current_state)
            S_NS_GREEN,
            S_EW_GREEN:   timer_done = (timer == T_GREEN-1);

            S_NS_YELLOW,
            S_EW_YELLOW:  timer_done = (timer == T_YELLOW-1);

            default:      timer_done = 1'b0;
        endcase
    end

    // ==============================
    // NEXT STATE LOGIC
    // ==============================
    always_comb begin
        next_state = current_state;

        if (timer_done) begin
            case (current_state)
                S_NS_GREEN:   next_state = S_NS_YELLOW;
                S_NS_YELLOW:  next_state = S_EW_GREEN;
                S_EW_GREEN:   next_state = S_EW_YELLOW;
                S_EW_YELLOW:  next_state = S_NS_GREEN;
                default:      next_state = S_NS_GREEN;
            endcase
        end
    end

    // ==============================
    // OUTPUT LOGIC (MOORE)
    // ==============================
    always_comb begin
        NS_red    = 0;
        NS_yellow = 0;
        NS_green  = 0;
        EW_red    = 0;
        EW_yellow = 0;
        EW_green  = 0;

        case (current_state)
            S_NS_GREEN: begin
                NS_green = 1;
                EW_red   = 1;
            end

            S_NS_YELLOW: begin
                NS_yellow = 1;
                EW_red    = 1;
            end

            S_EW_GREEN: begin
                EW_green = 1;
                NS_red   = 1;
            end

            S_EW_YELLOW: begin
                EW_yellow = 1;
                NS_red    = 1;
            end
        endcase
    end

endmodule
