import gc
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import category_encoders as ce
import joblib


def reduce_mem_usage(df, verbose=False):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                c_prec = df[col].apply(lambda x: np.finfo(x).precision).max()
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max and c_prec == np.finfo(
                        np.float16).precision:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max and c_prec == np.finfo(
                        np.float32).precision:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (
            start_mem - end_mem) / start_mem))
    return df


def mean_woe_target_encoder(train, test, target, col, n_splits=10):
    folds = StratifiedKFold(n_splits)

    y_oof = np.zeros(train.shape[0])
    y_test_oof = np.zeros(test.shape[0]).reshape(-1, 1)

    splits = folds.split(train, target)

    for fold_n, (train_index, valid_index) in enumerate(splits):
        X_train, X_valid = train[col].iloc[train_index], train[col].iloc[valid_index]
        y_train, y_valid = target.iloc[train_index], target.iloc[valid_index]
        clf = ce.target_encoder.TargetEncoder()

        clf.fit(X_train.values, y_train.values)
        y_pred_valid = clf.transform(X_valid.values)

        y_oof[valid_index] = y_pred_valid.values.reshape(1, -1)

        tp = (clf.transform(test[col].values) / (n_splits * 1.0)).values
        tp = tp.reshape(-1, 1)
        y_test_oof += tp

        del X_train, X_valid, y_train, y_valid
        gc.collect()
    return y_oof, y_test_oof


def getGoalMid(masterGoal, guestGoal, masterMidGoal, guestMidGoal):
    return int(masterGoal) + int(guestGoal) - int(masterMidGoal) - int(guestMidGoal)


def removeSub(pankou):
    pankou = pankou.replace("升", "")
    pankou = pankou.replace("降", "")
    return pankou.strip()


def getType(yapanMasterStartOdd, yapanGuestStartOdd, yapanPankouStart):
    linTypeStart = get18(yapanMasterStartOdd, yapanGuestStartOdd)
    return str(linTypeStart) + "_" + str(yapanPankouStart)


def get18(master, guest):
    if master > guest:
        return 18
    if master < guest:
        return 81
    if master == guest:
        return 99


def daxiao_num(x):
    x_list = x.split("/")
    num = 0
    for i in x_list:
        num += float(i)
    return (float(num) / len(x_list))


def realDaxiao(x, master, guest):
    return float(x) - int(master) - int(guest)


def shengjiang(start, end):
    return ((end) - (start))


def round2(x):
    return round((x), 2)


def getShuiPing(x):
    result = 11
    if x < 0.75:
        result = 0
    if 0.75 <= x and x <= 0.85:
        result = 1
    if 0.85 < x and x <= 0.90:
        result = 2
    if 0.90 < x and x <= 0.95:
        result = 3
    if 0.95 < x and x <= 1.00:
        result = 4
    if 1.00 < x and x <= 1.08:
        result = 5
    if 1.08 < x:
        result = 6
    return result


def num_fea_dis(df, features):
    for f in features:
        nm = f + '_' + 'shuiPing'
        df[nm] = df[f].map(getShuiPing)
    return df


def getLastTime(x):
    if x > 49 and x < 60:
        return 0
    if x >= 60 and x <= 70:
        return 1
    return 2


def getResult65(zhong, last):
    sum1 = 0
    for i in zhong.split('-'):
        sum1 += int(i)
    sum2 = 0
    for i in last.split('-'):
        sum2 += int(i)
    return sum2 - sum1


def getResultNew(x):
    if x >= 1:
        return 1
    return 0

def realDaxiao75(x, last):
    master = last.split("-")[0]
    guest = last.split("-")[1]
    return float(x) - float(master) - float(guest)

def daxiao_num_bifeng(x):
    x_list = x.split("-")
    num = 0
    for i in x_list:
        num += float(i)
    return (float(num)/len(x_list))

