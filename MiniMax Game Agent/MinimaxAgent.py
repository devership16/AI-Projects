from collections import deque
from operator import eq
from math import pow
import time

################################################# Alpha Beta

def cal_depth(size,time):
    
    if time > 1.0 and time <= 5.0:
        depth = 2 
    elif time >5.0 and time <25.0:
        if size <= 16:
            depth = 6
        elif size > 16 and size <=36:
            depth = 4
        elif size > 36 and size <=70:
            depth = 2
        else:
            depth = 2
    elif time >=25.0 and time <100.0:
        if size <= 16:
            depth = 6
        elif size > 16 and size <=36:
            depth = 4
        elif size > 36 and size <=70:
            depth = 2
        else:
            depth = 2
    elif time >=100.0 and time <250.0:
        if size <= 16:
            depth = 6
        elif size > 16 and size <=36:
            depth = 4
        elif size > 36 and size <=95:
            depth = 2
        else:
            depth = 2
    elif time >= 250:
        if size <= 16:
            depth = 8
        elif size > 16 and size <=36:
            depth = 6
        elif size > 36 and size <=100:
            depth = 4
        else:
            depth = 2
    else:
        depth = 1        
    
    return depth
    
def alpha_beta_pruning(grid,n,time):
    
    inf=float('inf') 
    best_score = -inf
    alpha=-inf
    beta=inf
    
    action=()

    score=0
    
    temp =[line[:] for line in grid]
    
    moves=get_sorted_moves(temp,n)
    
    size=len(moves)
#     print size
    print size
    depth=cal_depth( size, time)
    print depth
   
    for move in moves:
        temp =[line[:] for line in grid]
        
        score = min_alpha_beta_search(temp,depth-1,n,pow(move[0],2),alpha,beta,move[1])
        
        if score>best_score:
            best_score=score
            action=move[1]
         
#     print "Ans: "+str(action)
    
    return action

def min_alpha_beta_search(grid, depth,n,best_score,alpha,beta,seed):
    
    if depth == 0:
        return best_score
    
#     gravity_rearange_prune(grid,seed, n)
    grid = linear_gravity(grid, seed, n)
        
    if check_state(grid)==False:
        return best_score
     
    score=float('inf')
    temp =[line[:] for line in grid]
    
    moves=get_sorted_moves(temp,n)
    
    for move in moves:
        temp =[line[:] for line in grid]
         
        score_temp = max_alpha_beta_search(temp,depth-1,n,(best_score-pow(move[0],2)),alpha,beta,move[1])
         
        score=min(score,score_temp)
         
        if score <= alpha:
            return score
         
        beta=min(beta,score) 
       
    return score
 
def max_alpha_beta_search(grid, depth,n,best_score,alpha,beta,seed):
    
    if depth == 0:
        return best_score
    
#     gravity_rearange_prune(grid,seed, n)
    grid = linear_gravity(grid, seed, n)
           
    if check_state(grid)==False:
        return best_score
           
    score=float('-inf')
    temp =[line[:] for line in grid]
    
    moves=get_sorted_moves(temp,n)
    
    for move in moves:

        temp =[line[:] for line in grid]
        
        score_temp=min_alpha_beta_search(temp,depth-1,n,(best_score + pow(move[0],2)),alpha,beta,move[1])
         
        score=max(score,score_temp)

        if score>= beta:
            return score
            
        alpha=max(alpha,score)
     
    return score

############################################Single Move Generation

def get_fruit(grid, pos):
    x, y = pos
    return grid[x][y]

def get_next_fruit(element, direction):
    x, y = element
    change_x, change_y = direction
    return x + change_x, y + change_y

def is_valid_fruit_prune(grid, pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])

def is_valid_fruit(grid, pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[x]) and (grid[x][y]!='*')


def get_similar_fruit_list_prune(grid,seed):
    
    directions = (-1, 0), (0, +1), (+1, 0), (0, -1)
    
    match = grid[seed[0]][seed[1]]
    comp = {seed}
    queue = deque(comp)
    child = deque.pop
    count=0
    while queue:
        element = child(queue)
        for direction in directions:
            pos = get_next_fruit(element, direction)
            if pos not in comp:
                comp.add(pos)
                if is_valid_fruit_prune(grid, pos):
                    value = grid[pos[0]][pos[1]]
                    if eq(value, match):
                        queue.append(pos)
                        count=count+1
                        
        yield element
    
def convert_fruits(grid,picked_fruit_list,n):
    
    for row in xrange(n):
        for col in xrange(n):
            pos=row,col    
            if pos in picked_fruit_list:
                grid[row][col]='*'


