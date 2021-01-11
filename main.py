
from typing import List

import networkx as nx

class Worker:
    name: str # Worker name, for display.
    first_shift: int
    preferences: List # preferences[0] is the best shift for the worker.
                      # preferences[1] is the 2nd-best shift for the worker. etc...
    current_shift: int # The shift to which the worker is currently assigned
    flag: int

def work(list:Worker,num:int):
    count=0;
    for i in list:
        if i.current_shift==num and i.flag==0:
            return count
        count=count+1
    count=0
    for i in list:   # just one in cycle- return itself
        if(i.flag==0):
            return count
        count = count + 1

def exchange_shifts (workers: List[Worker]):
    """
    #one circle of all workers
    >>> a=Worker()
    >>> a.preferences=[3,2,1]
    >>> a.current_shift=1
    >>> a.first_shift=1;
    >>> a.flag=0
    >>> a.name="Avraham"

    >>> b=Worker()
    >>> b.preferences=[1,3,2]
    >>> b.current_shift=2
    >>> b.first_shift=2;
    >>> b.flag=0
    >>> b.name="Isaac"

    >>> c=Worker()
    >>> c.preferences=[2,1,3]
    >>> c.current_shift=3
    >>> c.first_shift=3;
    >>> c.flag=0
    >>> c.name="Yaakov"

    >>> workers=[a,b,c]
    >>> exchange_shifts(workers)
    Avraham moves from shift 1 to shift 3
    Isaac moves from shift 2 to shift 1
    Yaakov moves from shift 3 to shift 2

    #one circle of worker 1 and 2
    >>> a=Worker()
    >>> a.preferences=[2,3,1]
    >>> a.current_shift=1
    >>> a.first_shift=1;
    >>> a.flag=0
    >>> a.name="Avraham"

    >>> b=Worker()
    >>> b.preferences=[1,3,2]
    >>> b.current_shift=2
    >>> b.first_shift=2;
    >>> b.flag=0
    >>> b.name="Isaac"

    >>> c=Worker()
    >>> c.preferences=[2,1,3]
    >>> c.current_shift=3
    >>> c.first_shift=3;
    >>> c.flag=0
    >>> c.name="Yaakov"

    >>> workers=[a,b,c]
    >>> exchange_shifts(workers)
    Avraham moves from shift 1 to shift 2
    Isaac moves from shift 2 to shift 1
    Yaakov remains in 3 shift

    #No replacement
    >>> a=Worker()
    >>> a.preferences=[1,2]
    >>> a.current_shift=1
    >>> a.first_shift=1;
    >>> a.flag=0
    >>> a.name="Avraham"

    >>> b=Worker()
    >>> b.preferences=[2,1]
    >>> b.current_shift=2
    >>> b.first_shift=2;
    >>> b.flag=0
    >>> b.name="Isaac"
    >>> workers=[a,b]
    >>> exchange_shifts(workers)
    Avraham remains in 1 shift
    Isaac remains in 2 shift
    """
    count_of_workers_shift=0
    while(count_of_workers_shift<len(workers)):  #pass on all workers's preferences
        G = nx.DiGraph()
        for i in workers:  #insert to graph
            temp=(i.current_shift)
            temp2=(i.preferences[0])
            G.add_edge(temp, temp2);

        for cycle in nx.simple_cycles(G):
            listcycle=cycle
            first_shift_in_cycle = workers[0].current_shift;  #save the first worker's shift on the circle
            count=0;
            for i in listcycle:
                if(count<len(listcycle)-1):  #not the last one on the circle
                    index1=work(workers,i)  # index of worker i
                    index2=work(workers,listcycle[count+1]) # index of next worker on the circle
                    workers[index1].current_shift=workers[index2].current_shift
                    workers[index1].flag=1  #shift
                    count_of_workers_shift=count_of_workers_shift+1
                    for j in workers:  #erase for all workers this current shift
                        if(j.preferences.__contains__(workers[index2].current_shift)):
                             j.preferences.remove(workers[index2].current_shift);
                    count = count + 1

                else: #The last one on the circle

                    index1 = work(workers, i)
                    if(workers[index1].preferences.__contains__(first_shift_in_cycle)): #first_shift_in_cycle is still not taken
                        workers[index1].current_shift=first_shift_in_cycle
                    # else worker stays with it shift
                    workers[index1].flag = 1
                    count_of_workers_shift=count_of_workers_shift+1
                    for j in workers:
                        if(j.preferences.__contains__(workers[index1].current_shift)):
                             j.preferences.remove(workers[index1].current_shift);


        ################look at this example
    for j in workers:
        if(j.first_shift!=j.current_shift):
           print(j.name,"moves from shift",j.first_shift,"to shift",j.current_shift)
        else:
            print(j.name, "remains in", j.first_shift, "shift")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
