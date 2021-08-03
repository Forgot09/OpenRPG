#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "userdata.h"

void title(char version[])
{
	printf("=====OpenRPG=====\n");
	printf("버전 : %s\n", version);
}

int fight(char enemy[])
{
	int power;
	int random;
	srand(time(NULL));
	
	if (enemy == "Slime") {
		random = rand();
		printf(random);
	}
}

int main(void)
{
	char game_version[] = "v0.01-dev";
	int ans;
	title(game_version);
	
	printf("1. 게임시작, 2. 나가기\n");
	printf(">");
	scanf("%d", &ans);
	if (ans == 1) {
		while (1) {
			printf("1. 던전, 2. 마을, 3. 나가기\n");
			printf(">");
			scanf("%d", &ans);
			switch(ans)
			{
				case 1: //던전
				    printf("===던전===\n");
				    break;
				case 2: //마을n
				    printf("===마을===\n");
				    break;
				case 3:
				    exit(0);
			}
		}
	}
	else if (ans == 2) {
		exit(0);
	}
	else {
		exit(0);
	}
}