def gravity_rearange(grid,picked_fruit_list,n):
    
    c=""
    convert_fruits(grid, picked_fruit_list, n)
    
    for row in reversed(xrange(n)):
        for col in reversed(xrange(n)):
            if grid[row][col]=='*' and row-1>=0:
                i=row
                change_row=row
                while i>=0:
                    c=grid[i][col]
                    if c!='*':
                        grid[i][col]=grid[change_row][col]
                        grid[change_row][col]=c
                        change_row-=1
                    i-=1
    
    return
                                     
def linear_gravity(grid,seed,n):
    
    dfs_fruit_list(grid, seed, n,grid[seed[0]][seed[1]])
    temp =[['*' for _ in xrange(n)] for _ in xrange(n)]
    for col in xrange(n):
        offset=n-1
        for row in reversed(xrange(n)):
            if grid[row][col] !='*':
                temp[offset][col]=grid[row][col]
                offset-=1
    
    return temp
    
    
def gravity_rearange_prune(grid,seed,n):
    
    c=""
    dfs_fruit_list(grid, seed, n,grid[seed[0]][seed[1]])
      
    for row in reversed(xrange(n)):
        for col in reversed(xrange(n)):
            if grid[row][col]=='*' and row-1>=0:
                i=row
                change_row=row
                while i>=0:
                    c=grid[i][col]
                    if c!='*':
                        grid[i][col]=grid[change_row][col]
                        grid[change_row][col]=c
                        change_row-=1
                    i-=1
    
    return

def dfs_fruit_list(grid,seed,n,value):
    r,c=seed
    
    grid[r][c]='*'
    
    if r+1<n and grid[r+1][c]==value:
        dfs_fruit_list(grid,(r+1,c), n,value)
    
    if r-1>=0 and grid[r-1][c]==value:
        dfs_fruit_list(grid, (r-1,c),n,value)
    
    if c+1<n and grid[r][c+1]==value:
        dfs_fruit_list(grid, (r,c+1), n,value)
    
    if c-1>=0 and grid[r][c-1]==value:
        dfs_fruit_list(grid, (r,c-1), n,value)  
    
    return 

def dfs_fruits(grid,seed,value,n,count):
    r,c=seed
    count+=1
    
    grid[r][c]='*'
     
    if r+1<n and grid[r+1][c]==value:
        count=dfs_fruits(grid, (r+1,c), value, n,count)
        
    if r-1>=0 and grid[r-1][c]==value:
        count=dfs_fruits(grid, (r-1,c), value, n,count)
    
    if c+1<n and grid[r][c+1]==value:
        count=dfs_fruits(grid, (r,c+1), value, n,count)
    
    if c-1>=0 and grid[r][c-1]==value:
        count=dfs_fruits(grid, (r,c-1), value, n,count)
    
    return count

def get_sorted_moves(grid,n):
    
    temp=[]
    moves=[]
    for row in xrange(n):
        for col in xrange(n):
            if grid[row][col]!='*':
                seed =row,col      
                temp=dfs_fruits(grid,seed,grid[row][col],n,0)
                move=temp,seed
                moves.append(move)

    return sorted(moves,reverse=True)

def check_state(grid):
    
    for row in grid:
        for col in row:
            if col!='*':
                return True 
         
    return False


####################################### File Operations

def get_file_input():
    
    fin = open("input.txt","r")
    n = int(fin.readline())
    p = int(fin.readline())
    time = float(fin.readline())
    file_grid =  [line.strip() for line in fin]
    
    fin.close()
    
    return n,p,time,file_grid

def print_grid(move,grid):
    
    r=move[0]
    c=move[1]
    col_label=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    #r=col_label[0]
    fout = open("output.txt","w+")
    
    fout.write(col_label[c]+str(r+1)+"\n")
    print col_label[c]+str(r+1)
    for row in grid:
        fout.write("".join(row)+"\n")
        print "".join(row)
        
    fout.close()
    
    return
    
#################################### Main

def main():
    
    n,p,time,file_grid=get_file_input()
    
    original=[]
    for line in file_grid:
        row=[]
        for e in line:
            row.append(e)
        original.append(row)
     
    pick_fruit=alpha_beta_pruning(original,n,time)
    
    picked_fruit_list=list(get_similar_fruit_list_prune(original,pick_fruit)) 
          
    gravity_rearange(original, picked_fruit_list, n)
            
    print_grid(pick_fruit, original)

    return

#######################Program Start##################      

if __name__=='__main__':
    
    start=time.time()

    main()   
    print
    print "Time used = "+str(time.time()-start)+" seconds"
    
