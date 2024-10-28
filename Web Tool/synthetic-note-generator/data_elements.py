import datetime
from enum import Enum
from utils import get_feature_probabilities, format_date
from constants import problem_list, medication_list, surgery_list, allergy_list, race, ethnicity
from numpy import random
import names
import math
import numpy as np


class DateOffset(Enum):
    RANDOM = 'random'
    BEFORE = 'before'
    AFTER = 'after'


class CoresSide(Enum):
    RIGHT = 'right'
    LEFT = 'left'
    TOTAL = 'total'


class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'


class BaseClass:
    def __init__(self):
        self._text = None
        self._value = None

    def __str__(self):
        return self._text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class PSA:
    def __init__(self, base_date, days_offset=None, previous_score=None):
        super().__init__()
        if previous_score is None:
            self.psa_score = round(random.uniform(2, 20), 2)
        else:
            self.psa_score = round(previous_score * random.uniform(0.6, 1.1), 2)

        if days_offset is None:
            days_offset = random.randint(90, 365)
        self.psa_date = NoteDate(reference_date=base_date, offset_days=days_offset, direction=DateOffset.BEFORE)
        self.value = {'date': '', 'score': self.psa_score}


class Author(BaseClass):
    def __init__(self, create=True):
        super().__init__()
        if create:
            self._value = 'Dr. ' + names.get_last_name()
        else:
            self._value = None
        self._text = self._value


class Cores(BaseClass):
    def __init__(self, side=None, left_side=None, right_side=None):
        super().__init__()
        if side != CoresSide.LEFT and side != CoresSide.RIGHT and side != CoresSide.TOTAL:
            print(f'Error: side must be left or right, found {side}')
            exit(-1)
        if side == 'both':
            if left_side is None or right_side is None:
                print(f'Error: both left and right sides must be set')
                exit(-1)
            self.cores_per_side = left_side.core_per_side + right_side.core_per_side
            self.value = left_side.value + right_side.value
        else:
            self.cores_per_side = 6
            self.value = random.randint(0, self.cores_per_side)
        index = random.randint(0, 2)
        if index == 0:
            self.text = f'{self.value}/{self.cores_per_side} {side.value} cores positive'
        elif index == 1:
            self.text = f'{self.value} of {self.cores_per_side} {side.value} cores positive'
        else:
            self.text = f'{self.value} of {self.cores_per_side} {side.value} cores (+)'

class AUA(BaseClass):
    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.value = value  # Use provided value
        else:
            self.value = random.randint(0, 35)  # Randomize if no value is given

        index = random.randint(0, 2)
        if index == 0:
            self.text = f'AUA {self.value}'
        elif index == 1:
            self.text = f'AUA of {self.value}'
        else:
            self.text = f'AUA {self.value}/35'



class SHIM(BaseClass):
    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.value = value
        else:
            self.value = random.randint(1, 25)
        index = random.randint(0, 3)
        if index == 0:
            self.text = f'SHIM {self.value}'
        elif index == 1:
            self.text = f'SHIM of {self.value}'
        elif index == 2:
            self.text = f'SHIM score {self.value}/25'
        else:
            self.text = f'SHIM {self.value}/25'


class IPSS(BaseClass):
    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.value = value
        else:
            self.value = random.randint(0, 35)
        index = random.randint(0, 3)
        if index == 0:
            self.text = f'IPSS {self.value}'
        elif index == 1:
            self.text = f'IPSS of {self.value}'
        elif index == 2:
            self.text = f'IPSS score {self.value}/25'
        else:
            self.text = f'IPSS {self.value}/25'


class ECOG(BaseClass):
    def __init__(self, value=None):
        super().__init__()
        if value is not None:
            self.value = value
        else:
            self.value = random.randint(0, 4)

        index = random.randint(0, 2)
        if index == 0:
            self.text = f'ECOG {self.value}'
        elif index == 1:
            self.text = f'ECOG of {self.value}'
        else:
            self.text = f'ECOG {self.value}/5'


