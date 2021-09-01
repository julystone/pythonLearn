from self_ad import GlobalVarBean

if __name__ == '__main__':
    GlobalVarBean.setValue('123', 123456)
    GlobalVarBean.getValue('123')
    GlobalVarBean.getValue('addr')
