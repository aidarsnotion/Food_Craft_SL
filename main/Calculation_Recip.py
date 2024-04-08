from main.models import *
from collections import namedtuple
import time
import sys

#API reset password
#API product detail 
#API login with API key


AminoAcids = namedtuple('AminoAcids', [
    'isol', 'leit', 'val', 'met_tsist', 
    'fenilalalin_tirosin', 'tripto', 'lis', 'treon'
])

AminoAcidsSum = namedtuple('AminoAcidsTotal', [
    'isol', 'leit', 'val', 'met_tsist', 
    'fenilalalin_tirosin', 'tripto', 'lis', 'treon'
])

AminoAcidsTotal = namedtuple('AminoAcidsTotal', [
    'isol', 'leit', 'val', 'met_tsist', 
    'fenilalalin_tirosin', 'tripto', 'lis', 'treon'
])


AminoAcids_SCOR = namedtuple('AminoAcidsTotal', [
    'isol', 'leit', 'val', 'met_tsist', 
    'fenilalalin_tirosin', 'tripto', 'lis', 'treon'
])

AminoAcids_utility = namedtuple('AminoAcidsTotal', [
    'isol', 'leit', 'val', 'met_tsist', 
    'fenilalalin_tirosin', 'tripto', 'lis', 'treon'
])

CalculationResults = namedtuple('CalculationResults', [
    'protein', 'fatacid', 'carbohydrates', 'price_100', 'price_1kg', 
    'isol', 'leit', 'val', 'met_tsist1', 'fenilalalin_tirosin1', 
    'tripto', 'lis', 'treon', 'isolecin2', 'leitsin2', 'valin2', 
    'met_tsist3', 'fenilalalin_tirosin3', 'triptofan2', 'lisin2', 
    'treonin2', 'isolecin_a', 'leitsin_a', 'valin_a', 'met_tsist_a', 
    'fenilalalin_tirosin_a', 'triptofan_a', 'lisin_a', 'treonin_a', 
    'Cmin', 'power_kkal', 'power_kDj', 'kras', 'bc', 'U', 'G', 'my_time',
    'chart_kras', 'chart_bc', 'chart_U', 'chart_G', 'ingredients', 'mass_fraction',
    'recip_name', 'counter' 
])


def get_chemical_composition(ingredient):
    try:
        return Chemicals.objects.get(product=ingredient)
    except Chemicals.DoesNotExist:
        error_message = "Не удалось найти химический состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!"
        raise ValueError(error_message)

def get_amino_acid_composition(ingredient):
    try:
        return AminoAcidComposition.objects.get(product=ingredient)
    except AminoAcidComposition.DoesNotExist:
        error_message = "Не удалось найти аминокислотный состав ингредиентов, сообщите администратору об ошибке и дождитесь исправления!"
        raise ValueError(error_message)

def calculate_ingredient_chemical_composition(chemical_comp, mass):
    chemicals_prot = chemical_comp.protein
    chemicals_fat = chemical_comp.fat
    chemicals_carbo = chemical_comp.carbohydrates

    prot = mass * chemicals_prot
    fat = mass * chemicals_fat
    carbo = mass * chemicals_carbo

    return prot, fat, carbo

def get_aminoacids_sum(aminoacids_list):
    """
    Рассчитывает суммарную массовую долю аминокислот.
    """
    print(aminoacids_list)
    isol_total = sum(amino.isol for amino in aminoacids_list)
    leit_total = sum(amino.leit for amino in aminoacids_list)
    val_total = sum(amino.val for amino in aminoacids_list)
    met_tsist_total = sum(amino.met_tsist for amino in aminoacids_list)
    fen_tir_total = sum(amino.fenilalalin_tirosin for amino in aminoacids_list)
    tripto_total = sum(amino.tripto for amino in aminoacids_list)
    lis_total = sum(amino.lis for amino in aminoacids_list)
    treon_total = sum(amino.treon for amino in aminoacids_list)
    
    return AminoAcidsSum(
        isol=isol_total,
        leit=leit_total,
        val=val_total,
        met_tsist=met_tsist_total,
        fenilalalin_tirosin=fen_tir_total,
        tripto=tripto_total,
        lis=lis_total,
        treon=treon_total
    )


