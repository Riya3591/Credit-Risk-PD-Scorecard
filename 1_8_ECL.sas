/*===============================================================
  1_8_ECL.sas — Simple 12-Month Expected Credit Loss (ECL)
  ------------------------------------------------------------
  Purpose:
    - Compute ECL = PD × LGD × EAD
    - Use calibrated PDs from the previous step
===============================================================*/

ods graphics on;

/* Step 1 — Build ECL dataset */
data work.ecl_input;
    set work.test_calibrated;

    /* Exposure at Default (EAD) */
    EAD = 10000;

    /* Loss Given Default (LGD) */
    LGD = 0.35;

    /* 12-Month PD: prefer calibrated PD, else use model PD */
    PD_12m = coalesce(p_cal, P_1);

    /* Expected Credit Loss calculation */
    ECL_12m = EAD * LGD * PD_12m;
run;

/* Step 2 — Summarize portfolio-level results */
title "Portfolio-level ECL Summary";
proc means data=work.ecl_input sum mean;
    var EAD PD_12m ECL_12m;
run;

/* Step 3 — View sample rows */
title "Sample of Calculated ECLs";
proc print data=work.ecl_input(obs=10);
    var EAD LGD PD_12m ECL_12m;
run;

title;
ods graphics off;
