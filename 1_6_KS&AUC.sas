/*===============================================================
  1_6_KS&AUC.sas — Evaluate KS and AUC
===============================================================*/
proc logistic inmodel=work.pd_model;
  score data=work.test_fe out=work.test_scored_fitstat fitstat;
run;

%let probvar=P_1;

proc npar1way data=work.test_scored edf;
  class target_12m;
  var &probvar.;
run;
