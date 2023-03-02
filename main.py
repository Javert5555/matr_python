import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from math import floor

# функция превращает двумерный список чисел в одномерный список строк
def get_str_from_double_array(array):
    str_array = []
    for row in array:
        # из numpy.int32 конвертируем в список
        row = list(row)
        for j in range(len(row)):
            row[j] = str(row[j])
        str_array.append(''.join(row))    
    return str_array
#############################################################

# def vector_check(checking_sys_matrix_transpose, error_vectors):
#     code_words = []
#     for i in range(len(error_vectors)):
#         # получаем кодовое слово по формуле c=i*Gsys
#         code_word = np.dot(error_vectors[i], checking_sys_matrix_transpose)
#         # если сумма единиц в столбце при умножении чётная, то записываем 0, иначе 1
#         for j in range(len(code_word)):
#             if (code_word[j] % 2 == 0):
#                 code_word[j] = 0
#             else:
#                 code_word[j] = 1
#         code_words.append(list(code_word))
#     return (code_words)


def get_error_vectors(checking_sys_matrix_transpose):
    # делаем копию, чтобы не менять исходную
    column_count = len(checking_sys_matrix_transpose[0,:])
    row_count = len(checking_sys_matrix_transpose)
    error_vectors = []
    # количество вектор ошибок равно количеству строк транспонированной проверочной матрицы
    for i in range(row_count):
        error_vector = []
        for j in range(row_count):
            error_vector.append(0)
        error_vector[i] = 1
        # т.к. единицы идут справа-налево по диагонали
        error_vector.reverse()
        error_vectors.append(error_vector)
    return(error_vectors)


def get_num_errors_found(d_min):
    num_errors_found = d_min - 1
    return num_errors_found

def get_num_errors_fixed(d_min):
    num_errors_fixed = floor((d_min-1)/2)
    return num_errors_fixed

def get_d_min(wtn):
    # делаем копию, чтобы не менять исходную
    wtn = list(wtn)
    while 0 in wtn:
        wtn.remove(0)
    d_min = min(wtn)
    return d_min


def get_wtn(code_words):
    wtn = []
    for el in code_words:
        wtn.append(sum(el))
    return wtn

def product_vector_matrix(vector, matrix):
    product_vector = np.dot(vector, matrix)
    # если сумма единиц в столбце при умножении чётная, то записываем 0, иначе 1
    for j in range(len(product_vector)):
        if (product_vector[j] % 2 == 0):
            product_vector[j] = 0
        else:
            product_vector[j] = 1
    return list(product_vector)

def get_code_words_or_syndromes(matrix, vectors):
    code_words_or_syndromes = []
    for i in range(len(vectors)):
        # получаем кодовое слово по формуле c=i*Gsys
        code_word = product_vector_matrix(vectors[i], matrix)
        # если сумма единиц в столбце при умножении чётная, то записываем 0, иначе 1
        code_words_or_syndromes.append(code_word)
    return code_words_or_syndromes


def get_inf_words(code_dimension, alphabet_power):
    inf_words = []
    for i in range(alphabet_power):
        # преобразовываем из 10-ой системы в 2-ую
        inf_word = [int(num) for num in list(bin(i)[2:])]
        # если длина полученного 2-ого числа меньше длины инф. слов, то добавляем нули влево 
        while len(inf_word) != code_dimension:
            inf_word.insert(0, 0)
        inf_words.append(inf_word)

    return inf_words

# получаем проверочную матрицу, при условии, что начальная матрица - порождающая
def get_checking_sys_matrix_from_general_sys(p_matrix, type_of_matrix):
    # получаем транспонированную матрицу P
    # объединяем матрицы P транспонированную и единичную матрицу
    match type_of_matrix:
        case 'general':
            p_matrix_transpose = p_matrix.transpose()
            row_count = len(p_matrix_transpose)
            checking_sys_matrix = np.hstack([p_matrix_transpose, np.eye(row_count)])
        case 'checking':
            row_count = len(p_matrix)
            checking_sys_matrix = np.hstack([np.eye(row_count), p_matrix])
    # print(checking_sys_matrix)
    return [ map(int, row) for row in checking_sys_matrix]

