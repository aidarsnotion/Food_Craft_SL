from main.models import *
from collections import namedtuple
import time
import sys

CalculationResults = namedtuple('CalculationResults', [
    'protein', 'fatacid', 'carbohydrates', 'price_100', 'price_1kg', 
    'isol', 'leit', 'val', 'met_tsist1', 'fenilalalin_tirosin1', 
    'tripto', 'lis', 'treon', 'isolecin2', 'leitsin2', 'valin2', 
    'met_tsist3', 'fenilalalin_tirosin3', 'triptofan2', 'lisin2', 
    'treonin2', 'isolecin_a', 'leitsin_a', 'valin_a', 'met_tsist_a', 
    'fenilalalin_tirosin_a', 'triptofan_a', 'lisin_a', 'treonin_a', 
    'Cmin', 'power_kkal', 'power_kDj', 'kras', 'bc', 'U', 'G', 'my_time',
    'chart_kras', 'chart_bc', 'chart_U', 'chart_G', 'ingredients', 'mass_fraction',
    'recip_name', 'counter', 'error_flag', 'error_message' 
])

def get_chemical_composition(ingredient):
    try:
        return Chemicals.objects.get(product=ingredient)
    except Chemicals.DoesNotExist:
        error_message = "Не удалось найти химический состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!"
        return(error_message)

def get_amino_acid_composition(ingredient):
    try:
        return AminoAcidComposition.objects.get(product=ingredient)
    except AminoAcidComposition.DoesNotExist:
        error_message = "Не удалось найти аминокислотный состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!"
        return(error_message)
    
def total_aminoacids(aminoacids_list, proteins, massfractions):
    total_values = []  # Для хранения числителей
    total_weights = []  # Для хранения знаменателей

    # Проход по каждому аминокислотному набору
    for aminoacids, protein, massfraction in zip(aminoacids_list, proteins, massfractions):
        # Рассчитать числитель для текущей группы
        total_values.append([value * protein * float(massfraction) for value in aminoacids])
        # Рассчитать знаменатель (вес) для текущей группы
        total_weights.append(protein * float(massfraction))

    # Суммирование по всем группам
    numerator = [sum(values) for values in zip(*total_values)]
    denominator = sum(total_weights)

    # Итоговое значение
    return [round(value / denominator, 3) if denominator != 0 else 0 for value in numerator]



def sum_aminoacids(aminoacids_list):
    sums = []

    for aminoacid in aminoacids_list:
        aminoacid_values = [0 if aminoacid[i] == 0 else round((aminoacid[i]), 3)
                            for i in range(len(aminoacid))]
        # Append aminoacid_values to sums for each amino acid
        sums.append(aminoacid_values)

    return [sum(values) for values in zip(*sums)]

def get_non_zero_sum(c_amino, c_min):
    return sum(value - c_min for value in c_amino if value != 0)

def get_non_zero_count(c_amino):
    return sum(1 for value in c_amino if value != 0)

def get_a_amino(c_min, c_amino):
    print(f"C_amino: {c_amino}")
    return [round((c_min / value), 3) if value != 0 else 0 for value in c_amino]

# def C_aminacids(aminacids_list):
#     essential_amino_acids = [4, 7, 5, 3, 6, 4, 1, 5]
#     c_aminacids = []

#     for aminoacid_values, essential_value in zip(aminacids_list, essential_amino_acids):
#         value = [round(((value * 100) / essential_value), 3) for value in aminoacid_values]
#         c_aminacids.append(value)

#     return c_aminacids

def C_aminacids(aminacids_list):
    essential_amino_acids = [4, 7, 5, 3.5, 6, 1, 4, 5.5]
    c_aminacids = []

    for aminoacid in aminacids_list:
        value = (aminoacid / essential_amino_acids[aminacids_list.index(aminoacid)] * 100)
        c_aminacids.append(value)
        
    return c_aminacids

def calculate_U(row_values, coefficients):
    """
    row_values: список списков, где каждая строка соответствует диапазону (например, J4:J12, K4:K12 и т.д.)
    coefficients: список коэффициентов (например, B22, C22, ... I22)
    """
    # Проверка на корректность входных данных
    if not row_values or not coefficients:
        raise ValueError("row_values и coefficients не могут быть пустыми.")

    if any(len(row) != len(coefficients) for row in row_values):
        raise ValueError("Длина каждого списка в row_values должна совпадать с длиной coefficients.")

    # Числитель: сумма произведений
    numerator = sum(sum(values) * coef for values, coef in zip(row_values, coefficients))

    # Знаменатель: общая сумма всех элементов
    denominator = sum(sum(values) for values in row_values)

    # Возврат результата с защитой от деления на 0
    return round(numerator / denominator, 3) if denominator != 0 else 0


