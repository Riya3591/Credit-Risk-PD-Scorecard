/*===============================================================
  1_2_DQ.sas — Data-Quality Checks and 12-Month Target Creation
===============================================================*/
data work.pd_dq;
  set work.pd_data;

  /* Remove rows where default occurred before the report date */
  if not missing(default_date) and default_date <= report_date then delete;

  /* Bound key variables */
  dpd=max(0,dpd);
  credit_utilization=max(0,min(credit_utilization,1));

  /* Forward-looking target */
  length target_12m 8;
  target_12m=0;
  if not missing(default_date) then do;
     if intck('month',report_date,default_date,'c')<=12 then target_12m=1;
  end;
run;

proc freq data=work.pd_dq; tables target_12m; run;
proc means data=work.pd_dq n nmiss; run;
