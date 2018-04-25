# door-schedule

A set of scripts to produce a teacher's door schedule from the PCC class schedule

## Problem to Solve:

We have the schedule from the PCC website. Can a script create the printed schedule we hang on the door.

## To Run

1. Install [Anaconda](https://www.anaconda.com/download/) and open the Anaconda Prompt

2. Clone the repo and create the conda environment

```bash
$ git clone https://github.com/ProfessorKazarinoff/door-schedule.git
$ cd door-schedule
$ conda env create -f environment.yml
```

3. Activate the ```schedule``` environment and run the ```run.py``` script

```bash
$ conda activate schedule
(schedule)$ python run.py
```

4. Look for the ```.xlsx``` files in the ```output``` directory

```bash
cd output
ls
```