def get_aminoacids_composition(aminocaid_comp, mass, chemicals_prot):
    amino_isoleicin = ((aminocaid_comp.izoleitsin / 100) * mass) / chemicals_prot
    amino_leitsin = (aminocaid_comp.leitsin / 100) * mass / chemicals_prot
    amino_valin = (aminocaid_comp.valin / 100) * mass / chemicals_prot
    met_tsist = (aminocaid_comp.metionin / 100) + (aminocaid_comp.tsistein / 1000) * mass / chemicals_prot
    fenilanin_tirosin = (aminocaid_comp.fenilalalin / 100) + (aminocaid_comp.tirosin / 1000) * mass / chemicals_prot
    amino_triptofan = (aminocaid_comp.triptofan / 100) * mass / chemicals_prot
    amino_lisin = (aminocaid_comp.lisin / 100) * mass / chemicals_prot
    amino_treonin = (aminocaid_comp.treonin / 100) * mass / chemicals_prot


    return AminoAcids(
        isol=amino_isoleicin,
        leit=amino_leitsin,
        val=amino_valin,
        met_tsist=met_tsist,
        fenilalalin_tirosin=fenilanin_tirosin,
        tripto=amino_triptofan,
        lis=amino_lisin,
        treon=amino_treonin
    )

def get_total_aminoacids(aminoacids, total_mass_prot):
    """
    Рассчитывает суммарную массовую долю аминокислот.
    """
    isol = aminoacids.isol / total_mass_prot
    leit = aminoacids.leit / total_mass_prot
    val = aminoacids.val / total_mass_prot
    met_tsist = aminoacids.met_tsist / total_mass_prot
    fenilalalin_tirosin = aminoacids.fenilalalin_tirosin / total_mass_prot
    tripto = aminoacids.tripto / total_mass_prot
    lis = aminoacids.lis / total_mass_prot
    treon = aminoacids.treon / total_mass_prot
    
    return AminoAcidsTotal(
        isol=isol,
        leit=leit,
        val=val,
        met_tsist=met_tsist,
        fenilalalin_tirosin=fenilalalin_tirosin,
        tripto=tripto,
        lis=lis,
        treon=treon
    )

def calculate_aminoacid_scores(aminoacids_total):
    """
    Рассчитывает аминокислотные скоры на основе объекта aminoacids_total.
    """
    isolecin = (aminoacids_total.isol / 4) * 100
    leitsin = (aminoacids_total.leit / 7) * 100
    valin = (aminoacids_total.val / 5) * 100
    met_tsist = (aminoacids_total.met_tsist / 3.5) * 100
    fenilalalin_tirosin = (aminoacids_total.fenilalalin_tirosin / 6) * 100
    triptofan = (aminoacids_total.tripto / 1) * 100
    lisin = (aminoacids_total.lis / 5.5) * 100
    treonin = (aminoacids_total.treon / 4) * 100
    
    return AminoAcids_SCOR(
        isol=isolecin,
        leit=leitsin,
        val=valin,
        met_tsist=met_tsist,
        fenilalalin_tirosin=fenilalalin_tirosin,
        tripto=triptofan,
        lis=lisin,
        treon=treonin
    )

def calculate_aminoacid_utility(Cmin, aminoacid_scores):
    """
    Рассчитывает значения утилитарных коэффициентов на основе Cmin и значений аминокислотных скоров.
    """
    isolecin = Cmin / aminoacid_scores.isol if aminoacid_scores.isol > 0 else 0
    leitsin = Cmin / aminoacid_scores.leit if aminoacid_scores.leit > 0 else 0
    valin = Cmin / aminoacid_scores.val if aminoacid_scores.val > 0 else 0
    met_tsist = Cmin / aminoacid_scores.met_tsist if aminoacid_scores.met_tsist > 0 else 0
    fenilalalin_tirosin = Cmin / aminoacid_scores.fenilalalin_tirosin if aminoacid_scores.fenilalalin_tirosin > 0 else 0
    triptofan = Cmin / aminoacid_scores.tripto if aminoacid_scores.tripto > 0 else 0
    lisin = Cmin / aminoacid_scores.lis if aminoacid_scores.lis > 0 else 0
    treonin = Cmin / aminoacid_scores.treon if aminoacid_scores.treon > 0 else 0
    
    return AminoAcids_utility(
        isol=isolecin,
        leit=leitsin,
        val=valin,
        met_tsist=met_tsist,
        fenilalalin_tirosin=fenilalalin_tirosin,
        tripto=triptofan,
        lis=lisin,
        treon=treonin
    )



