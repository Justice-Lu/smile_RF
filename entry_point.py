import os
import shutil
import sys
import subprocess
import string
import logging as log
import numpy as np

# Add repo to path!
MAIN_PACKAGE_DIR = os.path.abspath(os.curdir)    
sys.path.append(MAIN_PACKAGE_DIR)

from graph_cnn.data_prep.data_generator import generateLigandMatrices

from graph_cnn.data_prep import data_generator
from cli_arguments import ModelingParser
from graph_cnn.model import GraphCNN
from graph_cnn.run_model import runModel, runGNN
#from graph_cnn.ligand_handlers import LigandAdjacencyData, LigandFeatureData
#from graph_cnn.protein_handlers import ProteinAdjacencyData, ProteinFeatureData

try:
    from graph_cnn.hp_model import optimizeHyperparameters
except:
    pass
import config

def createTemporaryDirectories():
    os.mkdir(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_bgf'))
    os.mkdir(os.path.join(MAIN_PACKAGE_DIR, 'temp_ligand_adj_npy'))
    os.mkdir(os.path.join(MAIN_PACKAGE_DIR, 'temp_ligand_feat_npy'))
    os.mkdir(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_adj_npy'))
    os.mkdir(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_feat_npy'))


def removeTemporaryDirectories():
    # FIXME make it catch exception when the directory doesn't exist
    shutil.rmtree(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_bgf'))
    shutil.rmtree(os.path.join(MAIN_PACKAGE_DIR, 'temp_ligand_adj_npy'))
    shutil.rmtree(os.path.join(MAIN_PACKAGE_DIR, 'temp_ligand_feat_npy'))
    shutil.rmtree(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_adj_npy'))
    shutil.rmtree(os.path.join(MAIN_PACKAGE_DIR, 'temp_protein_feat_npy'))
    

def generateNpyMatrices(protein_path='input_protein_pdb', ligand_path='input_ligand_mol'):
    data_generator.generateProteinMatrices(
        pdb_path=protein_path,
        bgf_path='temp_protein_bgf',
        target_adj_path='temp_protein_adj_npy',
        target_feat_path='temp_protein_feat_npy'
    )
    
    data_generator.generateLigandMatrices(
        mol_path=ligand_path,
        target_adj_path='temp_ligand_adj_npy',
        target_feat_path='temp_ligand_feat_npy'
    )


def generateLabelsList(protein_folder='input_protein_pdb', ligand_folder='input_ligand_mol'):
    protein_files = os.listdir(protein_folder)
    mol_files = os.listdir(ligand_folder)
    X_list = []
    for p_file in protein_files:
        if p_file.endswith('.pdb'):
            for m_file in mol_files:
                if m_file.endswith('.mol'):
                    X_list.append([p_file[:-4], m_file[:-4]])

    return X_list 


def savePredictions(label_list, results):
    with open('predeicted_results.txt', 'w') as results_file:
        for i in range(len(label_list)):
            results_file.write(
                str(label_list[i][0]) + ',' + str(label_list[i][1]) + ',' + str(results[i]) + '\n'
                )

def ppp():    
    parser = ModelingParser()
    parser.setup_arguments()
    args = parser.parse_args()

    if args.batch_size:
        batch_size = args.batch_size
    else:
        batch_size = -1
    
    if args.model == 'gnn':

        if args.gnn_mode == 'hptuning':
            optimizeHyperparameters()
        
        elif args.gnn_mode == 'eval_tuple':
            X = generateLabelsList()
            createTemporaryDirectories()
            log.info('Generated BGF and MOL files in temp directories.')
            
            try:
                generateNpyMatrices()
                log.info('Generated NPY arrays')
                
                temp_folders=[
                    'temp_protein_adj_npy',
                    'temp_protein_feat_npy',
                    'temp_ligand_adj_npy',
                    'temp_ligand_feat_npy'
                ]
                g = GraphCNN()
                g.initialize()
                temp_tensors, dummy_y = g.getTensors(X, ['0']*len(X), temp_folders)
                
                model = runModel(batch_size=batch_size)
                predicted_value = runGNN(model, temp_tensors)
                log.info('The predicted binding affinity is ' + str(predicted_value))
                print('The predicted value is ', predicted_value)
            finally:
                removeTemporaryDirectories()

            
        elif args.gnn_mode == 'eval_protein':
            
            X = generateLabelsList(ligand_folder=config.MOL_FILES_PATH)
            createTemporaryDirectories()
            try:
                generateNpyMatrices(ligand_path=config.MOL_FILES_PATH)
                log.info('Generated NPY arrays')
                
                temp_folders=[
                    'temp_protein_adj_npy',
                    'temp_protein_feat_npy',
                    'temp_ligand_adj_npy',
                    'temp_ligand_feat_npy'
                ]
                g = GraphCNN()
                g.initialize()
                temp_tensors, dummy_y = g.getTensors(X, ['0']*len(X), temp_folders)
                
                model = runModel(batch_size=batch_size)
                predicted_values = runGNN(model, temp_tensors)
                log.info('The predicted binding affinity is ' + str(predicted_values))
                print('The predicted value is ', predicted_values)
                savePredictions(X, predicted_values)
            finally:
#                pass
                removeTemporaryDirectories()
        elif args.gnn_mode == 'eval_ligand':
            pass
        else:
            model = runModel(batch_size)
    
    elif args.model == 'cnn':
        print('CNN CLI is not implemented yet!')
    
    elif args.model == 'rf':
        print('RF CLI is not implemented yet!')

ppp()

