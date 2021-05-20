import json

import uiautomator2 as u2


def dict_diff(d1, d2):
    diff_keys = d1.keys() & d2
    diff_values = [{k: [d1[k], d2[k]]} for k in diff_keys if d1[k] != d2[k]]
    res = json.dumps(diff_values, sort_keys=True, indent=4, ensure_ascii=True)
    print(res)
    return res


if __name__ == '__main__':
    d = u2.connect()
    elem1 = d(resourceId="esunny.test:id/es_login_activity_login_itv_save_account")
    elem2 = d(resourceId="esunny.test:id/es_login_activity_login_etv_save_pwd")
    dict1 = elem1.info
    dict2 = elem2.info
    dict_diff(dict1, dict2)
