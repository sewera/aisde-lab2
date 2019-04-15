import numpy as np
from matplotlib import pyplot as plt
import sys
import json
import re


def save_plot(alg_name, file_suffix, y_label, legend_list):
    plt.title('Time complexity for {0} algorithm'.format(alg_name))
    plt.legend(legend_list, loc='upper left')
    plt.xlabel('No. of elements in array')
    plt.ylabel(y_label)
    plt.grid()
    plt.savefig('out/' + alg_name + '_' + file_suffix + '.pdf')


if __name__ == '__main__':
    try:
        with open(str(sys.argv[1])) as input_file:
            data = json.load(input_file)
        with open(str(sys.argv[2])) as input_array_size_file:
            data_array_size = json.load(input_array_size_file)
    except Exception:
        print('Usage: python3 plot.py <input_file> <input_array_size_file>')
        quit()

    file_name = re.sub('out/', '', str(sys.argv[1]))
    alg_name = re.sub('.json', '', file_name)

    '''Execution time plot'''
    execution_time_array = [data_elem['execution_time'] for data_elem in data]
    plt.plot(data_array_size, execution_time_array, '-')
    save_plot(alg_name, 'exec_time', 'Execution time [s]', ['Execution time'])
    plt.clf()

    '''No of operations plot'''
    com_arr_alg = [elem['algorithm']['comparisons'] for elem in data]
    plt.plot(
        data_array_size, com_arr_alg, 'r--',
    )
    legends = [
        'Comparisons (algorithm)'
    ]
    save_plot(alg_name, 'oper_count', 'No. of operations', legends)
    plt.clf()

    '''No of comparisons'''
    com_arr_alg = [elem['algorithm']['comparisons'] for elem in data]
    plt.plot(
        data_array_size, com_arr_alg
    )
    save_plot(alg_name, 'comp_count', 'No. of comparisons', ['Comparisons'])
    plt.clf()

    '''No of swaps'''
    swps_arr_alg = [elem['algorithm']['swaps'] for elem in data]
    plt.plot(
        data_array_size, swps_arr_alg, 'b',
    )
    legends = [
        'Swaps (algorithm)'
    ]
    save_plot(alg_name, 'swap_count', 'No. of swaps', legends)
    plt.clf()

    '''No of operations implementation'''
    com_arr_imp = [elem['implementation']['comparisons'] for elem in data]
    add_arr_imp = [elem['implementation']['additions'] for elem in data]
    plt.plot(
        data_array_size, com_arr_imp, 'g.',
        data_array_size, add_arr_imp
    )
    legends = [
        'Comparisons (implementation)',
        'Additions (implementation)'
    ]
    save_plot(
        alg_name,
        'oper_count_impl', 'No. of operations (implementation)', legends
    )
    plt.clf()
