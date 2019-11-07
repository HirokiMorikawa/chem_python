import os
from pprint import pprint
from sys import argv

import rdkit
from rdkit import RDConfig
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw

def mkdir(out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

def file_load(file_path):
    with open(file_path) as f:
        return f.read()

def create_mol(file_path):
    """
    """
    smiles = file_load(file_path)
    return Chem.MolFromSmiles(smiles)

def saveImageFromMol(filename, mol):
    print("smilesから2d分子画像を生成・保存します->{}".format(filename))
    Draw.MolToImage(mol).save(filename + ".png")

def getFunctionFrom(descriptors):
    """
    Descriptorsから必要な関数のリストを取り出す関数
    """
    pointer = 0
    functions = {}
    print(descriptors)
    for descriptor, calculator in Descriptors.descList:
        if pointer < len(descriptors) and descriptor == descriptors[pointer]:
            # functions.append(calculator)
            functions[descriptor] = calculator
            pointer += 1
    return functions

def getFeaturesFrom(mol):
    fdefName = os.path.join(RDConfig.RDDataDir, "BaseFeatures.fdef")
    factory = ChemicalFeatures.BuildFeatureFactory(fdefName)
    feats = factory.GetFeaturesForMol(mol)
    print(len(feats))
   

def getFamilyFromFeatures(features):
    return features[0].GetFamily()

if __name__ in "__main__":
    molName = argv[1].rstrip(".smiles").split("/")[-1]
    mol = create_mol(argv[1])
    
    if len(argv) == 3:
        outputDirectory = argv[2]
        mkdir(outputDirectory)
        saveImageFromMol(outputDirectory + "/" + molName, mol)
        

    descriptors = ["NumHAcceptors", "NumHDonors"]
    calculators = getFunctionFrom(descriptors)
    
    numHAcceptors = calculators[descriptors[0]](mol)
    numHDonors = calculators[descriptors[1]](mol)
    print("水素結合ドナー -> {}".format(numHDonors))
    print("水素結合アクセプター -> {}\n".format(numHAcceptors))

    print("分子の特徴を計算します")
    getFeaturesFrom(mol)
    # features = getFeaturesFrom(mol)
    # pprint(features)
    # ret = getFamilyFromFeatures(features)
    # print("この分子は\"{}\"です".format(ret))