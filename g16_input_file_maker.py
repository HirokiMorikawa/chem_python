# coding:utf-8

import argparse
import os
import sys
from pprint import pprint

# from rdkit import rdBase
# from rdkit import Chem
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from multiprocessing import cpu_count


class Gaussian_Input:
    def __init__(self):
        self._chk_path = ""
        self._molecule_name = ""
        self._calc_function = ""
        self._xyz = ""

    def set_chk_path(self, chk_path):
        self._chk_path = chk_path

    def set_molecule_name(self, name):
        self._molecule_name = name

    def set_calc_function(self, function):
        self._calc_function = function

    def set_input_coordinates(self, xyz):
        self._xyz = xyz

    def _make_struct(self):
        return None

    def make_input(self):
        section = self._make_struct()
        struct = "{}\n{}\n\n{}\n\n{}\n\n"
        return struct.format(
            section.link0(),
            section.root(), 
            section.title(), 
            section.molcule(self._xyz))


class Opt_Input(Gaussian_Input):
    def _make_struct(self):
        return Opt_Section(self._molecule_name, self._calc_function, self._chk_path)


class Td_Input(Gaussian_Input):
    def _make_struct(self):
        return Td_Section(self._molecule_name, self._calc_function, self._chk_path)


class Section:
    def __init__(self, molecule_name, calc_function, chk_path):
        thread = int(max(1, cpu_count() * 0.8))
        self._memory = "4GB"
        self._cpu = "0-{}".format(thread)
        self._checkpoint = "{}{}.chk".format(chk_path, molecule_name)
        self._molecule_name = molecule_name
        self._calc_function = calc_function

    def link0(self):
        mem = "%mem={}".format(self._memory)
        cpu = ("%" + "cpu={}").format(self._cpu)
        chk = ("%" + "chk={}").format(self._checkpoint)
        ret = "{}\n{}\n{}"
        return ret.format(mem, cpu, chk)

    def root(self):
        pass

    def title(self):
        return self._molecule_name

    def molcule(self, xyz):
        ret = "0 1\n{}"
        return ret.format(xyz)


class Opt_Section(Section):
    def __init__(self, molecule_name, calc_function, chk_path):
        super().__init__(molecule_name, calc_function, chk_path)

    def root(self):
        return "#p opt {} pop=full".format(self._calc_function)


class Td_Section(Section):
    def __init__(self, molecule_name, calc_function, chk_path):
        super().__init__(molecule_name, calc_function, chk_path)

    def root(self):
        return "#p td {} pop=full".format(self._calc_function)


class PathParser(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parsed = None
        # parsed = parseof("seed", parser, values)
        if ".smiles" in values:
            parsed = values.rstrip(".smiles").split("/")[-1]
        elif ".xyz" in values:
            parsed = values.rstrip(".xyz").split("/")[-1]

        setattr(namespace, self.dest, [values, parsed])


def mkdir(out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", action=PathParser, required=True)
    parser.add_argument("-desc", default="Gaussian/input")
    parser.add_argument("-calc_type", choices=['opt', 'td'], required=True)
    parser.add_argument("-calc_func", required=True)
    return parser


def file_load(file_path):
    with open(file_path) as f:
        return f.read()


def file_load_line(file_path):
    with open(file_path) as f:
        return f.readlines()


def file_save(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)


def create_mol(file_path):
    smiles = file_load(file_path)
    return Chem.MolFromSmiles(smiles)

def load_mol(file_path):
    mol = file_load_line(file_path)
    mol = mol[2:]
    ret = ""
    for _mol in mol:
        ret += _mol
    return ret


def opt_xyz(mol):
    mol = AllChem.AddHs(mol)
    # 大きいMoluculesは3d構造を生成できず-1を返しComformerを生成できない
    # useRandomCoords=Trueにすることでより効果的になる
    # 参考キーワード[Bad Conformer Id]
    AllChem.EmbedMolecule(mol, useRandomCoords=True)
    AllChem.MMFFOptimizeMolecule(mol)
    
    xyz = ""

    conf = mol.GetConformer(0)
    for n, (x, y, z) in enumerate(conf.GetPositions()):
        atom = mol.GetAtomWithIdx(n)
        xyz += "{}\t {: .8f} {: .8f} {: .8f}\n".format(
            atom.GetSymbol(), x, y, z)

    print(xyz)

    # return xyz
    return xyz


if __name__ == "__main__":
    args = parse().parse_args()
    file_path, name = args.source
    desc = args.desc
    calculate_type = args.calc_type
    calculate_function = args.calc_func

    mkdir(desc)

    gaussian_input_maker = None
    if calculate_type == "opt":
        mol = create_mol(file_path)
        initial_xyz = opt_xyz(mol)
        gaussian_input_maker = Opt_Input()
        name = name + "_GS"
    elif calculate_type == "td":
        initial_xyz = load_mol(file_path)
        gaussian_input_maker = Td_Input()
        name = name + "_ExS"
    else:
        pass

    gaussian_input_maker.set_chk_path(desc.rstrip("input") if "input" in desc else desc)
    gaussian_input_maker.set_molecule_name(name)
    gaussian_input_maker.set_calc_function(calculate_function)
    gaussian_input_maker.set_input_coordinates(initial_xyz)

    input_file = gaussian_input_maker.make_input()

    print(input_file)

    file_save(desc + "/" + name + ".com", input_file)