class PerformanceScore(BaseClass):
    def __init__(self):
        super().__init__()
        options = [70, 80, 90, 100]
        title = ['KPS', 'Karnofsky']
        self.value = int(random.choice(options))
        self.text = f'{random.choice(title)}: {self.value}'


class Prostatectomy(BaseClass):
    def __init__(self, patient_last_name=None):
        super().__init__()
        prostatectomy_date = NoteDate(reference_date=datetime.date(2020, 1, 1),
                                      offset_days=random.randint(90, 365), direction=DateOffset.BEFORE)
        self.value = prostatectomy_date.value
        if patient_last_name is None:
            index = random.randint(1, 4)
        else:
            index = random.randint(0, 4)
        prostatectomy_type = random.choice(['', 'radical ', 'robotic '])
        if index == 0:
            self.text = f' A {prostatectomy_type} prostatectomy was offered but was declined and Mr. ' \
                        f'{patient_last_name} elected for radiotherapy instead. '
            self.value = 'No'
        elif index == 1:
            self.text = f' A {prostatectomy_type}prostatectomy was performed on {prostatectomy_date.text}. '
            self.value = 'Yes'
        elif index == 2:
            self.text = f' Patient underwent {prostatectomy_type} prostatectomy on {prostatectomy_date.text}. '
            self.value = 'Yes'
        elif index == 3:
            self.text = f' {prostatectomy_date.text} he underwent a {prostatectomy_type} prostatectomy. '
            self.value = 'Yes'
        else:
            self.text = ''
            self.value = None


class Colonoscopy(BaseClass):
    def __init__(self):
        super().__init__()
        index = random.randint(0, 6)
        colonoscopy_date = NoteDate(reference_date=datetime.date(2020, 1, 1), offset_days=random.randint(90, 365),
                                    direction=DateOffset.BEFORE).value

        if index == 0:
            self.text = f'He has never had a colonoscopy.'
            self.value = False
        elif index == 1:
            self.text = f'Last colonoscopy was {colonoscopy_date} and was unremarkable except for ' \
                        f'internal hemorrhoids.'
            self.value = True
        elif index == 2:
            self.text = f'He last had colonoscopy on {colonoscopy_date}.'
            self.value = True
        elif index == 3:
            self.text = f'Had colonoscopy on {colonoscopy_date.month}/{colonoscopy_date.year} with polyps showing ' \
                        f'tubular adenoma.'
            self.value = True
        elif index == 4:
            self.text = f'Had colonoscopy in {colonoscopy_date.year - random.randint(1, 5)} (benign polyps). Repeat ' \
                        f'colonoscopy in {colonoscopy_date.year} also revealed {random.randint(1, 3)} benign polyps.'
            self.value = True
        elif index == 5:
            self.text = f'He had colonoscopy {random.randint(1, 12)} months ago, no polyps but has internal ' \
                        f'hemorrhoid, denies rectal pain/bleeding.'
            self.value = True
        else:
            print(f'Warning: Colonoscopy index {index} is out of range')


class BiopsyType(BaseClass):
    def __init__(self, title=None):
        super().__init__()
        biopsy_type = random.choice([None, 'transrectal', 'TRUS', 'mpMRI'])
        guided = str(random.choice([' ', '-guided ', ' guided ']))
        prostate = str(random.choice(['', 'prostate ']))
        postfix = guided + prostate + 'biopsy'

        if biopsy_type is None:
            text = 'biopsy'
        elif biopsy_type == 'transrectal':
            if title:
                text = biopsy_type.title() + postfix
            else:
                text = biopsy_type + postfix
        elif biopsy_type == 'TRUS':
            text = biopsy_type + postfix
        else:
            text = biopsy_type + postfix
        self.value = biopsy_type
        self.text = text


