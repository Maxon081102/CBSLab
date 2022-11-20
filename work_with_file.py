def read_task_from_file(path):
    '''
    Reads map, start/goal positions and true value of path length between given start and goal from file by path. 
    '''

    tasks_file = open(path)
    tasks_file.readline()
    height = int(tasks_file.readline().split()[1])
    width = int(tasks_file.readline().split()[1])
    tasks_file.readline()
    cells = [[0 for _ in range(width)] for _ in range(height)]
    i = 0
    j = 0

    for l in tasks_file:
        j = 0
        for c in l:
            if c == '.':
                cells[i][j] = 0
            elif c == '@':
                cells[i][j] = 1
            else:
                continue
            j += 1
            
        if j != width:
            raise Exception("Size Error. Map width = ", j, ", but must be", width, "(map line: ", i, ")")
                
        i += 1
        if(i == height):
            break
    
    return (width, height, cells)

def read_tasks(file):
    file = file + ".scen"
    tasks_file = open(file)
    tasks = []
    tasks_file.readline()
    while True:
        task = tasks_file.readline()
        if task == "":
            break
        task = task.split()
        len_ = float(task[8])
        task = list(map(int, [task[0], task[4], task[5], task[6], task[7]]))
        task.append(len_)
        tasks.append(task)
    return tasks

