class GlobalVarBean:
    pass

    @staticmethod
    def setValue(key, value):
        setattr(GlobalVarBean, key, value)

    @staticmethod
    def getValue(key):
        output = getattr(GlobalVarBean, key)
        print(output)
        return output


GlobalVarBean.setValue('addr', '127.0.0.1:21513')

if __name__ == '__main__':
    globalVar = GlobalVarBean()
    globalVar.setValue('addr', '127.0.0.1:21513')
    globalVar.getValue('addr')
    globalVar.setValue('apk_name', 'esunny')
    globalVar.getValue('apk_name')