# в функции получаем матрицу P в зависимости от типа начальной матрицы
def get_p_matrix(matrix, type_of_matrix):
    column_count = len(matrix[0,:])
    row_count = len(matrix)
    # находим матрицу P взависимости от типа исходной матрицы
    match type_of_matrix:
        case 'general':
            # получаем правую часть порождающей матрицы (то есть без единичной матрицы слева размерностью row_count)
            p_matrix = matrix[:, [x for x in range(row_count, column_count)]]
            # print(p_matrix)
            if np.size(p_matrix) == 0:
                messagebox.showwarning(title="Предупреждение", message="Невозможно получить матрицу P")
                return
        case 'checking':
            # получаем левую часть порождающей матрицы (то есть без единичной матрицы справа размерностью column_count-row_count)
            p_matrix = matrix[:, [x for x in range(0, column_count-row_count)]]
            # print(p_matrix)
            if np.size(p_matrix) == 0:
                messagebox.showwarning(title="Предупреждение", message="Невозможно получить матрицу P")
                return
    return p_matrix


def get_sys_init_matrix(sys_matrix, init_type_matrix_value):
    column_count = len(sys_matrix[0,:])
    row_count = len(sys_matrix)

    if (row_count > column_count):
        messagebox.showwarning(title="Предупреждение", message="Матрица не может быть приведена к систематическому виду")
        return []
    
    # создаём массив столбцов единичной матрицы, здесь индекс столбца будет соответствовать позиици, на которой расположена единицы
    # в этом столбце
    i_sys = []
    for i in range(row_count):
        i_sys.append([0 for j in range(row_count)])
        i_sys[i][i] = 1

    # приводим матрицу к систематическому виду
    match init_type_matrix_value:
        case 'general':
            for i in range(row_count):
                for j in range(column_count):
                    # если столбец матрицы равен i-ому "столбцу" единичной матрицы, то
                    if (list(sys_matrix[:, j]) == i_sys[i]):
                        sys_matrix[:,[j, i]] = sys_matrix[:,[i, j]] # - меняем i-ый столбец с j-ым, чтобы получить единичную матрицу слева
            # проверяем действительно ли матрица систематическая (проверяем, получилась ли слева единичная матрицы)
            if not (np.array_equal(np.eye(row_count), sys_matrix[:, [x for x in range(row_count)]])):
                messagebox.showwarning(title="Предупреждение", message="Матрица не может быть приведена к систематическому виду")
                return []
        case 'checking':
            for i in range(row_count):
                for j in range(column_count):
                    if (list(sys_matrix[:, j]) == i_sys[i]):
                        # меняем i-ый столбец со столбцом под индексом column_count - (row_count - i), чтобы единичная матрица получилась справа
                        sys_matrix[:,[j, column_count - (row_count - i)]] = sys_matrix[:,[column_count - (row_count - i), j]]
            # проверяем действительно ли матрица систематическая (проверяем, получилась ли справа единичная матрицы)
            if not (np.array_equal(np.eye(row_count), sys_matrix[:, [x for x in range(column_count - row_count, column_count)]])):
                messagebox.showwarning(title="Предупреждение", message="Матрица не может быть приведена к систематическому виду")
                return []
    
    # print(sys_matrix[:, [x for x in range(row_count)]])


    return sys_matrix
    # general_matrix[:,[0, 1]] = general_matrix[:,[1, 0]]

# [[0 0 1 1]
#  [0 1 1 0]
#  [1 0 1 0]]
# a = np.array([[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1]])
# a = np.array([[1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1]])

# for el in get_checking_sys_matrix_from_general_sys(get_p_matrix(get_sys_init_matrix(a, 'checking'), 'checking').transpose(), 'checking'):
#     # print([e for e in el])
#     print(list(el))

