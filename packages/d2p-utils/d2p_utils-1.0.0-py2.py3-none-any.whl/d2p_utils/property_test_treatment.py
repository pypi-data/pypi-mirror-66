

class Type1(object):
    def __init__(self, **argsv):
        self.conf_fl_nm = argsv['conf_fl_nm']
        self.src = argsv['src_tbl_nm']
        print self.src
        print self.conf_fl_nm
        self._spark ='sparkSession'
        print self
        print ("In Super class Type1")

    @property
    def my_spark(self):
        return self._spark
    @property
    def source_df(self):
        return self.src

    @source_df.setter
    def source_df(self,src):
        self.src = src

    def test_default(self, num_part=20):
        return num_part

    def get_val(self):
        return self.src

class Treatment(Type1):
    def __init__(self, **argsv):
        super(Type1,self).__init__(**argsv)
        # print a
        # print self
        print ("In base class Treatment")

