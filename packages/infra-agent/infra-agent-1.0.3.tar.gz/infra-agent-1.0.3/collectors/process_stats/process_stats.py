import psutil
import logging

from collectors.utilities.process_output import get_subprocess_output


def get_list_of_process_sort_by_memory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    list_of_process_objects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'status'])
            # if pinfo['status'] == psutil.STATUS_RUNNING:
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            individual_process = psutil.Process(pid=pinfo['pid'])
            with individual_process.oneshot():
                pinfo['memory'] = dict(individual_process.memory_info()._asdict())
                pinfo['memory_percent'] = individual_process.memory_percent()
                pinfo['cpu'] = dict(individual_process.cpu_times()._asdict())
                pinfo['cpu_percent'] = individual_process.cpu_percent()
                pinfo['cpu_num'] = individual_process.cpu_num()
                pinfo['threads'] = individual_process.num_threads()
                pinfo['fds'] = individual_process.num_fds()
                pinfo['num_ctx_switches'] = dict(individual_process.num_ctx_switches()._asdict())
                pinfo['io_counters'] = dict(individual_process.io_counters()._asdict())
                pinfo['process_command'] = None
            list_of_process_objects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    list_of_process_objects = sorted(list_of_process_objects, key=lambda procObj: procObj['vms'], reverse=True)

    return list_of_process_objects


class ProcessStats():
    @classmethod
    def retrieve(self):
        processes = get_list_of_process_sort_by_memory()
        ps_arg = 'aux'
        output, _, _ = get_subprocess_output(['ps', ps_arg], logging)
        processLines = output.splitlines()  # Also removes a trailing empty line

        del processLines[0]  # Removes the headers
        for item in processLines:
            if isinstance(item, bytes):
                item = (item.decode('utf-8'))
            split_item = (item.split(" "))
            split_item = [splitted_item for splitted_item in split_item if splitted_item and len(splitted_item) > 0]
            for row in processes:
                if row['pid'] == int(split_item[1]):
                    if row['cpu_percent'] <= 0:
                        row['cpu_percent'] = float(split_item[2])
                        row['process_command'] = split_item[-1]

        return {'processes': processes}
