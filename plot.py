import numpy as np
from scipy.stats import linregress
import sys
import getopt
import json
import re
try:
    from matplotlib import pyplot as plt
except Exception:
    import matplotlib
    matplotlib.use('pdf')
    from matplotlib import pyplot as plt


def save_plot(alg_name, file_suffix, y_label, legend_list, title_prefix,
              is_log=False):
    plt.title(title_prefix + ' for {0} algorithm'.format(
                                                         re.sub(r'\_',
                                                                ' ',
                                                                alg_name)
                                                         )
              )

    plt.legend(legend_list, loc='upper left')
    if is_log:
        plt.xlabel('Log of no. of elements')
    else:
        plt.xlabel('No. of elements in array')
    plt.ylabel(y_label)
    plt.grid()
    plt.ticklabel_format(axis='both',
                         style='sci',
                         scilimits=(-3, 3),
                         useOffset=False)
    plt.savefig('out/pdf/' + alg_name + '_' + file_suffix + '.pdf')


def plot_log(execution_time_array, data_array_size,
             alg_name):
    '''Log plot of exec time
    Not very universal, you may have to tweak
    some numbers'''
    data_big_val = data_array_size  # which elem to start from
    data_big_val_log = np.log2(data_big_val)
    exec_time_log_arr = np.log2(execution_time_array)
    slope, _, _, _, err = linregress(data_big_val_log, exec_time_log_arr)
    # print(slope)
    # print(err)
    plt.plot(
        data_big_val_log, exec_time_log_arr
    )
    plt.text(10.0, 0.15,  # position of the text relative to axes
             'Linregress: slope = {0}\n err = {1}'.format(slope, err),
             horizontalalignment='left',
             verticalalignment='baseline')
    save_plot(alg_name, 'exec_log_log', 'Log of exec time',
              [''],
              'Log of exec time',
              is_log=True)
    plt.clf()


def plot_standard(argv, do_plot_log=False):
    try:
        with open(str(argv[0])) as input_file:
            data = json.load(input_file)
        with open(str(argv[1])) as input_array_size_file:
            data_array_size = json.load(input_array_size_file)
    except Exception:
        print('Usage: python plot.py [-l] <input_file>'
              '<input_array_size_file>')
        print('\tfor regular plotting, -l option for'
              'plotting log (you will need to tweak numbers in source file)')
        print('python plot.py -c <input_file0>,...'
              ' -n <input_array_size_file>')
        print('\tfor comparisons')
        print('Make sure you have valid json files')
        quit()

    file_name = re.sub('out/', '', str(argv[0]))
    alg_name = re.sub('.json', '', file_name)

    '''Execution time plot'''
    execution_time_array = [data_elem['execution_time']
                            for data_elem in data]
    plt.plot(data_array_size, execution_time_array, '-')
    save_plot(alg_name, 'exec_time', 'Execution time [s]',
              ['Execution time'],
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
    if do_plot_log:
        plot_log(execution_time_array, data_array_size, alg_name)


def plot_compare(opts, args):
    data_comp = []
    legends = []
    for opt, arg in opts:
        if opt == '-c':
            for file in arg.split(','):
                with open(file) as in_file:
                    data_comp.append(json.load(in_file))
                    legends.append(re.sub(r'_', ' ',
                                          re.sub('.json', '',
                                                 re.sub('out/', '', file)
                                                 )
                                          )
                                   )
        elif opt == '-n':
            with open(arg) as in_file:
                data_comp_arr_size = json.load(in_file)

    for data in data_comp:
        execution_time_array = [data_elem['execution_time']
                                for data_elem in data]
        plt.plot(data_comp_arr_size, execution_time_array)

    save_plot('all', 'comparison', 'Time of execution [s]',
              legends, 'Time of execution')


def main(argv):
    std_mode = True
    try:
        opts, args = getopt.getopt(argv, 'c:n:l')
    except getopt.GetoptError:
        exit()
    for opt, arg in opts:
        if opt == '-c':
            std_mode = False
            plot_compare(opts, args)
        if opt == '-l':
            std_mode = False
            plot_standard(argv[1:], True)

    if std_mode:
        plot_standard(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
