/*===============================================================
  1_1_LoadData.sas — Load and Prepare the Dataset
===============================================================*/
options mprint mlogic symbolgen nodate nonumber;
ods graphics on;

%let file_path=/home/u49308301/UDEMY_LESSONS/Lession1/Module1/ifrs9_pit_pd_intro.csv;

proc import datafile="&file_path."
    out=work.pd_data
    dbms=csv replace;
    guessingrows=max;
run;

/* Basic clean-up — remove impossible dates and normalise variables */
data work.pd_data;
  set work.pd_data;

  if loan_origination_date > report_date then delete;

  loan_age_m=intck('month',loan_origination_date,report_date,'c');

  credit_utilization=max(0,min(credit_utilization,1));
  if missing(default_flag) then default_flag=0;
  default_flag=(default_flag>0);

  if missing(region) then region="Unknown";
  if missing(employment_status) then employment_status="NA";
  if missing(marital_status) then marital_status="NA";
  if missing(dependents) then dependents=0;
run;

proc contents data=work.pd_data order=varnum; run;
proc print data=work.pd_data(obs=5); run;
