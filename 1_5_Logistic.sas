/*===============================================================
  1_5_Logistic.sas — Train 12-Month PD Logistic Model
===============================================================*/
ods graphics on;

proc logistic data=work.train_fe outmodel=work.pd_model plots(only)=roc;
   class dpd_30plus(ref='0') age_6m(ref='0') age_6_24(ref='0') age_24p(ref='0') / param=ref;
   model target_12m(event='1') =
         score_rev util_log dpd_clip dpd_30plus
         age2 age_6m age_6_24 age_24p
         macro_gdp_growth macro_unemployment macro_interest_rate
         / lackfit rsq;

   /* Score ALL splits so downstream code always has inputs */
   score data=work.train_fe out=work.train_scored;   /* <-- add this */
   score data=work.valid_fe out=work.valid_scored;
   score data=work.test_fe  out=work.test_scored;
run;

ods graphics off;
