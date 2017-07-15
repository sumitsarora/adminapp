class Level:
    __level1=None
    __level2=None
    __level3=None
    __level4=None
    __level5=None
    __ptitle=None
    __pimg=None
    __pprice=None
    __pdesc=None

    def __init__(self,level1,level2,level3,level4,level5,ptitle,pimg,pprice,pdesc):
        self.__level1=level1
        self.__level2=level2
        self.__level3=level3
        self.__level4=level4
        self.__level5=level5
        self.__ptitle=ptitle
        self.__pimg=pimg
        self.__pprice=pprice
        self.__pdesc=pdesc

    def set_level1(self,level1):
        self.__level1=level1

    def get_level1(self):
        return self.__level1

    def set_level2(self,level2):
        self.__level2=level2

    def get_level2(self):
        return self.__level2

    def set_level3(self,level3):
        self.__level3=level3

    def get_level3(self):
        return self.__level3

    def set_level4(self,level4):
        self.__level4=level4

    def get_level4(self):
        return self.__level4

    def set_level5(self,level5):
        self.__level5=level5

    def get_level5(self):
        return self.__level5

    def set_ptitle(self,ptitle):
        self.__ptitle=ptitle

    def get_ptitle(self):
        return self.__ptitle

    def set_pimg(self,pimg):
        self.__pimg=pimg

    def get_pimg(self):
        return self.__pimg

    def set_pprice(self,pprice):
        self.__pprice=pprice

    def get_pprice(self):
        return self.__pprice

    def set_pdesc(self,pdesc):
        self.__pdesc=pdesc

    def get_pdesc(self):
        return self.__pdesc

    def toString(self):
        return "{} {} {} {} {} {} {} {} {}".format(self.__level1,self.__level2,self.__level3,self.__level4,self.__level5,self.__ptitle,self.__pimg,self.__pprice,self.__pdesc)