class Gleason:
    def __init__(self):
        self.primary = random.randint(3, 5)
        self.secondary = random.randint(3, 5)
        self.total = self.primary + self.secondary
        self.text = ''

        if random.randint(0, 1) == 0:
            self.text = 'Gleason score '
        else:
            self.text = 'GS '

        index = random.randint(0, 2)
        if index == 0:
            self.text += f'{self.primary}+{self.secondary}={self.primary + self.secondary}'
        elif index == 1:
            self.text += f'{self.primary + self.secondary}({self.primary}+{self.secondary})'
        else:
            self.text += f'{self.primary}+{self.secondary}'

    def __str__(self):
        return self.text


class Biopsy:
    def __init__(self, base_date):
        self.biopsy_type = BiopsyType()
        self.biopsy_date = NoteDate(reference_date=base_date, offset_days=random.randint(0, 180),
                                    direction=DateOffset.BEFORE)
        self.gleason = Gleason()
        self.left_cores = Cores(side=CoresSide.LEFT)
        self.right_cores = Cores(side=CoresSide.RIGHT)
        self.total_cores = Cores(side=CoresSide.TOTAL, left_side=self.left_cores, right_side=self.right_cores)
        self.value = {'biopsy_type': self.biopsy_type.value, 'biopsy_date': format_date(self.biopsy_date.value, 2),
                      'gleason': {'primary': self.gleason.primary, 'secondary': self.gleason.secondary,
                                  'total': self.gleason.total},
                      'left_cores': self.left_cores.value, 'right_cores': self.right_cores.value,
                      'total_cores': self.total_cores.value}


class TNM(BaseClass):
    def __init__(self):
        super().__init__()
        self.t = random.choice(['TX', 'T1', 'T1a', 'T1b' 'T1c', 'T2', 'T2a', 'T2b', 'T2c', 'T3', 'T3a', 'T3b', 'T4'])
        self.n = random.choice(['NX', 'N0', 'N1'])
        self.m = random.choice(['MX', 'M0', 'M1', 'M1a', 'M1b', 'M1c'])
        self.value = f'{self.t}{self.n}{self.m}'
        if random.choice(['True', 'False']):
            self.text = self.value
        else:
            self.text = f'{self.t} {self.n} {self.m}'


class Staging:
    def __init__(self):
        self.tnm = TNM()
        # TODO: update to match to AJCC rules
        self.group_stage = random.choice(['I', 'IIA', 'IIB', 'IIC', 'IIIA', 'IIIB', 'IIIC', 'IVA', 'IVB'])
        self.risk = random.choice(['low', 'intermediate', 'intermediate-favorable', 'intermediate-unfavorable', 'high',
                                   'very high'])
        self.histology = 'adenocarcinoma'
        self.value = {'tnm': self.tnm.value, 'group_stage': self.group_stage, 'risk': self.risk,
                      'histology': self.histology}


