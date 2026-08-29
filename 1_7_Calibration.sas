/*===============================================================
  1_7_Calibration.sas — Decile-Based PD Calibration (Simple)
  ------------------------------------------------------------
  Purpose: Compare predicted PDs vs. actual default rates
  ------------------------------------------------------------
===============================================================*/

ods graphics on;

/* 1) Define the predicted probability variable (from SCORE step) */
%let probvar = P_1;

/* 2) Confirm input datasets exist */
proc contents data=work.train_scored out=_check_train(keep=name) noprint;
run;

proc contents data=work.test_scored out=_check_test(keep=name) noprint;
run;

/* 3) Build decile buckets on TRAIN data */
proc rank data=work.train_scored groups=10 out=work.train_bins;
    var &probvar.;
    ranks decile;
run;

/* 4) Calculate observed (actual) and predicted default rates per decile */
proc sql;
    create table work.cal_map as
    select decile,
           mean(target_12m) as obs_rate format=percent8.2,
           mean(&probvar.)  as pred_rate format=percent8.2
    from work.train_bins
    group by decile;
quit;

/* 5) Apply the calibration map to TEST data */
proc rank data=work.test_scored groups=10 out=work.test_bins;
    var &probvar.;
    ranks decile;
run;

proc sql;
    create table work.test_calibrated as
    select a.*, b.obs_rate as p_cal
    from work.test_bins as a
    left join work.cal_map  as b
      on a.decile = b.decile;
quit;

/* 6) Compare predicted vs. calibrated vs. actual PD */
proc means data=work.test_calibrated mean;
    var target_12m &probvar. p_cal;
run;

/* 7) Optional: visualize calibration curve */
proc sgplot data=work.cal_map;
    series x=decile y=obs_rate / markers lineattrs=(pattern=solid);
    series x=decile y=pred_rate / markers lineattrs=(pattern=dash);
    xaxis label="PD Decile (1=Lowest Risk → 10=Highest)";
    yaxis label="Default Rate / PD";
    title "Calibration Curve — Observed vs Predicted PD";
run;

ods graphics off;
