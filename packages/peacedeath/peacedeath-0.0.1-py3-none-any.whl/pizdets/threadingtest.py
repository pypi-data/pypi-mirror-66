import peacedeath, schedule, time
from multiprocessing import Pool
import threading,multiprocessing

schedule.clear()


def exp_loop_subprocess():
    # schedule.clear()
    schedule.every(5).seconds.do(print, time.time())

    while True:
        schedule.run_pending()
        time.sleep(1)

def job_that_executes_once():
    print("insertion")
    return schedule.CancelJob

def do_job_that_executes_once():
    schedule.every().second.do(job_that_executes_once)

# with Pool(2) as p:
#     p.map(exp_loop_subprocess)
#     p.map(do_job_that_executes_once)
#

# import multiprocessing
# multiprocessing.Process(exp_loop_subprocess()).start()
# multiprocessing.Process(exp_loop_subprocess()).start()
#
# working:
thread = threading.Thread(target=exp_loop_subprocess, args=())
thread.daemon = True
thread.start()

# do_job_that_executes_once()

