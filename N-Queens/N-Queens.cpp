#include<iostream>
#include<cstring>
#include<fstream>
#include<cstdlib>
#include<ctime>
#include<cmath>
#define e 2.718281828459045

using namespace std;

int liz,n,ct=0,cur_x=0,cur_y=0,next_x=0,next_y=0;

long long int ctr=0;
bool tle=false,complete=false;
double tp=0;
clock_t start;


ifstream fin ("input.txt");
ofstream fout("output.txt");

//Helper function to display the nursery
inline void shownur(string nur[]){
  for(int i=0;i<=n-1;i++){
    //cout<<nur[i]<<"\n";
    fout<<nur[i]<<"\n";
    }
    //cout<<"\n";
  return;
}
// Helper function to get random numbers within a range
inline int getrand()
{
    int random_num=0;
    int low=0, high=n-1;

    //int random_num1=rand()%n;
    random_num = low + (rand() % (int)(high - low + 1));
    return random_num;
}
//Helper function to calculate remaining space available 
inline int rem_space(string nur[],int r,int c)
{
  int ts=0,rem=0,k;
  for(int i=r;i<=n-1;i++)
  {
    if(i==r)k=c;
    else k=0;

    for(int j=k;j<=n-1;j++)
    {
      if(nur[i][j]=='2'&&ts>0)
      {
        rem++;
        ts=0;
      }
      if(nur[i][j]=='0')
        ts++;
    }
    if(ts>0)
    {
      rem++;
      ts=0;
    }
  }
  return rem;
}
//Helper function to find random lizard to move
inline void rand_liz(string nur[])
{
    int i=getrand();
    int j=getrand();
    while(nur[i][j]!='1')
      {
        i=getrand();
        j=getrand();
      }
      cur_x=i;
      cur_y=j;
  return;
}
//Helper function to find cell to place a lizard
inline void rand_pos(string nur[])
{
    int i=getrand();
    int j=getrand();

    while(nur[i][j]!='0')
      {
        i=getrand();
        j=getrand();
      }
      next_x=i;
      next_y=j;
  return;
}

//Helper function to calculate probablity
inline bool cal_prob(double t, double d) {
    if (d < 0)
        return true;

    double p = pow(e,((-d) / t));
    double act = ((double) rand() / (RAND_MAX));

    if (act < p) {
        return true;
    }
    return false;
}

//Helper function to check validity of a cell
inline bool check(string arr[],int row,int col){

  //Left
  for(int j=col-1;j>=0;j--){
    if(arr[row][j]=='2')break;
    if(arr[row][j]=='1')return false;
  }
  //Right
  for(int j=col+1;j<=n-1;j++){
    if(arr[row][j]=='2')break;
    if(arr[row][j]=='1')return false;
  }
  //up
  for(int i=row-1;i>=0;i--){
    if(arr[i][col]=='2')break;
    if(arr[i][col]=='1') return false;
  }
  //bottom
  for(int i=row+1;i<=n-1;i++){
    if(arr[i][col]=='2')break;
    if(arr[i][col]=='1') return false;
  }
  //Diagonal Up
  for(int i=row-1,j=col-1;i>=0&&j>=0;i--,j--){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1')return false;
  }
  //Diagonal Down
  for(int i=row+1,j=col-1;i<n&&j>=0;i++,j--){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1')return false;
  }
  for(int i=row-1,j=col+1;i>=0&&j<=n-1;i--,j++){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1')return false;
  }
  for(int i=row+1,j=col+1;i<=n-1&&j<=n-1;i++,j++){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1')return false;
  }
  return true;
}

//Helper function to count conflicts given a cell coordinate 
inline int cal_conflicts ( string arr[],int row,int col)
{

    int conflicts = 0;

  /*//Left
  for(int j=col-1;j>=0;j--){
    if(arr[row][j]=='2')break;
    if(arr[row][j]=='1'){conflicts++;break;}
  }*/

  //Right
  for(int j=col+1;j<=n-1;j++){
    if(arr[row][j]=='2')break;
    if(arr[row][j]=='1'){conflicts++;break;}
  }
  /*//up
  for(int i=row-1;i>=0;i--){
    if(arr[i][col]=='2')break;
    if(arr[i][col]=='1'){conflicts++;break;}
  }*/
  //bottom
  for(int i=row+1;i<=n-1;i++){
    if(arr[i][col]=='2')break;
    if(arr[i][col]=='1') {conflicts++;break;}
  }
  /*//Left Diagonal Up
  for(int i=row-1,j=col-1;i>=0&&j>=0;i--,j--){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1'){conflicts++;break;}
  }*/
  /*//Left Diagonal Down
  for(int i=row+1,j=col-1;i<n&&j>=0;i++,j--){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1'){conflicts++;break;}
  }*/
  for(int i=row-1,j=col+1;i>=0&&j<=n-1;i--,j++){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1'){conflicts++;break;}
  }
  for(int i=row+1,j=col+1;i<=n-1&&j<=n-1;i++,j++){
    if(arr[i][j]=='2')break;
    if(arr[i][j]=='1'){conflicts++;break;}
  }
    //cout<<"Conflicts="<<conflicts<<"\n";
    return conflicts;
}

//Helper function to check for Tree(obstruction)
inline int check_tree(string nur[],int r ,int c)
{
  int i;
  for (i=c;i<=n-2;i++){
    if(nur[r][i]=='2')
      return i;
  }
  return 0;
}

