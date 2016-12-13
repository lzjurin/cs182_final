#!/bin/bash
#SBATCH -t 60
#SBATCH -p serial_requeue
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=8000
#SBATCH -o endgame1p.out
#SBATCH -e endgame1p.err
#SBATCH --mail-type=END
#SBATCH --mail-user=benjaminzheng@college.harvard.edu
python endgame1p.py
