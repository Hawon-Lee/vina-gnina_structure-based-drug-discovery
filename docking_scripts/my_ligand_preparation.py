import os
import numpy as np
import pandas as pd
import argparse
import inquirer
import subprocess
import random
from tqdm import tqdm

def parse_arguments():
    
    parser = argparse.ArgumentParser(description='ligand preparation for docking.')
    
    parser.add_argument(
        '--ligand', '-l',
        type=str,
        required=True,
        help='mol_id, smiles 로 구성된 csv 파일 경로'
        )
    parser.add_argument(
        '--out_dir', '-o',
        type=str,
        required=True,
        help='전처리 결과 sdf 파일들을 저장할 폴더'
        )
    parser.add_argument(
        '--create_batch', '-b',
        action='store_true',
        help='(Optional) 전처리된 smiles의 경로들을 txt 파일로 기록합니다.'
    )

    args = parser.parse_args()
    return args

def ligand_preparation(args):
    
    project_dir = os.path.join(args.out_dir, os.path.basename(args.ligand).split('.')[0])
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
        
    df = pd.read_csv(args.ligand)
    
    mol_ids, smiles = df.iloc[:, 0].values, df.iloc[:, 1].values
    
    pdbqt_files = []
    for mol_id, smile in zip(mol_ids, smiles):
        temp_smi_file = f"{project_dir}/{mol_id}.smi"
        temp_sdf_file = f"{project_dir}/{mol_id}.sdf"
        pdbqt_file = f"{project_dir}/{mol_id}.pdbqt"
        
        # smiles를 smi 파일로 저장
        with open(temp_smi_file, 'w') as fp:
            fp.write(f"{smile}")
            
        # smi -> sdf
        command = f"obabel -ismi {temp_smi_file} \
            -osdf -O {temp_sdf_file} \
            --gen3d --best -p 7.4"
        subprocess.run(command.split(), stdout=subprocess.DEVNULL)
        
        # sdf -> pdbqt
        command = f"mk_prepare_ligand.py -i {temp_sdf_file} \
            -o {pdbqt_file}"
        subprocess.run(command.split())
        
        with open(pdbqt_file, 'r') as fp:
            if fp.read() is not None:
                pdbqt_files.append(os.path.abspath(pdbqt_file))
        
        # temp 파일 삭제
        os.remove(temp_smi_file)
        os.remove(temp_sdf_file)

    if args.create_batch:
        with open(f"{project_dir}/batch.txt", 'w') as fp:
            fp.write('\n'.join(pdbqt_files))
            print(f"batch file was created at {project_dir}/batch.txt")
            
if __name__ == '__main__':
    ligand_preparation(parse_arguments())