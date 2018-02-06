# -*- coding: utf-8 -*-
"""
@author: Aaron Penne
"""

import time
import datetime
import psutil as ps

file_out = "C:/tmp/system_status.txt"

def get_values():
    cpu = ps.cpu_percent()
    ram = ps.virtual_memory().percent
#    disk = ps.disk_io_counters()
    return (cpu, ram)

def main():
    # Write the header values
    with open(file_out, "a+") as f:
            f.write("Date\tTime\tCPU\tRAM\n")
    
    while 1:
        time.sleep(0.5)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d\t%H:%M:%S.%f")
        values = get_values()
        with open(file_out, "a+") as f:
            f.write(timestamp + "\t" +
                    str(values[0]) + "\t" +
                    str(values[1]) +
                    "\n")

            
if __name__ == "__main__":
    main()