class Processor:
    def __init__(self):
        projectPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.data1 = pd.read_csv(projectPath + r'\predict\train_5.txt')
        self.modelPath = projectPath + '\\model\\'

    @staticmethod
    def preF(test):

        test['zhongbifengNew'] = test['midMasterGoal'].astype(
            str) + "-" + test['midGuestGoal'].astype(str)

        test['allbifeng'] = test['lastBifeng'].astype(
            str) + "-" + test['zhongbifengNew'].astype(str)

        pankou = ["pankouOdd_End_Zhong_3", "pankou_Start_Zhong_3"] + ["pankou_Start_Ji_3", "pankouOdd_End_Ji_3"]

        for col in pankou:
            test[col] = test[col].astype(str)
            test[col] = test[col].map(daxiao_num)
            #         test[col+"daxiao"] = test[col]
            test[col] = test[col].astype(str)
            nm = col + "Real"
            test[nm] = test.apply(lambda x: realDaxiao(x[col], x['midGuestGoal'], x['midMasterGoal']), axis=1)
            test[nm] = test[nm].astype(str)

        test['allbifengNew'] = test['allbifeng'].astype(
            str) + "-" + test['pankouOdd_End_Zhong_3Real'].astype(str) + "-" + test['pankouOdd_End_Ji_3'].astype(str)

        fes = ['masterOdd_Start_Ji_3', 'masterOdd_End_Ji_3',
               'masterOdd_Start_Zhong_3', 'masterOdd_End_Zhong_3'] + ['guestOdd_Start_Ji_3', 'guestOdd_End_Ji_3',
                                                                      'guestOdd_Start_Zhong_3', 'guestOdd_End_Zhong_3']

        num_fea_dis(test, fes)

        test['daxiaoTypeStart'] = test.apply(
            lambda x: getType(x['masterOdd_Start_Ji_3'], x['guestOdd_Start_Ji_3'], x['pankou_Start_Ji_3']), axis=1)
        test['daxiaoType'] = test.apply(
            lambda x: getType(x['masterOdd_End_Ji_3'], x['guestOdd_End_Ji_3'], x['pankouOdd_End_Ji_3']), axis=1)
        test['daxiaoTypeStartMid'] = test.apply(
            lambda x: getType(x['masterOdd_Start_Zhong_3'], x['guestOdd_Start_Zhong_3'], x['pankou_Start_Zhong_3Real']),
            axis=1)
        test['daxiaoTypeMid'] = test.apply(
            lambda x: getType(x['masterOdd_End_Zhong_3'], x['guestOdd_End_Zhong_3'], x['pankouOdd_End_Zhong_3Real']),
            axis=1)

        test['daxiaoTypeStart'] = test['masterOdd_Start_Ji_3_shuiPing'].astype(str) + test['daxiaoTypeStart']
        test['daxiaoType'] = test['masterOdd_End_Ji_3_shuiPing'].astype(str) + test['daxiaoType']

        test['daxiaoTypeStartMid'] = test['masterOdd_Start_Zhong_3_shuiPing'].astype(str) + test['daxiaoTypeStartMid']
        test['daxiaoTypeMid'] = test['masterOdd_End_Zhong_3_shuiPing'].astype(str) + test['daxiaoTypeMid']

        test['daxiaoTypeALL'] = test['daxiaoTypeStart'] + test['daxiaoType']
        test['daxiaoTypeMidALL'] = test['daxiaoTypeStartMid'] + test['daxiaoTypeMid'] + test['zhongbifengNew']

        test['daxiaoPankou'] = test['pankou_Start_Ji_3'] + test['pankouOdd_End_Ji_3']
        test['daxiaoPankouMid'] = test['pankou_Start_Zhong_3Real'] + test['pankouOdd_End_Zhong_3Real']
        test['daxiaoPankouALL'] = test['daxiaoPankou'] + test['daxiaoPankouMid'] + test['zhongbifengNew']

        test['MasterOddFlowPankou'] = test["pankouOdd_End_Ji_3"].astype(float) - test["pankou_Start_Ji_3"].astype(float)
        test['MasterOddFlowPankouMid'] = test["pankou_Start_Zhong_3"].astype(float) - test[
            "pankouOdd_End_Zhong_3"].astype(float)
        test['MasterOddFlow'] = test["masterOdd_Start_Ji_3"] - test["masterOdd_End_Ji_3"]

        test['daxiaoTypeStartMidLast'] = test['daxiaoTypeStartMid'] + test['lastBifeng'].astype(str)
        test['daxiaoTypeMidLast'] = test['daxiaoTypeMid'] + test['lastBifeng'].astype(str)
        test['daxiaoTypeStartLast'] = test['daxiaoTypeStart'] + test['lastBifeng'].astype(str)
        test['daxiaoTypeLast'] = test['daxiaoType'] + test['lastBifeng'].astype(str)
        test['daxiaoPankouLast'] = test['pankou_Start_Ji_3'] + test['pankouOdd_End_Ji_3'] + test['lastBifeng'].astype(
            str)
        test['daxiaoPankouMidLast'] = test['pankou_Start_Zhong_3Real'] + test['pankouOdd_End_Zhong_3Real'] + test[
            'lastBifeng'].astype(str)
        test['daxiaoPankouALLLast'] = test['daxiaoPankou'] + test['daxiaoPankouMid'] + test['zhongbifengNew'] + test[
            'lastBifeng'].astype(str)

        #     test = test.drop(['masterOdd_Start_Ji_3_shuiPing', 'masterOdd_End_Ji_3_shuiPing',
        #                       'masterOdd_Start_Zhong_3_shuiPing','masterOdd_End_Zhong_3_shuiPing'], axis=1)

        #     test = test.drop(['guestOdd_Start_Ji_3_shuiPing', 'guestOdd_End_Ji_3_shuiPing',
        #                       'guestOdd_Start_Zhong_3_shuiPing','guestOdd_End_Zhong_3_shuiPing'], axis=1)

        test = test.drop(columns=['midGuestGoal', 'midMasterGoal'])
        test = test.drop(columns=['time'])

        test["lastTime"] = test["lastTime"].astype(int)
        test["lastTime75"] = test["lastTime75"].astype(int)
        test["lastTime130"] = test["lastTime130"].astype(int)

        test["lastTimeSub"] = test["lastTime75"] - test["lastTime"]
        test["lastTimeSub130"] = test["lastTime130"] - test["lastTime75"]

        test['lastBifengNum'] = test['lastBifeng'].map(daxiao_num_bifeng)
        test['lastBifeng130Num'] = test['lastBifeng130'].map(daxiao_num_bifeng)

        test = test[test['lastBifengNum'] <= test['lastBifeng130Num']]

        test = test[test['masterOdd_End_Ji_3'] <= 1.30]
        test = test[test['masterOdd_End_Zhong_3'] <= 1.30]
        test = test[test['masterOdd_End_60_3'] <= 1.30]
        test = test[test['masterOdd_End_752_3'] <= 1.30]
        test = test[test['masterOdd_End_75_3'] <= 1.30]
        test = test[test['masterOdd_End_130_3'] <= 1.30]
        return test

    @staticmethod
    def realDaxiao75(x, last):
        master = last.split("-")[0]
        guest = last.split("-")[1]
        return float(x) - float(master) - float(guest)

    @staticmethod
    def pref65(test, time):
        pankou = ["pankouOdd_End_" + time + "_3"]

        for col in pankou:
            test[col] = test[col].astype(str)
            test[col] = test[col].map(daxiao_num)
            test[col + "daxiao"] = test[col]
            test[col] = test[col].astype(str)

        fes = ['masterOdd_End_' + time + "_3", 'guestOdd_End_' + time + "_3"]

        num_fea_dis(test, fes)

        test['daxiaoType' + time] = test.apply(
            lambda x: getType(x['masterOdd_End_' + time + "_3"], x['guestOdd_End_' + time + "_3"],
                              x['pankouOdd_End_' + time + "_3"]), axis=1)
        test['daxiaoType' + time] = test['masterOdd_End_' + time + "_3_shuiPing"].astype(str) + test[
            'daxiaoType' + time]
        test["pankouOdd_End_" + time + "_real2"] = test.apply(
            lambda x: realDaxiao75(x['pankouOdd_End_' + time + "_3"], x['lastBifeng' + time]), axis=1)

        #     test["daxiaoType"+time+"odd"] = test['lastBifeng'+time] + test['masterOdd_End_'+time+"_3"].astype(str) + test["pankouOdd_End_"+time+"_real2"].astype(str) + test['guestOdd_End_'+time+"_3"].astype(str)

        test = test.drop(['masterOdd_End_' + time + "_3_shuiPing", 'guestOdd_End_' + time + "_3_shuiPing"], axis=1)

        return test

    def getPerOneDaxiao(self, dictDa):
        train = self.data1.copy(deep=True)
        train = train.drop(['Unnamed: 0'], axis=1)

        test_x = pd.DataFrame(dictDa)
        test_x = test_x.dropna()
        test_x = reduce_mem_usage(test_x)
        test_x = test_x[test_x["lastTime"] != "中场"]
        test_x = self.preF(test_x)
        for time in ["60"]:
            test_x =  self.pref65(test_x, time)
        test_x_o = test_x.copy(deep=True)
        test_x = test_x.drop(
            ['place','lastBifengNow'], axis=1)
        test_x.head()

        cat_features = test_x.select_dtypes(include='object').columns
        num_columns = [col for col in test_x.columns if test_x[col].dtype != 'object']

        train_x = train.drop(columns=['result'])
        train_y = train['result']

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        train_x[num_columns] = sc.fit_transform(train_x[num_columns])
        test_x[num_columns] = sc.transform(test_x[num_columns])
        print(train_x.shape)
        print(test_x.shape)

        for col in cat_features:
            train_x[col] = train_x[col].astype(str)
            test_x[col] = test_x[col].astype(str)
            y_oof, y_test_oof = mean_woe_target_encoder(train_x, test_x, train_y, col, n_splits=10)
            train_x[col] = y_oof
            test_x[col] = y_test_oof

        y_preds = np.zeros(test_x.shape[0])
        for fold_n in range(0, 5):
            model = self.modelPath + "gbm_2" + str(fold_n) + "_singe" + ".txt"
            clf = joblib.load(model)
            y_preds += clf.predict(test_x) / 5
        test_x_o["per"] = y_preds
        del train
        return test_x_o

Processor()