def process_recipe(recip_name, reg, ingredient, mass_fraction, price, size):
    aminoacids_list = []
    start = time.time()

    if recip_name != "" and reg != "" and ingredient and mass_fraction and price and size:
        prot = fat = carbo = prplus = 0
        mass_fractions = total_mass_prot = Cmin = kras = bc = U = G = 0

        for i in range(0, int(size)):
            amino_acid_comp = None
            try:
                ing = ingredient[i]
                chemical_comp = get_chemical_composition(ing)
                chemicals_prot = chemical_comp.protein
                if chemicals_prot:
                    amino_acid_comp = get_amino_acid_composition(ing)
                mass = float(mass_fraction[i])

                

                # Расчет параметров ингредиента
                prot_i, fat_i, carbo_i = calculate_ingredient_chemical_composition(chemical_comp, mass)
                if amino_acid_comp:
                    aminoacids_list.append(get_aminoacids_composition(amino_acid_comp, mass, chemicals_prot))

                if amino_acid_comp:
                    total_mass_prot += (float(mass) * chemicals_prot)

                pr_i = (float(price[i]) * mass) / 1000

                # Обновление суммарных значений
                prot += prot_i
                fat += fat_i
                carbo += carbo_i

                prplus += pr_i

                mass_fractions += mass

            except (ValueError, Chemicals.DoesNotExist, AminoAcidComposition.DoesNotExist) as e:
                return [str(e)]
            
        aminoacids_sum = get_aminoacids_sum(aminoacids_list)
        aminoacids_total = get_total_aminoacids(aminoacids_sum, total_mass_prot)
        aminoacids_scor = calculate_aminoacid_scores(aminoacids_total) 
        values = [aminoacids_total.isol, aminoacids_total.leit, aminoacids_total.val, aminoacids_total.met_tsist, aminoacids_total.fenilalalin_tirosin, aminoacids_total.tripto, aminoacids_total.lis, aminoacids_total.treon]

        # Избавляемся от нулей
        values = [value for value in values if value > 0]

        # Если все значения нулевые, используем sys.maxsize
        if not values:
            Cmin = sys.maxsize
        else:
            # Находим минимальное значение
            Cmin = min(values)       
        # Cmin = min(aminoacids_total.isol, aminoacids_total.leit, aminoacids_total.val, aminoacids_total.met_tsist, aminoacids_total.fenilalalin_tirosin, aminoacids_total.tripto, aminoacids_total.lis, aminoacids_total.treon)

        aminoacids_util = calculate_aminoacid_utility(Cmin, aminoacids_scor)

        # Расчет параметров рецептуры
        protein = prot / mass_fractions
        fatacid = fat / 100
        carbohydrates = carbo / 100
        price_100 = (prplus * 100) / mass_fractions
        price_1kg = price_100 * 10

        #Сумманая масса незаменимых аминокислот
        sum_M = aminoacids_total.isol * (1 - aminoacids_util.isol) + aminoacids_total.leit * (1 - aminoacids_util.leit) + aminoacids_total.val * (1 - aminoacids_util.val) + (aminoacids_total.met_tsist * (1 - aminoacids_util.met_tsist)) + aminoacids_total.fenilalalin_tirosin * (1 - aminoacids_util.fenilalalin_tirosin) + aminoacids_total.tripto * (1 - aminoacids_util.tripto) + aminoacids_total.treon * (1 - aminoacids_util.treon) + aminoacids_total.lis * (1 - aminoacids_util.lis)
        #Коэффициент КРАС - Средняя величина избытка аминакислотного скора
        kras = (aminoacids_scor.isol - Cmin + aminoacids_scor.leit - Cmin + aminoacids_scor.val - Cmin + aminoacids_scor.met_tsist - Cmin + aminoacids_scor.fenilalalin_tirosin - Cmin + aminoacids_scor.tripto - Cmin + aminoacids_scor.lis - Cmin + aminoacids_scor.treon - Cmin) / 8
        #Биологическая ценность пищевого белка
        bc = 100 - kras
        #Коэффициент утилитарности 
        U = (aminoacids_util.isol * aminoacids_total.isol + aminoacids_util.leit * aminoacids_total.leit + aminoacids_util.val * aminoacids_total.val + aminoacids_util.met_tsist * aminoacids_total.met_tsist + aminoacids_util.fenilalalin_tirosin * aminoacids_total.fenilalalin_tirosin + aminoacids_util.tripto * aminoacids_total.tripto + aminoacids_util.treon * aminoacids_total.treon + aminoacids_util.lis * aminoacids_total.lis)/(aminoacids_total.isol + aminoacids_total.leit + aminoacids_total.val + aminoacids_total.met_tsist + aminoacids_total.fenilalalin_tirosin + aminoacids_total.tripto + aminoacids_total.treon + aminoacids_total.lis)
        #Коэффициент сопоставимой избыточности
        
        G = sum_M/(Cmin/100)

        #Каллорийность в Ккал
        power_kkal = protein * 4 + fatacid * 9 + carbohydrates * 4
        #Каллорийность в кДж
        power_kDj = protein * 17 + fatacid * 37 + carbohydrates * 4

        stop = time.time()  

        execution_time = stop - start

        return CalculationResults(
            protein=round(protein, 3),
            fatacid=round(fatacid, 3),
            carbohydrates=round(carbohydrates, 3),
            price_100=round(price_100, 3),
            price_1kg=round(price_1kg, 3),
            isol=round(aminoacids_total.isol, 3),
            leit=round(aminoacids_total.leit, 3),
            val=round(aminoacids_total.val, 3),
            met_tsist1=round(aminoacids_total.met_tsist, 3),
            fenilalalin_tirosin1=round(aminoacids_total.fenilalalin_tirosin, 3),
            tripto=round(aminoacids_total.tripto, 3),
            lis=round(aminoacids_total.lis, 3),
            treon=round(aminoacids_total.treon, 3),
            isolecin2=round(aminoacids_scor.isol, 3),
            leitsin2=round(aminoacids_scor.leit, 3),
            valin2=round(aminoacids_scor.val, 3),
            met_tsist3=round(aminoacids_scor.met_tsist, 3),
            fenilalalin_tirosin3=round(aminoacids_scor.fenilalalin_tirosin, 3),
            triptofan2=round(aminoacids_scor.tripto, 3),
            lisin2=round(aminoacids_scor.lis, 3),
            treonin2=round(aminoacids_scor.treon, 3),
            isolecin_a=round(aminoacids_util.isol, 3),
            leitsin_a=round(aminoacids_util.leit, 3),
            valin_a=round(aminoacids_util.val, 3),
            met_tsist_a=round(aminoacids_util.met_tsist, 3),
            fenilalalin_tirosin_a=round(aminoacids_util.fenilalalin_tirosin, 3),
            triptofan_a=round(aminoacids_util.tripto, 3),
            lisin_a=round(aminoacids_util.lis, 3),
            treonin_a=round(aminoacids_util.treon, 3),
            Cmin=round(Cmin, 3),
            power_kkal=round(power_kkal, 3),
            power_kDj=round(power_kDj, 3),
            kras=round(kras, 3),
            bc=round(bc, 3),
            U=round(U, 3),
            G=round(G, 3),
            my_time=round(execution_time, 4),
            chart_kras=str(round(kras, 3)),
            chart_bc=str(round(bc, 3)),
            chart_U=str(round(U, 3)),
            chart_G=str(round(G, 3)),
            ingredients=ingredient,
            mass_fraction=mass_fractions,
            recip_name=recip_name,
            counter=str(size),
        )

    else:
        error_message = "Fill in the fields!"
        return [error_message]