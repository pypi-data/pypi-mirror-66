import json, argparse
from property_test_treatment import Type1, Treatment



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="input of arguments from airflow dag")
    parser.add_argument('-dag_run_dt_tm','--dag_run_dt_tm',help= "dag_run_dt_tm=date and time of the DAG run, not to be confused with the actual run time")
    parser.add_argument('-src_tbl_nm', '--src_tbl_nm', default='')
    parser.add_argument('-conf_fl_nm', '--conf_fl_nm', default='')
    argsv = vars(parser.parse_args())
    type1 = Type1(**argsv)
    print argsv
    print(type1.source_df)
    print(type(type1.source_df))
    type1.source_df='fact_new_tbl'
    print(type1.source_df)
    print(type(type1.source_df))
    print (type1.my_spark)
    print(type1.test_default(30))

    # subclass test
    treat = Treatment()
    x= treat.test_default()
    # x= treat.get_val()

    # print x
    # print treat
    # print(help(x))
