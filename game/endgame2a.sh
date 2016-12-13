#!/bin/bash
#SBATCH -t 15
#SBATCH -p serial_requeue
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=8000
#SBATCH -o endgame2a.out
#SBATCH -e endgame2a.err
#SBATCH --mail-type=END
#SBATCH --mail-user=benjaminzheng@college.harvard.edu
python endgame2a.py