def calculate_G(row_values, coefficients, denominator):
    """
    row_values: список списков, где каждая строка соответствует диапазону (например, K4:K12, L4:L12 и т.д.).
    coefficients: список коэффициентов (например, C22, D22, ..., J22).
    denominator: знаменатель (например, B23).
    """
    # Проверка входных данных
    if not row_values or not coefficients or len(row_values[0]) != len(coefficients):
        raise ValueError("Количество значений в строках row_values должно совпадать с количеством коэффициентов.")
    
    if denominator == 0:
        raise ValueError("Знаменатель не может быть равен нулю.")

    # Числитель: сумма произведений
    numerator = sum(sum(values[i] * (1 - coef) for i, coef in enumerate(coefficients)) for values in row_values)

    # Возвращаем результат
    return round(numerator / denominator, 3)

def process_recipe(recip_name, reg, ingredient, mass_fraction, price, size):
    start = time.time()

    aminoacids_list = []
    proteins_list = []
    fats_list = []
    carbohydrates_list = []

    error_flag = 0
    error_message = ""

    if recip_name != "" and reg != "" and ingredient and mass_fraction and price and size:

        empty_list = []
        for i in range(0, int(size)):
            chemical_composition = get_chemical_composition(ingredient[i])

            if chemical_composition != "Не удалось найти химический состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!":
                proteins_list.append(chemical_composition.protein if chemical_composition.protein != 0 else 0)  
                fats_list.append(chemical_composition.fat if chemical_composition.fat != 0 else 0)  
                carbohydrates_list.append(chemical_composition.carbohydrates if chemical_composition.carbohydrates != 0 else 0)   
            else:
                error_flag = 1
                error_message = chemical_composition
            # Добавляем проверку на ноль
            aminoacid_composition = get_amino_acid_composition(ingredient[i])   
            if aminoacid_composition != "Не удалось найти аминокислотный состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!":
                selected_amino_acids = aminoacid_composition.get_amino_acids_subset()   
                empty_list.extend((value / 1000 if value > 100 else value) for value in selected_amino_acids)

                aminoacids_list.append(empty_list)  # Перемещаем заполненный список аминокислот в основной список
                empty_list = []
            else:
                error_flag = 2
                error_message = aminoacid_composition

        total_amino = total_aminoacids(aminoacids_list, proteins_list, mass_fraction)   #M
        print("Total_amino:", total_amino)
        c_amino = C_aminacids(total_amino)  #C

        positive_values = [value for value in c_amino if value > 0]

        if positive_values:  
            c_min = min(positive_values)   
            a_amino = get_a_amino(c_min, c_amino)   

            kras = round(get_non_zero_sum(c_amino, c_min) / get_non_zero_count(c_amino), 3) if get_non_zero_count(c_amino) > 0 else 0
            
            bc = 100 - kras

            amino_sum = sum_aminoacids(aminoacids_list)
            
            u = calculate_U(aminoacids_list, a_amino)

            g = calculate_G(aminoacids_list, a_amino, c_min)

        else:
            c_min = 0
            a_amino = total_amino
            kras = 0
            bc = 0
            u = 0
            g = 0
            
        sum_mass_fraction = sum(float(fraction) for fraction in mass_fraction)
        
        if proteins_list:
            sum_prot = sum(proteins_list[i] * float(mass_fraction[i]) if float(mass_fraction[i]) != 0 else 0 for i in range(len(mass_fraction)))
            sum_fat = sum(fats_list[i] * float(mass_fraction[i]) if float(mass_fraction[i]) != 0 else 0 for i in range(len(mass_fraction)))
            sum_carbo = sum(carbohydrates_list[i] * float(mass_fraction[i]) if float(mass_fraction[i]) != 0 else 0 for i in range(len(mass_fraction)))
        else:
            sum_prot = 0
            sum_fat = 0
            sum_carbo = 0


        protein = sum_prot/sum_mass_fraction if sum_prot != 0 else 0
        fatacid = sum_fat/sum_mass_fraction if sum_fat != 0 else 0
        carbohydrates = sum_carbo/sum_mass_fraction if sum_carbo != 0 else 0

        power_kkal = protein * 4 + sum_fat/sum_mass_fraction * 9 + sum_carbo/sum_mass_fraction * 4 
        power_kDj = protein * 17 + sum_fat/sum_mass_fraction * 37 + sum_carbo/sum_mass_fraction * 4
        
        sum_price = sum((float(price[i]) * float(mass_fraction[i])) / 1000 for i in range(len(mass_fraction)))

        price_100 = (sum_price * 100) / sum_mass_fraction
        price_1kg = price_100 * 10

        stop = time.time()  

        execution_time = stop - start
        
        if total_amino:
            return CalculationResults(
                protein=round(protein, 3),
                fatacid=round(fatacid, 3),
                carbohydrates=round(carbohydrates, 3),
                price_100=round(price_100, 3),
                price_1kg=round(price_1kg, 3),

                isol=round(total_amino[0], 3),
                leit=round(total_amino[1], 3),
                val=round(total_amino[2], 3),
                met_tsist1=round(total_amino[3], 3),
                fenilalalin_tirosin1=round(total_amino[4], 3),
                tripto=round(total_amino[5], 3),
                lis=round(total_amino[7], 3),
                treon=round(total_amino[6], 3),

                isolecin2=round(c_amino[0], 3),
                leitsin2=round(c_amino[1], 3),
                valin2=round(c_amino[2], 3),
                met_tsist3=round(c_amino[3], 3),
                fenilalalin_tirosin3=round(c_amino[4], 3),
                triptofan2=round(c_amino[5], 3),
                lisin2=round(c_amino[7], 3),
                treonin2=round(c_amino[6], 3),

                isolecin_a=round(a_amino[0], 3),
                leitsin_a=round(a_amino[1], 3),
                valin_a=round(a_amino[2], 3),
                met_tsist_a=round(a_amino[3], 3),
                fenilalalin_tirosin_a=round(a_amino[4], 3),
                triptofan_a=round(a_amino[5], 3),
                lisin_a=round(a_amino[7], 3),
                treonin_a=round(a_amino[6], 3),

                Cmin=round(c_min, 3),
                power_kkal=round(power_kkal, 3),
                power_kDj=round(power_kDj, 3),
                kras=round(kras, 3),
                bc=round(bc, 3),
                U=round(u, 3),
                G=round(g, 3),
                my_time=round(execution_time, 4),
                chart_kras=str(round(kras, 3)),
                chart_bc=str(round(bc, 3)),
                chart_U=str(round(u, 3)),
                chart_G=str(round(g, 3)),
                ingredients=ingredient,
                mass_fraction=sum_mass_fraction,
                recip_name=recip_name,
                counter=str(size),
                error_flag = 0 if error_flag == 0 else error_message,
                error_message = None
            )
        else:
            return CalculationResults(
            protein=round(protein, 3),
            fatacid=round(fatacid, 3),
            carbohydrates=round(carbohydrates, 3),
            price_100=round(price_100, 3),
            price_1kg=round(price_1kg, 3),
            isol=0,
            leit=0,
            val=0,
            met_tsist1=0,
            fenilalalin_tirosin1=0,
            tripto=0,
            lis=0,
            treon=0,
            isolecin2=0,
            leitsin2=0,
            valin2=0,
            met_tsist3=0,
            fenilalalin_tirosin3=0,
            triptofan2=0,
            lisin2=0,
            treonin2=0,
            isolecin_a=0,
            leitsin_a=0,
            valin_a=0,
            met_tsist_a=0,
            fenilalalin_tirosin_a=0,
            triptofan_a=0,
            lisin_a=0,
            treonin_a=0,
            Cmin=0,
            power_kkal=0,
            power_kDj=0,
            kras=0,
            bc=0,
            U=0,
            G=0,
            my_time=round(execution_time, 4),
            chart_kras=str(0),
            chart_bc=str(0),
            chart_U=str(0),
            chart_G=str(0),
            ingredients=ingredient,
            mass_fraction=sum_mass_fraction,
            recip_name=recip_name,
            counter=str(size),
            error_flag = 0 if error_flag == 0 else error_message,
            error_message = error_message
        )
    else:
        error_message = "Fill in the fields!"
        return [error_message]

