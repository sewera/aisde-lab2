# import numpy as np
from matplotlib import pyplot as plt
import sys
import json
import re


def save_plot(alg_name, file_suffix, y_label, legend_list, title_prefix):
    plt.title(title_prefix + ' for {0} algorithm'.format(
                                                         re.sub(r'\_',
                                                                ' ',
                                                                alg_name))
              )

    plt.legend(legend_list, loc='upper left')
    plt.xlabel('No. of elements in array')
    plt.ylabel(y_label)
    plt.grid()
    plt.ticklabel_format(axis='both',
                         style='sci',
                         scilimits=(-3, 3),
                         useOffset=False)
    plt.savefig('out/' + alg_name + '_' + file_suffix + '.pdf')


if __name__ == '__main__':
    try:
        with open(str(sys.argv[1])) as input_file:
            data = json.load(input_file)
        with open(str(sys.argv[2])) as input_array_size_file:
            data_array_size = json.load(input_array_size_file)
    except Exception:
        print('Usage: python3 plot.py <input_file> <input_array_size_file>')
        print('Make sure you have valid json files')
        quit()

    file_name = re.sub('out/', '', str(sys.argv[1]))
    alg_name = re.sub('.json', '', file_name)

    '''Execution time plot'''
    execution_time_array = [data_elem['execution_time'] for data_elem in data]
    plt.plot(data_array_size, execution_time_array, '-')
    save_plot(alg_name, 'exec_time', 'Execution time [s]', ['Execution time'],
              'Time complexity')
    plt.clf()

    '''No of operations total plot'''
    com_arr_alg = [elem['algorithm']['comparisons'] for elem in data]
    swps_arr_alg = [elem['algorithm']['swaps'] for elem in data]
    com_arr_imp = [elem['implementation']['comparisons'] for elem in data]
    add_arr_imp = [elem['implementation']['additions'] for elem in data]
    plt.plot(
        data_array_size, com_arr_alg,
        data_array_size, swps_arr_alg,
        data_array_size, com_arr_imp,
        data_array_size, add_arr_imp
    )
    legends = [
        'Comparisons (algorithm)',
        'Swaps (algorithm)',
        'Comparisons (implementation)',
        'Additions (implementation)'
    ]
    save_plot(alg_name, 'oper_count', 'No. of operations', legends,
              'No. of total operations')
    plt.clf()
