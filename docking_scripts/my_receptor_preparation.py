import os
import numpy as np
import argparse
import inquirer
import subprocess
import random

def parse_arguments():
    parser = argparse.ArgumentParser(description='protein preparation for docking.')
    
    parser.add_argument(
        '--receptor', '-r',
        type=str,
        required=True,
        help='단백질 PDB 파일 경로'
        )
    parser.add_argument(
        '--out', '-o',
        type=str,
        required=True,
        help='결과물 파일을 저장할 경로'
        )
    parser.add_argument(
        '--autobox_path', '-a',
        type=str,
        default=None,
        help='리간드 정보로부터 자동 계산한 box 정보를 저장할 경로 (option)'
    )
    parser.add_argument(
        '--autobox_size', '-s',
        type=float,
        default=25,
        help='리간드 정보로부터 자동 계산할 box의 크기 (option)'
    )
    
    args = parser.parse_args()
    return args

def select_with_inquirer(tuple_options):
    # 표시용 문자열 생성
    display_options = [f"resname '{tup[0]}' - chainID '{tup[1]}'" for tup in tuple_options]
    
    # 표시할 옵션과 원래 튜플을 매핑
    option_map = {display_options[i]: tuple_options[i] for i in range(len(tuple_options))}
    
    questions = [
        inquirer.List('chosen_option',
                      message="Box를 계산할 레퍼런스 리간드를 선택하세요",
                      choices=display_options,
                     )
    ]
    answers = inquirer.prompt(questions)
    
    # 사용자가 선택한 문자열을 원래 튜플로 변환
    selected_display = answers['chosen_option']
    selected_tuple = option_map[selected_display]
    
    return selected_tuple

def get_ligand_center(pdb_path, lig_name, chain2parse):
    with open(pdb_path, 'r') as f:
        ligand_geom = []
        for l in f:
            if l.startswith('HETATM') and l[17:20]==lig_name:
                if l[21] == chain2parse:
                    x, y, z = float(l[30:38]), float(l[38:46]), float(l[46:54])
                    ligand_geom.append([x,y,z])
        ligand_center = np.array(ligand_geom).mean(axis=0)
        return ligand_center

def protein_preparation(args):
    
    BUFFERS = ['GOL', 'PEG', 'EDO', 'SO4', 'BIS']
    
    with open(args.receptor, 'r') as fp:
        pdb_raw = fp.read().splitlines()
        
    # get hetatm name for binding box setting
    hetatms = []
    prot_lines = []
    for line in pdb_raw:
        if line.startswith("HET   "):
            lig_name, lig_chain_id = line[7:10], line[12]
            if lig_name not in BUFFERS:
                hetatms.append((lig_name, lig_chain_id))
        
        elif line.startswith("ATOM  ") or line.startswith("TER   "):
            prot_lines.append(line)
        
    prot_lines.append("END")
    
    identifier = random.randint(0, 999999)
    with open(f"temp_{identifier}.pdb", 'w') as fp:
        prot_text = "\n".join(prot_lines)
        fp.write(prot_text)
    
    box_resname, box_chain = select_with_inquirer(hetatms)
    ligand_center = get_ligand_center(args.receptor, box_resname, box_chain)
    
    if args.autobox_path:
        with open(args.autobox_path, 'w') as fp:
            fp.write(f'''center_x = {ligand_center[0]}
center_y = {ligand_center[1]}
center_z = {ligand_center[2]}

size_x = {args.autobox_size}
size_y = {args.autobox_size}
size_z = {args.autobox_size}''')
            print(f"Box config file was successfully generated at {args.autobox_path}")
    command = f"prepare_receptor4.py -r temp_{identifier}.pdb \
                -A bonds_hydrogens \
                -U nphs_lps_waters_nonstdres \
                -o {args.out}"
            
    subprocess.run(command.split())
    
    os.remove(f"temp_{identifier}.pdb")
    print(f"Successfully converted into pdbqt. Path: {args.out}")
            

if __name__ == '__main__':
        protein_preparation(parse_arguments())