import sys
from sys import argv
from rdkit import rdBase
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import numpy as np

# dir="./化合物/"
#name = "FBR_Fluorene.smiles"

base_outdir = "./生成データ/"

if len(argv) < 2:
    print("引数が足りません")
    sys.exit(1)


name = argv[1]

smiles = None
with open(name) as f:
    smiles = f.read()

name = name.rstrip(".smiles").split("/")[-1]

mol = Chem.MolFromSmiles(smiles)
# Draw.MolToImage(mol, includeAtomNumbers=True).save("test.png")
Draw.MolToImage(mol, includeAtomNumbers=True).save(base_outdir + name + ".png")

print("原子の表示")

for atom in mol.GetAtoms():
    print(atom.GetIdx(), ":", atom.GetSymbol())

print("分子結合の表示")

for bond in mol.GetBonds():
    print(bond.GetBeginAtomIdx(), "-", bond.GetEndAtomIdx())

print("水素の電荷の計算")

AllChem.ComputeGasteigerCharges(mol)

hydro_bounds_atom = []

for atom in mol.GetAtoms():
    # print(atom.GetIdx(), ":", atom.GetSymbol(), end="")
    # print("-> 水素原子の電荷", atom.GetProp('_GasteigerHCharge'))
    hcharge = float(atom.GetProp('_GasteigerHCharge'))
    if hcharge > 0:
        hydro_bounds_atom.append(atom)

string_hydro_bounds_atom = ""

for i, atom in enumerate(hydro_bounds_atom):
    string_hydro_bounds_atom += str(atom.GetIdx())
    print(atom.GetIdx(), end="")
    if i + 1 != len(hydro_bounds_atom):
        string_hydro_bounds_atom += ":"
        print(end=":")
    else:
        print()

with open(base_outdir + name + ".txt", "w") as f:
    f.write(string_hydro_bounds_atom)