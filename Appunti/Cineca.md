
First of all we have to use two factor authentication, then we have to choose between hpc cluster resources and hpc cloud resources.

HPC
Each account has a project, each account can have multiple project associated with a certain username. 

Using the command  saldo -b \<User Account>   

when giving this command, there is a table with the following columns

- account (list of the projects)
- start/end date  the starting and ending of the period with cineca
- total hours (local):  the hours of using the CPU allocated to use the local cluster
- consumed (local): consumed CPU hours.
- total consumed %: percentage of the total hours consumed.
- month total/consumed: hours consumed for the month.

Billing policy

This is how the total consumption is computed. 
The budget consumption is measured in effective CPU hours (CPUh) and it is calculated on the amount of resources allocated per node and the duration of their usage. 

Once the resources are assigned they cannot be used by other users.

Bh =  T * N * R * C

- T : elapsed time in hours (tempo usato)
- N : number of allocated nodes
- R : reserved resources per node
- C : number of CPUs per node they are default cpu per node.
- Bh: billed hours

R measures the fraction of node resources reserved by a job that are UNAVAILABLE to the other users, 

This is defined by the maximum of all the the reserved resources (the number of gpu, cpu memory) divided by the total capacity of each respective resource on a single note.

requested cpu /C , requested gpu/total gpu   we select the max and use it in the Bh formula.

so users are charged based on the resourced made unavailable to other users.
There is a monthly budget computed by dividing the total budget over the number of months.
As the use percentage of monthly hours quota increases the priority decreases linearly.

----
Cineca offers some storage whuch can be divided into:
- temporary : after the expiry the data is cancelled
- permanent: data remains 6 months after the end of the projects.

Storage areas can be also:
- user specific
- shared : it can be accessed by all the users belonging to the same project.

The areas available are defined by these environment variables.

| **Name** | **Area Attributes**            | **Quota**                 | **Backup** | **Note**                                                                                                                |
| -------- | ------------------------------ | ------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| $HOME    | permanent, user specific       | 50 GB                     | daily      |                                                                                                                         |
| $WORK    | permanent, shared              | 1 TB                      | no         | Large data to be shared with project’s collaborators.                                                                   |
| $FAST    | permanent, shared              | 1 TB                      | no         | Only on [Leonardo](https://docs.hpc.cineca.it/hpc/leonardo.html#leonardo).<br><br>Faster I/O compared with outer areas. |
| $SCRATCH | temporary, user specific       | -/20 TB                   | no         | files older than 40 days<br><br>are deleted                                                                             |
| $TMPDIR  | temporary, user specific       | (-)                       | no         | directory removed<br><br>at job completion                                                                              |
| $PUBLIC  | permanent, open, user specific | 50 GB                     | no         | Only on [Leonardo](https://docs.hpc.cineca.it/hpc/leonardo.html#leonardo).                                              |
| $DRES    | permanent, shared              | defined<br><br>by project | no         |                                                                                                                         |
$HOME is the local area where you are placed after the login procedure. It is conceived to store quotas and small personal data.

*Specifics of my pc and home computer*

PC
Nome dispositivo	Simonepc
Processore	Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz (1.80 GHz)
RAM installata	8,00 GB (7,84 GB utilizzabile)
Tipo sistema	Sistema operativo a 64 bit, processore basato su x64

HOME COMPUTER
Nome dispositivo  DESKTOP-4TQE23E
Processore  12th Gen Intel(R) Core(TM) i9-12900 (2.40 GHz)
RAM installata 32,0 GB (31,7 GB utilizzabile) 
Tipo sistema   Sistema operativo a 64 bit, processore basato su x64
