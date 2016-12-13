#!/bin/bash
#SBATCH -t 60
#SBATCH -p serial_requeue
#SBATCH -N 1
#SBATCH -c 4
#SBATCH --mem=8000
#SBATCH -o endgame1a.out
#SBATCH -e endgame1a.err
#SBATCH --mail-type=END
#SBATCH --mail-user=benjaminzheng@college.harvard.edu
python endgame1a.py
