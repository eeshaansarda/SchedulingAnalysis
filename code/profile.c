#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define BILLION 1000000000L;
#define USING_STARTTIME 1
#define START_TIME 0.002 // 2 milliseconds after start
#define END_TIME   0.003 // 3 milliseconds after start

clock_t startm, stopm, global_s, global_end;

double get_current_time() {
	static int start = 0, startu =0;
	struct timeval tval;
	double result;

	if (gettimeofday(&tval, NULL) == -1)
		result = -1.0;
	else if(!start) {
		start = tval.tv_sec;
		startu = tval.tv_usec;
		result = 0.0;
	}
	else
		result = (double) (tval.tv_sec - start) + 1.0e-6*(tval.tv_usec - startu);

	return result;

}

int main(int argc, char *argv[])
{
	double start, stop, accum =0;
	pid_t child;
	int status;
	struct user_regs_struct regs;
	int orig_rax;

	double cpu_start_time = get_current_time(); 
	child = fork();
	if (child == 0) {
		// Register child process as the process to be traced, then exec the programm passed in parameters
		ptrace(PTRACE_TRACEME, 0, NULL, NULL);
		execvp(argv[1], argv+1);
		exit(0);
	} else {
		wait(&status); // Receive SIGCHLD signal sent by subprocess

        int once = 0;
		while (1) {
			// Continue the child process until it requests a systemcall
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);

			wait(&status); 			// Wait until something happens -- a syscall or the child ends
			if (WIFEXITED(status)) { 	// If the child process exits, the trace is terminated
				break;
			}

			// The child is still alive, so it is trying to call a syscall. Get the start time
			start = get_current_time();

			// Here we can mess with the registers. We are only interested 
			// in the RAX register -- which system call is it?
			ptrace(PTRACE_GETREGS, child, 0, &regs);
			orig_rax = regs.orig_rax; 
            if (!USING_STARTTIME || (start >= START_TIME && start <= END_TIME))
                printf("%lf, ", start);
                // printf("Entering syscall: %d at %lf\n", orig_rax, start);

			// Now we can allow the child process to continue until it exists the system call
			ptrace(PTRACE_SYSCALL, child, NULL, NULL);

			wait(&status); 			// Wait until something happens -- syscall ends or child ends
			if (WIFEXITED(status)) { 	// If the child process exits, the trace is terminated
				break;
			}

			// The child is still alive, so it is just coming back from the syscall. Get the end time
			stop = get_current_time();

            if (!USING_STARTTIME || (start >= START_TIME && start <= END_TIME))
                printf("%lf\n", stop);
                // printf("Ending Syscall %d at %lf\n", orig_rax, stop);

            if (!USING_STARTTIME || (start >= START_TIME && start <= END_TIME))
                accum += (stop-start);

            if (USING_STARTTIME && (start > END_TIME && !once)) {
                printf("\ntotal : %f\n", get_current_time()-cpu_start_time);
                printf("syscalls: %f\n", accum);
                once++;
            }
		}
	}	
	double cpu_end_time=get_current_time();


	if(!USING_STARTTIME) printf("\ntotal : %f\n", cpu_end_time-cpu_start_time);
	if(!USING_STARTTIME) printf("syscalls: %f\n", accum);

	return 0;
}