class Weight(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        options = ['Weight', 'Wt']
        self.value = random.randint(100, 300)
        if include_title:
            self.text = f'{random.choice(options)}: {self.value} lbs'
        else:
            self.text = f'{self.value} lbs'


class Temperature(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        options = ['Temperature', 'Temp']
        self.value = round(random.uniform(96, 101), 2)
        if include_title:
            self.text = f'{random.choice(options)}: {self.value} F'
        else:
            self.text = f'{self.value} F'


class BloodPressure(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        options = ['BP', 'B/P', 'Blood Pressure']
        diastolic = random.randint(60, 121)
        systolic = round(diastolic * random.uniform(1.5, 1.6))
        self.value = {'systolic': systolic, 'diastolic': diastolic}
        if include_title:
            self.text = f'{random.choice(options)}: {systolic}/{diastolic}'
        else:
            self.text = f'{systolic}/{diastolic}'


class Pulse(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        options = ['Pulse', 'HR', 'Heart Rate']
        self.value = random.randint(60, 120)
        if include_title:
            self.text = f'{random.choice(options)}: {self.value}'
        else:
            self.text = f'{self.value}'


class Respiration(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        title = ['Respiration', 'Resp']
        self.value = random.randint(12, 25)
        if include_title:
            self.text = f'{title}: {self.value}'
        else:
            self.text = f'{self.value}'


class Pain(BaseClass):
    def __init__(self, include_title=None):
        super().__init__()
        options = ['Pain', 'Pain Scale', 'Pain Score']
        self.value = random.randint(0, 6)
        if include_title:
            self.text = f'{random.choice(options)}: {self.value}'
        else:
            self.text = f'{self.value}'


class Vitals:
    def __init__(self):
        self.weight = Weight()
        self.temperature = Temperature()
        self.blood_pressure = BloodPressure()
        self.pulse = Pulse()
        self.respiration = Respiration()
        self.pain = Pain()

        text = ''
        format_index = random.randint(0, 2)
        if format_index == 0:
            indices = [x for x in range(0, 7)]
            random.shuffle(indices)
            for i in indices:
                if i == 0:
                    text += f'Temperature:\t{self.temperature}\n'
                elif i == 1:
                    text += f'Weight:\t{self.weight}\n'
                elif i == 2:
                    text += f'Blood Pressure:\t{self.blood_pressure}\n'
                elif i == 3:
                    text += f'Pulse:\t{self.pulse}\n'
                elif i == 4:
                    text += f'Respiration:\t{self.respiration}\n'
                elif i == 5:
                    text += f'Pain:\t{self.pain}\n'
        else:
            text += 'TEMP\tPULSE\tRESP\tBP\t\tPAIN\tWT\n'
            text += str(self.temperature) + '\t' + str(self.pulse) + '\t\t' + str(self.respiration) + '\t\t' + \
                    str(self.blood_pressure) + '\t' + str(self.pain) + '\t\t' + str(self.weight) + '\n'
        self.text = text
        self.value = {
            'weight': self.weight.value,
            'temperature': self.temperature.value,
            'blood_pressure': self.blood_pressure.value,
            'pulse': self.pulse.value,
            'respiration': self.respiration.value,
            'pain': self.pain.value
        }

    def __str__(self):
        return self.text


class ProblemList:
    def __init__(self):
        self.feature_probabilities = get_feature_probabilities()
        text = ''
        self.active_problems = []
        self.surgical_history = []
        if random.random() <= self.feature_probabilities['problem_list']:
            num_problems = int(random.normal(8, 2))
            num_surgeries = int(random.normal(2, 1))
            if num_problems <= 0:
                num_problems = 1
            if num_surgeries <= 0:
                num_surgeries = 0

            if num_problems >= len(problem_list):
                problems = random.choice(problem_list, len(problem_list), replace=False).tolist()
            else:
                problems = random.choice(problem_list, num_problems, replace=False).tolist()

            if num_problems >= len(surgery_list):
                surgeries = random.choice(surgery_list, len(surgery_list), replace=False).tolist()
            else:
                surgeries = random.choice(surgery_list, num_surgeries, replace=False).tolist()
            totals = np.concatenate((problems, surgeries), axis=0)
            random.shuffle(totals)

            if len(problems) > 0:
                self.active_problems = list(problems)
            if len(surgeries) > 0:
                self.surgical_history = list(surgeries)
            if len(surgeries) == 0:
                self.surgical_history = ["None"]

            titles = ['PAST MEDICAL AND SURGICAL HISTORY\n',
                      'PAST MEDICAL\nComputerized Problem List is the source of the following:\n',
                      'Past Medical/Surgical History:\n']
            text = '\n' + random.choice(titles)
            style = random.randint(0, len(titles))

            for index, problem in enumerate(totals):
                problem = str(problem)
                if style == 0:
                    text += problem
                    if index < len(problem) - 1:
                        text += ', '
                    else:
                        text += '\n'
                elif style == 1:
                    text += problem + '\n'
                else:
                    text += str(index + 1) + ': ' + problem + '\n'
        self.text = text
        self.value = {'surgical_history': self.surgical_history, 'active_problems': self.active_problems}

    def __str__(self):
        return self.text


class Imaging(BaseClass):
    def __init__(self, image_type=None, base_date=None):
        super().__init__()
        self.feature_probabilities = get_feature_probabilities()
        self.text = ''
        self.image_type = image_type
        self.value = NoteDate(reference_date=base_date, direction=DateOffset.BEFORE, offset_days=random.randint(10, 300)).value
        if self.image_type == 'pelvic_ct':
            self.text = f'CT abdomen and pelvis on {self.value}: No evidence of metastatic disease in the abdomen or pelvis\n'
        elif self.image_type == 'pelvic_mri':
            self.text = f'MRI abdomen and pelvis on {self.value}: No evidence of metastatic disease in the abdomen or pelvis\n'
        elif self.image_type == 'bone_scan':
            self.text = f'Bone scan on {self.value}: No evidence for skeletal metastatic involvement is noted at this time.\n'


class Medications(BaseClass):
    def __init__(self):
        super().__init__()
        feature_probabilities = get_feature_probabilities()
        self.value = None
        self.text = ''
        if random.random() <= feature_probabilities['medication_list']:
            text = '\n'
            mode = random.randint(0, 2)
            if mode == 0:
                text += '\t\tActive Outpatient Medications\t\t\t\tStatus\n'
                text += '==================================================================\n'
            elif mode == 1:
                text += 'Active Outpatient Medications\n'
            else:
                text += 'Meds:\n'

            num_meds = int(random.normal(5, 3))
            if num_meds < 0:
                num_meds = 0
            if num_meds < 8:
                num_meds = 8
            is_numbered = random.choice([True, False])
            ordered_meds = random.choice(medication_list, num_meds, replace=False)

            for index, medication in enumerate(ordered_meds):
                if is_numbered:
                    text += str(index + 1) + ')\t'
                text += medication
                if mode == 0:
                    text += '\t\t\t\tACTIVE\n'
                else:
                    text += '\n'
            self.text = text
            self.value = list(ordered_meds)


class Allergies(BaseClass):
    def __init__(self):
        super().__init__()
        feature_probabilities = get_feature_probabilities()
        self.value = None
        self.text = ''
        text = '\nAllergies: '
        if random.random() <= feature_probabilities['allergies_list']:
            count = int(random.normal(2.0, 2.0))
            if count < 1:
                count = 1
            allergies = random.choice(allergy_list, count, replace=False)
            if count > 1:
                for index, allergy in enumerate(allergies):
                    text += allergy
                    if index < count - 1:
                        text += ', '
            else:
                text += allergies[0]
            self.value = list(allergies)
        else:
            index = random.randint(0, 2)
            if index == 0:
                text += 'NKA'
            elif index == 1:
                text += 'None'
            else:
                text += ''
        text += '\n'
        self.text = text


def alcohol_former_current(current_drinker):
    index = random.randint(0, 2)
    stopped_index = random.randint(0, 2)
    if stopped_index == 0:
        stopped_text = ', has since quit'
    else:
        stopped_text = f', stopped drinking {random.randint(1, 30)} years ago'

    if index == 0:
        # social drinker
        if not current_drinker:
            text = 'former social drinker' + stopped_text
        else:
            text = 'drinks socially'
    elif index == 1:
        # drinks 1-10 beers week
        min_drinks = random.randint(0, 5)
        max_drinks = min_drinks + random.randint(1, 5)
        if not current_drinker:
            text = f'used to drink {min_drinks}-{max_drinks} beers per week{stopped_text}'
        else:
            text = f'currently drinks {min_drinks}-{max_drinks} beers per week'
    else:
        # heavy drinker
        if not current_drinker:
            text = 'h/o heavy drinking' + stopped_text
        else:
            text = 'h/o heavy drinking'
    return text


class AlcoholHistory:
    def __init__(self):
        feature_probabilities = get_feature_probabilities()
        self.value = random.choice([None, 'never', 'former', 'current'], p=feature_probabilities['alcohol_status'])
        alcohol_list_never_options = ['denies alcohol use', 'No h/o alcohol use', 'No']
        text = ''
        if self.value == 'never':
            text = alcohol_list_never_options[random.randint(0, 1)] + '. '
            self.value = 'never'
        elif self.value == 'former':
            text = alcohol_former_current(current_drinker=False) + '. '
            self.value = 'former'
        elif self.value == 'current':
            text = alcohol_former_current(current_drinker=True) + '. '
            self.value = 'current'
        self.text = text

    def __str__(self):
        return self.text


class SmokingHistory:
    def __init__(self, reference_date):
        feature_probabilities = get_feature_probabilities()
        self.reference_date = reference_date
        self.smoking_status = None
        self.years_smoked = None
        self.packs_per_year = None
        self.years_ago_stopped = None
        text = ''
        use_status = [None, 'never', 'former', 'current']
        smoking_status = random.choice(use_status, p=feature_probabilities['smoking_status'])
        tobacco_list_never_options = ['denies tobacco use', 'No h/o tobacco use', 'No']

        if smoking_status == 'never':
            text = tobacco_list_never_options[random.randint(0, 1)] + '. '
            self.smoking_status = 'never'
        elif smoking_status == 'former':
            text = self.tobacco_former_current(current_smoker=False) + '. '
            self.smoking_status = 'former'
        elif smoking_status == 'current':
            text = self.tobacco_former_current(current_smoker=True) + '. '
            self.smoking_status = 'current'
        self.text = text
        self.value = {'smoking_status': self.smoking_status, 'years_smoked': self.years_smoked,
                      'packs_per_year': self.packs_per_year, 'years_ago_stopped': self.years_ago_stopped}

    def __str__(self):
        return self.text

    def tobacco_former_current(self, current_smoker=False):
        text = ''
        self.years_smoked = random.randint(10, 60)  # TODO: base this on age
        self.packs_per_year = random.randint(10, 100)
        self.years_ago_stopped = random.randint(1, 25)

        former = not current_smoker
        index = random.randint(0, 4)
        if index == 0:
            if former:
                text += f'Former smoker of 1ppd x {self.years_smoked} for years'
            else:
                text += f'1ppd x {self.years_smoked} years'
        elif index == 1:
            if former:
                text += f'Former smoked, 1ppd x {self.years_smoked} years, stopped smoking {self.years_ago_stopped} years ago'
            else:
                text += f'Currently smoking, 1ppd x {self.years_smoked} years'
        elif index == 2:
            if former:
                text += f'Smoked a half pack a day for {self.years_smoked} years, since quit'
            else:
                text += f'Smoking a half pack a day for {self.years_smoked} years'
        elif index == 3:
            if former:
                text += f'h/o {self.packs_per_year} packs per year, has smoked for approximately {self.years_smoked} years. Quit {self.years_ago_stopped} years ago'
            else:
                text += f'{self.packs_per_year} packs per year, has smoked for approximately {self.years_smoked} years'
        elif index == 4:
            min_packs = random.randint(10, 100)
            max_packs = min_packs + random.randint(5, 100)
            if former:
                text += f'Former smoker with {min_packs}-{max_packs} pack per year history, quit  {self.reference_date.year - self.years_ago_stopped}'
            else:
                text += f'Current smoker with {min_packs}-{max_packs} pack per year history'
        else:
            if former:
                text += 'former smoker'
            else:
                text += 'h/o smoking'
        return text


class SocialHistory:
    def __init__(self, reference_date):
        self.smoking_history = SmokingHistory(reference_date=reference_date)
        self.alcohol_history = AlcoholHistory()
        titles = ['SOCIAL HX:', 'Social History:', 'SOCIAL HISTORY:']
        text = '\n' + random.choice(titles) + '\n'
        sh_list = random.choice([True, False])

        sh_list_formats = [{'alcohol': 'Alcohol Use: ', 'tobacco': 'Tobacco Use: '},
                           {'alcohol': 'Alcohol use: ', 'tobacco': 'Tobacco use: '},
                           {'alcohol': 'alcohol: ', 'tobacco': 'tobacco: '},
                           {'alcohol': 'Alcohol Use Status: ', 'tobacco': 'Tobacco Use Status: '}]

        if sh_list:
            list_index = random.randint(0, len(sh_list_formats) - 1)
            text += sh_list_formats[list_index]['tobacco']
            text += str(self.smoking_history)
            text += '\n'
            text += sh_list_formats[list_index]['alcohol']
            text += str(self.alcohol_history)
            text += '\n'
        else:
            text += str(self.smoking_history)
            text += str(self.alcohol_history)
            text += '\n'
        self.text = text
        self.value = {'smoking_history': self.smoking_history.value, 'alcohol_history': self.alcohol_history.value}

    def __str__(self):
        return self.text


class FamilyHistory(BaseClass):
    def __init__(self):
        super().__init__()
        self.value = None
        male_members = ['father', 'uncle', 'brother', 'grandfather']
        female_members = ['mother', 'aunt', 'sister', 'grandmother']
        cancers = ['esophageal', 'rectum', 'brain', 'head and neck', 'lung']
        male_cancers = cancers + ['prostate', 'testicular']
        female_cancers = cancers + ['breast', 'ovarian']
        label = random.choice(['ca', 'cancer'])
        titles = ['FAMILY HISTORY', 'Family History', 'Family Hx']
        text = '\n' + random.choice(titles) + ':\n'
        num_family_members = random.randint(0, 3)
        if num_family_members == 0:
            text += 'No family history of cancer'
            self.value = False
        else:
            for index in range(0, num_family_members):
                is_male = random.choice([True, False])
                if is_male:
                    current_member = random.choice(male_members)
                    current_cancer = random.choice(cancers + male_cancers)
                else:
                    current_member = random.choice(female_members)
                    current_cancer = random.choice(cancers + female_cancers)

                text += current_member + ' had ' + current_cancer + ' ' + label
                if index < num_family_members - 1:
                    text += ', '
            self.value = True
        self.text = text


class PriorTreatment:
    def __init__(self, reference_date):
        self.prior_rt = None
        self.prior_rt_date = NoteDate(reference_date=reference_date, offset_days=random.randint(365, 3650),
                                      direction=DateOffset.BEFORE)
        self.chemotherapy_prescribed = None
        self.chemotherapy_drugs_prescribed = None
        self.chemotherapy_date = NoteDate(reference_date=reference_date, offset_days=random.randint(365, 3650),
                                          direction=DateOffset.BEFORE)
        self.hormone_therapy_prescribed = None
        self.hormone_therapy_date = NoteDate(reference_date=reference_date, offset_days=random.randint(365, 3650),
                                             direction=DateOffset.BEFORE)
        hormone_drugs = ['', 'Eligard', 'Lupron']
        chemo_drugs = ['', 'Docetaxel', 'Cabazitaxel', 'Mitoxantrone', 'Estramustine']
        text = '\n\n' + random.choice(['CANCER TREATMENT HISTORY:', 'Cancer Treatments:'])
        text += '\n'
        rad_choice = random.choice(['', 'Yes', 'No'])
        text += 'Radiation: '
        if rad_choice == 'Yes':
            text += f'Yes, {self.prior_rt_date}' + '\n'
            self.previous_rt = True
        elif rad_choice == 'No':
            text += 'No\n'
            self.previous_rt = False
        else:
            text += '\n'
        text += 'Chemotherapy: '
        chemo_choice = random.choice(['', 'Yes', 'No'])
        if chemo_choice == 'Yes':
            chemo_drug = random.choice(chemo_drugs)
            text += f'Yes, {self.chemotherapy_date}' + f' {chemo_drug}\n'
            self.chemotherapy_prescribed = True
            self.chemotherapy_drugs_prescribed = chemo_drug
        elif chemo_choice == 'No':
            text += 'No\n'
            self.chemotherapy_prescribed = False
        else:
            text += '\n'
        text += 'Hormone Therapy: '
        hormone_choice = random.choice(['', 'Yes', 'No'])
        if hormone_choice == 'Yes':
            hormone_drug = random.choice(hormone_drugs)
            text += random.choice(
                ['', f'Yes, {self.hormone_therapy_date}']) + f' {hormone_drug}\n'
            self.hormone_therapy_prescribed = True
        elif hormone_choice == 'No':
            text += 'No\n'
            self.hormone_therapy_prescribed = False
        else:
            text += '\n'
        self.text = text
        self.value = {'prior_rt': self.prior_rt, 'prior_rt_date': format_date(self.prior_rt_date.value, date_format=2),
                      'chemotherapy_prescribed': self.chemotherapy_prescribed,
                      'chemotherapy_drugs_prescribed': self.chemotherapy_drugs_prescribed,
                      'hormone_therapy_prescribed': self.hormone_therapy_prescribed}

    def __str__(self):
        return self.text


class Dose:
    def __init__(self):
        self.dose_per_fraction = 180
        self.num_fractions = random.randint(36, 44)
        self.total_dose = self.num_fractions * self.dose_per_fraction
        self.weeks_of_rt = int(math.ceil(self.num_fractions / 5.))
        self.value = {'dose_per_fraction': self.dose_per_fraction, 'num_fractions': self.num_fractions,
                      'total_dose': self.total_dose, 'weeks_of_rt': self.weeks_of_rt}


class Patient:
    def __init__(self, reference_date=datetime.datetime.now()):
        self.sex = Sex.MALE
        self.race = random.choice(race)
        self.ethnicity = random.choice(ethnicity)
        self.first_name = names.get_first_name(gender=self.sex)
        self.last_name = names.get_last_name()
        date_of_birth = datetime.date(random.randint(1940, 1980), random.randint(1, 12), random.randint(1, 28))
        self.age = reference_date.year - date_of_birth.year - ((reference_date.month, reference_date.day) < (
            date_of_birth.month, date_of_birth.day))
        self.date_of_birth = NoteDate(reference_date=date_of_birth)
        self.value = {'sex': self.sex.value, 'race': self.race, 'ethnicity': self.ethnicity,
                      'first_name': self.first_name, 'last_name': self.last_name,
                      'date_of_birth': format_date(self.date_of_birth.value, date_format=2), 'age': self.age}


class NoteDate(BaseClass):
    def __init__(self, reference_date=datetime.date(2020, 1, 1), offset_days=None, direction: DateOffset = None,
                 date_format=None):
        super().__init__()

        if offset_days is not None and direction is not None:
            if direction == DateOffset.RANDOM:
                direction = random.choice([DateOffset.BEFORE, DateOffset.AFTER])
            if direction == DateOffset.BEFORE:
                self._value = reference_date - datetime.timedelta(days=offset_days)
            elif direction == DateOffset.AFTER:
                self._value = reference_date + datetime.timedelta(days=offset_days)
        else:
            if offset_days is None and direction is not None:
                print(f'Warning: offset_days is None but direction is set, defaulting to reference date')
            elif offset_days is not None and direction is None:
                print(f'Warning: direction is None but offset_days is set, defaulting to reference date')
            self._value = reference_date
        self.year = self._value.year
        self.month = self._value.month
        self.day = self._value.day
        self._text = format_date(self._value, date_format=date_format)
