import glob
from pprint import pprint

import numpy as np
import pandas as pd
from rdkit import Chem

from module_mixer import ExecGaussian16, ModuleMixer, function1, function2, function3

mixer = ModuleMixer()


def module_list():
    for module in mixer.module_id:
        yield module


def mix_module(target) -> dict:
    pairs = mixer.get_target_module_id_pair2(target)
    compounds = {}
    err = {}
    for m in pairs:
        act_pair = mixer.get_actual_pair(m[0], m[1])
        name, smiles = mixer.convert_smiles_specify_label(m[0], m[1], act_pair[0][0], act_pair[0][1])
        if smiles is None:
            err[name] = smiles
            continue
        compounds[name] = smiles
    return compounds


def mix_module_all_pair(left, right):
    act_pair = mixer.get_actual_pair(left, right)
    compounds = {}
    err = {}
    for left_pair, right_pair in act_pair:
        name, smiles = mixer.convert_smiles_specify_label(left, right, left_pair, right_pair)
        if smiles is None:
            err[name] = smiles
            continue
        compounds[name] = smiles
    return compounds


def smiles_to_mol(compounds) -> list:
    return [Chem.MolFromSmiles(compounds[key]) for key in compounds.keys()]


def module_adopt(compounds) -> dict:
    result_dict = {}
    for key in compounds.keys():
        print("{}".format(key))
        g16 = ExecGaussian16("smiles", "individual", compounds[key])
        ret = g16.run(key, function1, function2, function3)
        if not isinstance(ret, np.ndarray):
            if ret == 0:
                continue
        result_dict[key] = ret
        np.savetxt("{}/{}.csv".format("result/org", key), ret, delimiter=",")
    return result_dict


def result_to_pandas(result_dict) -> pd.DataFrame:
    df_index = ["function1", "function2", "function3"]
    df = pd.DataFrame(result_dict, index=df_index)
    return df


def collect_all() -> pd.DataFrame:
    module_list = glob.glob("result/col/*.csv")
    df1 = pd.read_csv(module_list.pop(0), index_col=0)
    for module in module_list:
        df2 = pd.read_csv(module, index_col=0)
        df1 = pd.concat([df1, df2], axis=1)
    df1 = df1.T.sort_index()
    df1 = df1[~df1.duplicated()]
    # print(df1
    return df1


def calc_local_max(data):
    """
    局所的最大値を取得する
    :param data:
    :return:
    """
    if isinstance(data, pd.Series):
        ret = pd.Series()
        for i in range(data.shape[0] - 2):
            if data[i] <= data[i + 1] and data[i + 1] > data[i + 2]:
                # ret.append(data[i + 1])
                ret[data.index[i + 1]] = data[i + 1]
    else:
        ret = []
        for i in range(data.shape[0] - 2):
            if data[i] <= data[i + 1] and data[i + 1] > data[i + 2]:
                ret.append(data[i + 1])
        ret = np.array(ret)
    # return np.array(ret)
    return ret


def frequency_module(data) -> pd.DataFrame:
    """


    :param data:
    :return:
    """
    compound_list = data
    if isinstance(compound_list, pd.DataFrame) or isinstance(compound_list, pd.Series):
        compound_list = compound_list.index.to_list()
    elif isinstance(compound_list, pd.Index):
        compound_list = compound_list.to_list()

    compound_list = [mol.split("_")[0] for mol in compound_list]
    left = []
    right = []
    for mol in compound_list:
        for mod in module_list():
            if mol.startswith(mod):
                left.append(mod)
            if mol.endswith(mod):
                right.append(mod)
            else:
                continue

    df = pd.DataFrame({"left": left, "right": right})
    freq_mol_appear: pd.DataFrame = df.apply(lambda x: x.value_counts())
    return freq_mol_appear


def save_data(df, filename):
    df.to_csv(filename)


if __name__ == "__main__":
    df = collect_all()
    # print(df[df > 150]["func2"].dropna().to_dict())

    # df["func2"].to_csv("a.csv")
    c = calc_local_max(df["func2"])
    c.name = "func2"
    # c.to_csv("b.csv")
    c = frequency_module(c)
    c = c.idxmax()
    left = c["left"]
    right = c["right"]

    pprint(mix_module_all_pair(left, right))
    pprint(mix_module_all_pair(right, left))
