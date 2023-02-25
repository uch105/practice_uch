#include<string.h>
#include<stdio.h>

int main(){
    int n;
    scanf("%d",&n);
    char a[n][100];
    char l;
    for(int i=0;i<n;i++){
        scanf("%s",&a[i]);
    }
    for(int i=0;i<n;i++){
        if(strlen(a[i])>10){
            sprintf(l,"%d",strlen(a[i])-2);
            printf(a[i][0]+l+a[i][-1]);
            printf("\n");
        }
        else{
            printf(a[i]);
            printf("\n");
        }
    }
}