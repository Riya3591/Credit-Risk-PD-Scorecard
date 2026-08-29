/*===============================================================
  1_4_FeatureEng.sas — Feature Engineering (Transparent)
===============================================================*/
%macro mkfe(in=,out=);
data &out.;
  set &in.;

  score_rev=900-internal_score;
  util_log=log(1+credit_utilization);
  dpd_clip=min(dpd,90);
  dpd_30plus=(dpd>=30);
  age2=age**2;

  /* Loan-seasoning buckets for vintage effect */
  age_6m  =(loan_age_m<6);
  age_6_24=(6<=loan_age_m<24);
  age_24p =(loan_age_m>=24);
run;
%mend;

%mkfe(in=work.train,out=work.train_fe);
%mkfe(in=work.valid,out=work.valid_fe);
%mkfe(in=work.test ,out=work.test_fe );
