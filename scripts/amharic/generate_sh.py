PATH="./data/amhclean/"
with open("cleaned.txt") as cld:
    with open("run_sim.sh","w") as runsim:
        for line in cld:
            for file in line.strip().split():
                runsim.write(" python similarity.py -i " + PATH+file + "& \n")
