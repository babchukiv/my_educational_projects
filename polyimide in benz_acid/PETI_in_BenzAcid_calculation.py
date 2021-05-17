print()
print("----"*15)
print('Расчёт синтеза олигомеров')
print('При вводе нескольких значений в качестве разделителя используется ПРОБЕЛ')
print()

def taking_the_information(di_name):
    di_names = input(f'Введите название молекулы (молекул) {di_name}а: ').upper().split()
    return di_names
        
def taking_mol_relations(di_name, lenn):
    if lenn > 1:
        print(f'<В поле ниже нажмите "Enter" для использования {round(1/lenn, 3)} моль для каждого {di_name}а>')
        di_prop = [float(i) for i in input(f'Ввeдите cоответствующие мольные доли {di_name}ов: ').split()]
        if di_prop == []:
            di_prop = [ 1/lenn for i in range(lenn) ]
            print(f'\n{54*"*"}\n**** Доля каждого {di_name}а составляет {round((1/lenn), 3)} моль ****\n{54*"*"}\n')
    else:
        di_prop = [1]
    return di_prop

def total_mol_weight_calc(diang, diang_proportion, diamin, diamin_proportion):
    global n
    n = float(input("Введите число олигомеризации: "))
    M = 2*(Mol_weights["PEPA"] - 16) - 4
    link_M = 0
    for current_term_diam, current_term_proportion in zip(diamin, diamin_proportion):
        M += Mol_weights[current_term_diam] * current_term_proportion
    for reag_diang_name, mol_diang_fract in zip(diang, diang_proportion):
        M += (Mol_weights[reag_diang_name] - 32) * mol_diang_fract * n
        link_M += (Mol_weights[reag_diang_name] - 32) * mol_diang_fract
    for reag_diamin_name, mol_diamin_fract in zip(diamin, diamin_proportion):
        M += (Mol_weights[reag_diamin_name] - 4) * mol_diamin_fract * n
        link_M += (Mol_weights[reag_diamin_name] - 4) * mol_diamin_fract
    return (M, link_M)
    
def total_masses(M_and_link_M, diang, diang_proportion, diamin, diamin_proportion):
    product_mass = float(input("Введите желаемую массу продукта: "))
    w = float(input("Введите желаему концентрацию продукта в БК (в %): "))
    total_quantity = product_mass/M_and_link_M[0]
    m_PEPA = 2 * total_quantity * Mol_weights["PEPA"]
    total_prod_mass = 0
    total_prod_mass += m_PEPA
    print()
    print()
    print("Результаты расчёта:")
    print(f"Молекулярная масса олигомера составляет {round(M_and_link_M[0], 3)} г/моль")
    print(f"Молекулярная масса олигомерного звена составляет {round(M_and_link_M[1], 3)} г/моль")
    print()
    for reag_diang_name, mol_diang_fract in zip(diang, diang_proportion):
        a = n * mol_diang_fract * total_quantity * Mol_weights[reag_diang_name]
        total_prod_mass += a
        print(f"Необходимая масса {reag_diang_name} составляет {round(a, 3)} грамм")
    for reag_diamin_name, mol_diamin_fract in zip(diamin, diamin_proportion):
        a = (n * mol_diamin_fract + mol_diamin_fract) * total_quantity * Mol_weights[reag_diamin_name]
        total_prod_mass += a
        print(f"Необходимая масса {reag_diamin_name} составляет {round(a, 3)} грамм")
    print(f"Необходимая масса PEPA составляет {round(m_PEPA, 3)} грамм")    
    print(f"Необходимая масса БК (для {w} % конц) составляет {round(product_mass*100/w - product_mass, 3)} грамм")
    print()
    print(f"Масса выделившейся воды составляет {round(total_prod_mass-product_mass, 3)} грамм")
    print(f"Массовая доля выделившейся воды составляет {round((total_prod_mass-product_mass)/total_prod_mass, 3)}")
    
Mol_weights = {
                "ОДА": 200.24,
                "ODA": 200.24,
                "М-ФДА": 108.14,
                "ФДА": 108.14,
                "BPDA": 294.22,
                "БФДА": 294.22,
                "EBPA": 318.24,
                "M-TOLIDINE": 212.30,
                "6-FDA": 444.24,
                "ФЛУ": 348.45,
                "APF": 348.45,
                "ДАДФО": 310.22,
                "ДАДФМ": 198.27,
                "NEXIMID 400": 318.24,
                "NEXIMID-400": 318.24,
                "ДИАМИН-А": 410.52,
                "ДИАНГИДРИД-А": 520.49,
                "ДАБТК": 322.23,
                "PEPA": 248.24,
                "APB": 292.34
                }

# Getting general information about the reagents and corresponding mole fractions

diang = taking_the_information('диангидрид')
diang_proportion = taking_mol_relations('диангидрид', len(diang))

diamin = taking_the_information('диамин')
diamin_proportion = taking_mol_relations('диамин', len(diamin))

# Total molar mass calculating

total_mol_weight = total_mol_weight_calc(diang, diang_proportion, diamin, diamin_proportion)

# Getting the final ammounts of the reagents:

total_masses(total_mol_weight, diang, diang_proportion, diamin, diamin_proportion)

print()
print("Чтобы закрыть окно нажмите Enter")
k = input()