//Function to recursively place lizards in the board using Depth First Search
bool dfs(string nur[],int q,int r,int c){

  int k=0;
  if(q==liz){
    return true;
    };

  clock_t endt=clock();
  tp=(double)(endt-start)/(double)(CLOCKS_PER_SEC);
  //cout<<"TP:"<<tp<<endl;
  if(tp>270){
    tle=true;
    return false;
  }

  if(ctr++>=10000000){
      tle=true;
      return false;
    }

    if(rem_space(nur,r,c)<(liz-q))
      return false;

    for(int i=r;i<=n-1;i++){
        if(q==liz){
          return true;
        };
        if(i==r)k=c;
        else k=0;
      for(int j=k;j<=n-1;j++){
         if(check(nur,i,j)&& nur[i][j]=='0'){
            nur[i][j]='1';
            //shownur(nur);

            if(j==n-1)r++;
            if(dfs(nur,q+1,r,c+1)){
                //cout<<ct++<<endl;
                //ctr++;
              return true;
          }
          nur[i][j]='0';
         }

      }
  }
  return false;
}


//Function to recursively place lizards in the board using Breadth First Search
bool bfs(string nur[],int q,int r,int c ){

  if(q==liz){
    return true;
    };
  clock_t endt=clock();
  tp=(double)(endt-start)/(double)(CLOCKS_PER_SEC);
  if(tp>270){
    tle=true;
    return false;
  }

    if(ctr++>=10000000){
       tle=true;
      return false;
    }
    for(int i=r;i<=n-1;i++){
        if(q==liz){
          return true;
        };
      for(int j=0;j<=n-1;j++){
         if(check(nur,i,j)&& nur[i][j]=='0'){
            nur[i][j]='1';
            //shownur(nur);
            if(j==n-1)r++;
            if(bfs(nur,q+1,r,c)){
              return true;
          }
          nur[i][j]='0';
         }

      }
  }
  return false;
}
inline int cal_energy(string arr[])
{
  int total=0;
  for(int i=0;i<=n-1;i++)
  {
    for(int j=0;j<=n-1;j++)
    {
      if (arr[i][j]=='1'){
        total=total+cal_conflicts(arr,i,j);
      }
    }
  }
  return total;
}

//Function to recursively place lizards in the board using Simulated Anneleaing(Heuristic Approach)
bool sa(string nur[])
{
  int i=0,j=0;
  int curr_energy=0,next_energy=0,d;

  bool done=false;
  double tem=100;
  long long int itr=2;

    while(true && tem>0 && itr<=10000000){

      clock_t endt=clock();
      tp=(double)(endt-start)/(double)(CLOCKS_PER_SEC);

      if(tp>240)
      {
        tle=true;
        complete=false;
        return false;
        //cout<<"\nTLE.....\n";
        //break;
      }

      curr_energy=cal_energy(nur);
      if(curr_energy==0)
      {
        done=true;
        complete=true;
        return done;
      }
        rand_liz(nur);
        rand_pos(nur);

      if(nur[next_x][next_y]=='0'){
        nur[next_x][next_y]='1';
        nur[cur_x][cur_y]='0';
      }

      next_energy=cal_energy(nur);

      if(next_energy==0){
        done=true;
        complete=true;
        return done;
      }
      d = next_energy-curr_energy;

      if(cal_prob(tem,d));
      else
      {
        nur[next_x][next_y]='0';
        nur[cur_x][cur_y]='1';

      }
      tem=(1/log(itr++));
    }
    return false;
}
inline void init_nur(string arr[])
{
  int q=liz;
  for(int i=0;i<=n-1&&q>0;i++)
  {
    for(int j=0;j<=n-1;j++){
      if(check(arr,i,j) && arr[i][j]=='0'){
        arr[i][j]='1';
        q--;
      }
    }
  }
  while(q>0)
  {
    int i=getrand();
    int j=getrand();
    if(arr[i][j]=='0')
    {
      arr[i][j]='1';
      q--;
    }
  }
  return;
}

/***********************************Main********************************/

//Driver Function
int main(){

  start=clock();
  srand((unsigned)time(0));

  int i,j;
  string type;
  char c;

  fin>>type>>n>>liz;
  //cin>>type>>n>>liz;

  string nur[n],cpy[n];

  for(i=0;i<=n-1;i++){
    fin>>nur[i];
    //cin>>nur[i];
  }
  c=type[0];
  switch(c){

    case 'B':
      if(bfs(nur,0,0,0)){
        //cout<<"OK\n";
        fout<<"OK\n";
        shownur(nur);
      }
      else{
        fout<<"FAIL\n";
        //cout<<"FAIL\n";
      }
      break;

    case 'S':

      for(i=0;i<=n-1;i++)
        cpy[i]=nur[i];

      init_nur(nur);
       //if(sa(nur)){
       complete=sa(nur);
          if(tle==false){
           if(complete){
          //cout<<"OK\n";
          fout<<"OK\n";
          shownur(nur);
           }
          else{
          fout<<"FAIL\n";
          //cout<<"FAIL\n";
          }
        }
      else{

       ctr=9000000;
        if(dfs(cpy,0,0,0)){
          //cout<<"OK\n";
          fout<<"OK\n";
          shownur(nur);
          }

        else{
          fout<<"FAIL\n";
          //cout<<"FAIL\n";
        }
      }
      break;

    case 'D':
//
        if(dfs(nur,0,0,0)){
          //cout<<"OK\n";
          fout<<"OK\n";
          shownur(nur);
          }

        else{
          fout<<"FAIL\n";
          //cout<<"FAIL\n";
        }

      break;

    default:
      if(dfs(nur,0,0,0)){
        //cout<<"OK\n";
        fout<<"OK\n";
        shownur(nur);
      }
      else{
        fout<<"FAIL\n";
        //cout<<"FAIL\n";
      }
      break;
    };

  fin.close();
  fout.close();
  return 0;
}