def display_solution_matrix(input_matrix_values, init_type_matrix_value, v_vector):
    column_count = len(input_matrix_values[0,:])
    row_count = len(input_matrix_values)

    ################################
    code_length = column_count
    code_speed = round(row_count/column_count, 2)

    match init_type_matrix_value:
        case 'general':
            code_dimension = row_count

            general_sys_matrix = get_sys_init_matrix(input_matrix_values, init_type_matrix_value)
            # если матрица не может быть приведена к систематическому виду просто прерываем выполнение программы
            if np.size(general_sys_matrix) == 0: return

            p_matrix = get_p_matrix(general_sys_matrix, init_type_matrix_value)

            # если матрицы P не существует, то прерываем выполнение программы
            if p_matrix is None: return

            # из списка map объектов в обычный список
            checking_sys_matrix = [list(row) for row in get_checking_sys_matrix_from_general_sys(p_matrix, init_type_matrix_value)]
        case 'checking':
            code_dimension = column_count - row_count
            # print('dim',code_dimension)
            
            checking_sys_matrix = get_sys_init_matrix(input_matrix_values, init_type_matrix_value)
            # print('checking_sys_matrix',checking_sys_matrix)

            if np.size(checking_sys_matrix) == 0: return

            p_matrix = get_p_matrix(checking_sys_matrix, init_type_matrix_value).transpose()
            # print('p_matrix',p_matrix)

            # если матрицы P не существует, то прерываем выполнение программы
            if p_matrix is None: return

            general_sys_matrix = [list(row) for row in get_checking_sys_matrix_from_general_sys(p_matrix, init_type_matrix_value)]
            # print('general_sys_matrix',general_sys_matrix)
    
    alphabet_power = 2**code_dimension
    # print('alphabet_power',alphabet_power)

    inf_words = get_inf_words(code_dimension, alphabet_power)
    # print('inf_words',inf_words)

    code_words = get_code_words_or_syndromes(general_sys_matrix, inf_words)
    # print('code_words',code_words)

    wtn = get_wtn(code_words)
    # print('wtn',wtn)

    d_min = get_d_min(wtn)
    # print('d_min',d_min)

    num_errors_fixed = get_num_errors_fixed(d_min)
    # print('num_errors_fixed',num_errors_fixed)

    num_errors_found = get_num_errors_found(d_min)
    # print('num_errors_found',num_errors_found)

    if (num_errors_fixed != 0):

        checking_sys_matrix_transpose = np.array(checking_sys_matrix).transpose()

        # print('checking_sys_matrix_transpose',checking_sys_matrix_transpose)
        
        if (len(v_vector) != len(checking_sys_matrix_transpose)):
            messagebox.showwarning(title="Предупреждение", message="Длина v-вектора не равна количеству строк проверочной систематической транспонированной матрицы")
            return

        error_vectors = get_error_vectors(checking_sys_matrix_transpose)
        # print('error_vectors',error_vectors)

        syndromes = get_code_words_or_syndromes(checking_sys_matrix_transpose, error_vectors)
        # print('syndromes',syndromes)

        s_vector = product_vector_matrix(v_vector, checking_sys_matrix_transpose)
        # print('s_vector',s_vector)
        
        # получаем индекс нашего синдрома
        try:
            index_of_s_vector = syndromes.index(s_vector)
            # print('index_of_s_vector',index_of_s_vector)
        # если полученного синдрома нет в списке синдромов, то прерываем работу программы с ошибкой
        except:
            messagebox.showwarning(title="Предупреждение", message="Для данного вектора нет решения")
            return
        
        # получаем вектор ошибки с таким же индексом, как и у полученного синдрома
        e_vector = error_vectors[index_of_s_vector]
        # print('e_vector',e_vector)

        # получаем кодовое слово
        # для сложения векторов конвертируем из обычных массивов в np.Array() - объекты
        c_vector = list(np.array(v_vector) + np.array(e_vector))

        # в случае если случилась ситуация 1+1 в векторе c
        for i in range(len(c_vector)):
            if (c_vector[i] == 2):
                c_vector[i] = 0

        # print('c_vector',c_vector)

        # получаем индекс нашего кодового слова
        try:
            index_of_c_vector = code_words.index(c_vector)
            # print('index_of_c_vector',index_of_c_vector)
        # если полученного кодового слова нет в списке синдромов, то прерываем работу программы с ошибкой
        except:
            messagebox.showwarning(title="Предупреждение", message="Для данного вектора нет решения")
            return
        
        # получаем информационное слово с таким же индексом, как и у кодового слова
        i_vector = inf_words[index_of_c_vector]
        # print('i_vector',i_vector)
    


    ################################


    ###################################################################################
    ################################### tkInter #######################################
    ###################################################################################

    window = tk.Tk()     # создаем корневой объект - окно
    window.title('Начальные сведения')     # устанавливаем заголовок окна
    window.geometry('1000x500')    # устанавливаем размеры окна

    first_frame = tk.Frame(window, width=700, height=400)
    first_frame.pack(expand=1, fill='both')
    # frame = tk.Frame(window, width=700, height=400, borderwidth=1, relief='solid')

    canvas=tk.Canvas(first_frame,bg='#FFFFFF',width=700,height=400,scrollregion=(0,0,1000000,1000000))
    canvas.pack(side='left',expand=1,fill='both')

    vbar =ttk.Scrollbar(first_frame,orient='vertical',command=canvas.yview)
    vbar.pack(side='right',fill='y')
    # hbar =ttk.Scrollbar(first_frame,orient='horizontal',command=canvas.xview)
    # hbar.pack(side='bottom',fill='x')
    canvas.config(width=300,height=300)
    # canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.config(yscrollcommand=vbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox(('all'))))

    second_frame = ttk.Frame(canvas)
    second_frame['padding'] = (5, 5)
    canvas.create_window((0,0), window=second_frame, anchor='nw')

    # Длина кода (длина кодовых слов)
    code_length_label = tk.Label(second_frame, text='Длина кода, длина кодовых слов: {}'.format(code_length)).pack(anchor='nw')

    # Размерность кода, длина информационных слов
    code_dimension_label = tk.Label(second_frame, text='Размерность кода, длина информационных слов: {}'.format(code_dimension)).pack(anchor='nw')

    # Скорость кода
    code_speed_label = tk.Label(second_frame, text='Скорость кода: {}'.format(code_speed)).pack(anchor='nw')

    # Количество кодовых слов, мощность алфавита
    number_of_code_words_label = tk.Label(second_frame, text='Количество кодовых слов, мощность алфавита: {}'.format(alphabet_power)).pack(anchor='nw')

    # Систематическая порождающая матрица
    general_sys_matrix_label_value = get_str_from_double_array(general_sys_matrix)
    general_sys_matrix_title_label = tk.Label(second_frame, text='Систематическая порождающая матрица:').pack(anchor='nw')
    general_sys_matrix_label = tk.Label(second_frame, text='{}'.format('\n'.join(general_sys_matrix_label_value))).pack(anchor='nw')

    # Систематическая проверочная матрица:
    checking_sys_matrix_label_value = get_str_from_double_array(checking_sys_matrix)
    checking_sys_matrix_title_label = tk.Label(second_frame, text='Систематическая проверочная матрица:').pack(anchor='nw')
    checking_sys_matrix_label = tk.Label(second_frame, text='{}'.format('\n'.join(checking_sys_matrix_label_value))).pack(anchor='nw')

    third_frame = tk.Frame(second_frame, highlightbackground="black", highlightthickness=2)
    third_frame.pack(pady=20, anchor='nw')

    # Информационные слова (i)
    inf_words_label_value = get_str_from_double_array(inf_words)
    inf_words_label = tk.Label(third_frame, text='Информационные слова (i): \n{}'.format('\n'.join(inf_words_label_value))).pack(side='left')

    # Кодовые слова (c)
    code_words_label_value = get_str_from_double_array(code_words)
    code_words_label = tk.Label(third_frame, text='Кодовые слова (c): \n{}'.format('\n'.join(code_words_label_value))).pack(side='left')

    # wtn
    wtn_label_value = [str(num) for num in wtn]
    wtn_label = tk.Label(third_frame, text='wtn: \n{}'.format('\n'.join(wtn_label_value))).pack(side='left')

    # d_min
    d_min_label = tk.Label(second_frame, text='d min: {}'.format(str(d_min))).pack(anchor='nw')

    # num_errors_fixed (t)
    num_errors_fixed_label = tk.Label(second_frame, text='t: {} - количество исправляемых ошибок'.format(str(num_errors_fixed))).pack(anchor='nw')

    # num_errors_found (ρ)
    num_errors_found_label = tk.Label(second_frame, text='ρ: {} - количество ошибок гарантированно находит'.format(str(num_errors_found))).pack(anchor='nw')

    # если количество исправляемых равно 0, то прерываем решение
    if (num_errors_fixed == 0):
        return

    checking_sys_matrix_transpose_label_value = get_str_from_double_array(checking_sys_matrix_transpose)
    checking_sys_matrix_transpose_title_label = tk.Label(second_frame, text='Систематическая проверочная транспонированная матрица:').pack(anchor='nw')
    checking_sys_matrix_transpose_label = tk.Label(second_frame, text='{}'.format('\n'.join(checking_sys_matrix_transpose_label_value))).pack(anchor='nw')
    
    fourth_frame = tk.Frame(second_frame, highlightbackground="black", highlightthickness=2)
    fourth_frame.pack(pady=20, anchor='nw')

    table_title_label = tk.Label(fourth_frame, text='Таблица вектор-ошибок:').pack(side='top')

    # Синдромы (s)
    syndromes_label_value = [''.join(map(str, row)) for row in syndromes]
    syndromes_label = tk.Label(fourth_frame, text='Синдромы (s): \n{}'.format('\n'.join(syndromes_label_value))).pack(side='left')

    # Векторы ошибок
    error_vectors_label_value = get_str_from_double_array(error_vectors)
    error_vectors_label = tk.Label(fourth_frame, text='Векторы ошибок: \n{}'.format('\n'.join(error_vectors_label_value))).pack(side='left')

    # Полученный синдром (s)
    s_vector_label_value = [str(num) for num in s_vector]
    s_vector_label = tk.Label(second_frame, text='Полученный синдром (s): {}'.format(''.join(s_vector_label_value))).pack(anchor='nw')

    # Полученный вектор ошибки (e)
    e_vector_label_value = [str(num) for num in e_vector]
    e_vector_label = tk.Label(second_frame, text='Полученный вектор ошибки (e): {}'.format(''.join(e_vector_label_value))).pack(anchor='nw')

    # Полученный кодовое слово (c)
    c_vector_label_value = [str(num) for num in c_vector]
    c_vector_label = tk.Label(second_frame, text='Полученный кодовое слово (c): {}'.format(''.join(c_vector_label_value))).pack(anchor='nw')

    # Полученный информационное слово (i)
    i_vector_label_value = [str(num) for num in i_vector]
    i_vector_label = tk.Label(second_frame, text='Полученный информационное слово (i): {}'.format(''.join(i_vector_label_value))).pack(anchor='nw')





