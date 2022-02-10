import multiprocessing, ctypes



def smile_detection(thread_name, count2):

    for x in range(10):
        count2.value +=1
        print (thread_name,count2)

    return count2 

if __name__=="__main__":
    count = multiprocessing.Value(ctypes.c_int, 5)  # (type, init value)
    x = multiprocessing.Process(target=smile_detection, args=("Thread1", count))
    y = multiprocessing.Process(target=smile_detection, args=("Thread2", count))
    x.start()
    y.start()