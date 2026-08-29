/*===============================================================
  1_3_DataSplit.sas — Time-Based Train/Validation/Test Split
===============================================================*/
%let train_end='31DEC2023'd;
%let valid_end='30JUN2024'd;

proc sort data=work.pd_dq out=work.pd_sorted; by report_date; run;

data work.train work.valid work.test;
  set work.pd_sorted;
  if report_date<=&train_end. then output work.train;
  else if report_date<=&valid_end. then output work.valid;
  else output work.test;
run;

proc freq data=work.train; tables target_12m; run;
proc freq data=work.valid; tables target_12m; run;