#####################################################
##################### main ##########################
#####################################################
def main():
    def get_solution():
        ############# тип матрицы
        init_type_matrix_value = init_type_matrix.get() # получаем тип матрицы

        # если пользователь не указал тип матрицы, то прерываем выполнение программы и выводим предупреждение на экран
        if (not init_type_matrix_value):
            messagebox.showwarning(title="Предупреждение", message="Укажите тип начальной мтарицы")
            return

        ############# матрицы
        # получаем значения матрицы с 1 строки до предпоследней (т.к. в Text последняя строка всегда пустая)
        # и разбиваем эти значения сначала по строкам, а потом по значениям в строке через пробел
        try:
            input_matrix_values = np.array([row.split() for row in input_initial_matrix.get('1.0','end-1c').strip().split('\n')], int)
        # если пользователь введёт не числа, а иные знаки
        except:
            messagebox.showwarning(title="Предупреждение", message="Введите корректные значения матрицы")
            return

        # если пользователь не ввёл значения матрицы, то прерываем выполнение программы и выводим предупреждение на экран
        if np.size(input_matrix_values) == 0:
            messagebox.showwarning(title="Предупреждение", message="Введите значения матрицы")
            return
        
        for row in input_matrix_values:
            for el in row:
                # если хотябы одно значение матрицы не является бинарным, то прерываем выполнение программы и выводим предупреждение на экран
                if not (el == 1 or el == 0):
                    messagebox.showwarning(title="Предупреждение", message="Введите бинарные значения матрицы")
                    return

        ############# вектор
        try:
            # input_v_vector_value =  input_v_vector.get('1.0', '2.0-1c').strip()
            input_v_vector_value = [int(num) for num in input_v_vector.get('1.0', '2.0-1c').strip()]
        # если пользователь введёт не числа, а иные знаки
        except:
            messagebox.showwarning(title="Предупреждение", message="Введите корректные значения вектора v")
            return 

        # если пользователь не ввёл значения вектора, то прерываем выполнение программы и выводим предупреждение на экран
        if(not input_v_vector_value):
            messagebox.showwarning(title="Предупреждение", message="Введите вектор v")
            return

        for el in input_v_vector_value:
            # если хотябы одно значение вектора не является бинарным, то прерываем выполнение программы и выводим предупреждение на экран
            if not (el == 1 or el == 0):
                messagebox.showwarning(title="Предупреждение", message="Вектор может состоять только из бинарных значений")
                return 

        display_solution_matrix(input_matrix_values, init_type_matrix_value, input_v_vector_value)

    root = tk.Tk()     # создаем корневой объект - окно
    root.title('Начальные сведения')     # устанавливаем заголовок окна
    root.geometry('580x500')    # устанавливаем размеры окна

    # f_top = tk.LabelFrame(text="Верх").pack()

    # создаем текстовую метку 'Выберите тип матрицы на входе: '
    label_init_type_matrix = tk.Label(text='Выберите тип матрицы на входе: ').place(x=5, y=5)

    init_type_matrix = tk.StringVar()

    general_btn = tk.Radiobutton(text='Порождающая', var=init_type_matrix, value='general').place(x=5, y=25)
    checking_btn = tk.Radiobutton(text='Проверочная', var=init_type_matrix, value='checking').place(x=150, y=25)


    # создаем текстовую метку 'Введите начальную матрицу'
    label_init_type_matrix = tk.Label(text='Введите начальную матрицу: ').place(x=5, y=70)
    # Обварачиваем скобки, чтобы в будущем получить значение этого поля через get()
    (input_initial_matrix := tk.Text(wrap='none', width=50, height=15)).place(x=5, y=100)
    # init_type_matrix

    # Ввод вектора v
    label_v_vector = tk.Label(text='Введите вектор v: ').place(x=5, y=350)
    # Обварачиваем скобки, чтобы в будущем получить значение этого поля через get()
    (input_v_vector := tk.Text(width=30, height=1)).place(x=5, y=370)


    btn_get_solution = tk.Button(text="Получить решение", command=get_solution, width=15, height=1).place(x=5, y=400)


    root.mainloop()

main()



# G:

# 1 1 0 0 1 1 0
# 0 1 1 1 1 0 0
# 0 1 1 0 0 1 1

# v: 0001011


# 1 0 1 1 0
# 0 1 0 1 1

# v: 10101

####################

# H:

# 1 1 0 0 1 1 0
# 0 1 1 1 1 0 0
# 0 1 1 0 0 1 1

# v: 1100110