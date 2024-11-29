from icecream import ic, install

install()
ic.configureOutput(prefix=f'DEBUG:|', includeContext=True)

def make_ice_cream(topping):
    ic(topping)
    ic(f"Making ice cream with {topping}...")
    return "Ice cream with " + topping + " is ready!"

def obj_read():
    from Utils.Excelize import ReadExcel
    result = ReadExcel('../ExcelFiles/SearchWords_v3.xlsx').read_data_obj()
    return ic(result)

if __name__ == '__main__':
    # make_ice_cream("chocolate")
    res = obj_read()
    ic(type(res))
