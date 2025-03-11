import random
import pandas as pd
from deap import base, creator, tools

COURSES = {
    "GE104": 3, "HS101": 3, "MA102": 3, "GE102": 3, "NO102": 2,
    "CY101": 3, "GE103": 3, "GE105": 3, "ME101": 3,
}

TEACHERS = {
    "GE104": "DR. K.R SHEKAR", "HS101": "DR. KAMAL", "MA102": "DR. TAPAS",
    "GE102": "DR. DHIRAJ K MAHAJAN", "NO102": "DR. TV KALYAN", "GE105": "Dr. Devranjan",
    "CY101": "Dr. Sudipta Kumar Sinha", "GE103":"Dr. Sukrit Gupta","ME101":"Satwinder Jit Singh"
}

ROOMS = {
    "M1": 50, "M2": 50, "M3": 100, "M4": 100, "M5": 195, "M6": 180,
    "CS1": 60, "CS2": 40, "CS(SH)": 90, "EE1": 65, "EE2": 35, "EE3": 60,
    "EE(SH)": 80, "ME1": 70, "ME2": 35, "ME(SH)": 90, "CY(SH)": 90,
    "CY1": 35, "CY2": 30
}

LABS = {"ENG_DRAW_LAB": "Engineering Drawing Lab"}
ROOM_LIST = list(ROOMS.keys())
NO102_LOCATION = "C Sports Ground"
TIME_SLOTS = [
    "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM",
    "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM"
]
DAYS = ["Monday", "Tuesday", "Wednesday"]

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()

def create_individual():
    schedule = {}
    for course, slots in COURSES.items():
        fixed_time = random.choice(TIME_SLOTS[8:] if course == "NO102" else TIME_SLOTS[:8])
        fixed_room = (
            NO102_LOCATION if course == "NO102" else
            "ENG_DRAW_LAB" if course == "GE105" else
            random.choice(ROOM_LIST)
        )
        fixed_days = random.sample(DAYS, slots)
        for day in fixed_days:
            schedule[(course, day)] = (fixed_time, fixed_room)
    return list(schedule.items())

toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    conflicts = 0
    schedule_map = {}
    for (course, day), (time, room) in individual:
        teacher = TEACHERS[course]
        if (day, time, room) in schedule_map or (day, time, teacher) in schedule_map:
            conflicts += 1
        schedule_map[(day, time, room)] = course
        schedule_map[(day, time, teacher)] = course
    return (conflicts,)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)

def custom_mutate(individual, indpb=0.2):
    for i in range(len(individual)):
        if random.random() < indpb:
            course, day = individual[i][0]
            new_time = random.choice(TIME_SLOTS[8:] if course == "NO102" else TIME_SLOTS[:8])
            new_room = (
                NO102_LOCATION if course == "NO102" else
                "ENG_DRAW_LAB" if course == "GE105" else
                random.choice(ROOM_LIST)
            )
            individual[i] = ((course, day), (new_time, new_room))
    return (individual,)

toolbox.register("mutate", custom_mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

def run_ga():
    population = toolbox.population(n=50)
    generations = 100
    crossover_prob = 0.8
    mutation_prob = 0.2
    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < crossover_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values
        for mutant in offspring:
            if random.random() < mutation_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)
        population[:] = offspring
        best = tools.selBest(population, 1)[0]
        if best.fitness.values[0] == 0:
            break
    return best

def generate_timetable():
    best_schedule = run_ga()
    data = []
    for (course, day), (time, room) in best_schedule:
        teacher = TEACHERS[course]
        data.append([course, teacher, day, time, room])
    df = pd.DataFrame(data, columns=["Course", "Teacher", "Day", "Time", "Room"])
    df.to_excel("Timetable.xlsx", index=False)

generate_timetable()