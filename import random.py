import random
import pandas as pd
from deap import base, creator, tools
from collections import defaultdict



# 1st  year 
C_DIV_1_2 = {
    "GE104": {"hr_pw": 3, "dur_hr": 1, "stud": 100},
    "HS101": {"hr_pw": 2, "dur_hr": 1, "stud": 100},
    "MA102A": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "PH101": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "ME101": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "CH101": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "CS111": {"hr_pw": 3, "dur_hr": 1, "stud": 80}
}

C_DIV_3_4 = {
    "CY101": {"hr_pw": 3, "dur_hr": 1, "stud": 100},
    "GE103": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "GE105": {"hr_pw": 1, "dur_hr": 3, "stud": 120}, 
    "MA102B": {"hr_pw": 3, "dur_hr": 1, "stud": 190},
    "GE106": {"hr_pw": 3, "dur_hr": 1, "stud": 190},
    "GE110": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "PH102": {"hr_pw": 1, "dur_hr": 4, "stud": 100},  
    "GE102": {"hr_pw": 1, "dur_hr": 4, "stud": 120}   
}

# 2nd  year courses
C_AI = {
    "EE207": {"hr_pw": 3, "dur_hr": 1, "stud":90},
    "CS503": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "MA302": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "BM101": {"hr_pw": 3, "dur_hr": 1, "stud": 190},
    "GE108": {"hr_pw": 3, "dur_hr": 1, "stud": 190}
}

C_CE = {
    "CE301": {"hr_pw": 2, "dur_hr": 1, "stud": 60},
    "CE302": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "CE303": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "MA202": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "BM101": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "GE108": {"hr_pw": 3, "dur_hr": 1, "stud": 60}
}

C_CH = {
    "CH203": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "CH204": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "CH231": {"hr_pw": 2, "dur_hr": 2, "stud": 60}, 
    "BM101": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "C230": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "GE108": {"hr_pw": 3, "dur_hr": 1, "stud": 60}
}

C_CSE = {
    "CS202": {"hr_pw": 3, "dur_hr": 1, "stud": 90},
    "CS204": {"hr_pw": 3, "dur_hr": 1, "stud": 80},
    "MA202": {"hr_pw": 3, "dur_hr": 1, "stud": 120},
    "BM101": {"hr_pw": 3, "dur_hr": 1, "stud": 60},
    "GE108": {"hr_pw": 3, "dur_hr": 1, "stud": 60}
}


# common courses with fix location
C_COMMON = {
    "NS102": {"hr_pw": 3, "dur_hr": 1, "fixed_time": "5:00 PM", "loc": "Sports Complex", "stud": 240},
    "NS104": {"hr_pw": 3, "dur_hr": 1, "fixed_time": "5:00 PM", "loc": "Sports Complex", "stud": 240}
}

TEACHERS = {
    "GE104": "K Ramchandra", "HS101": "Dr. Kamal", "MA102A": "Dr. Tapas", "PH101": "Dr. Shankadeep",
    "CY101": "Dr. Mohan", "GE103": "Prof. Sharma", "GE105": "Prof. Rawat", "GE106": "Dr. Bhatia", 
    "GE110": "Prof. Kumar", "EE207": "Dr. Sinha", "CS503": "Prof. Gupta", "MA302": "Dr. Joshi",
    "BM101": "Dr. Pandey", "GE108": "Prof. Trivedi", "CE301": "Dr. Goel", "CE302": "Prof. Singh",
    "CE303": "Dr. Rathore", "MA202": "Prof. Das", "CH203": "Dr. Verma", "CH204": "Prof. Kapoor",
    "CH231": "Dr. Reddy", "C230": "Prof. Agarwal", "CS202": "Dr. Khanna", "CS204": "Prof. Mehra",
    "ME101": "Dr. Patel", "CH101": "Prof. Rao", "CS111": "Dr. Malik", "NS102": "Coach Sharma",
    "NS104": "Coach ", "GE102": "Prof. Agarwal", "MA102B": "Dr. Tapas"  
}

# Room with capacity 
ROOMS = {
    "M1": 60, "M2": 60, "M3": 120, "M4": 120, "M5": 200, "M6":200,
    "CS1": 75, "CS2": 75, "EE1": 75, "ME1": 75 ,"EESH": 80, "MESH":80
}

# Labs
LABS = {
    "PH Lab": 120,
    "Drawing Lab": 120, 
    "Chemical Lab": 60,
    "Sports Complex": 300
}

# Individual lab location 
LAB_COURSES = {
    "PH102": "PH Lab", 
    "GE105": "Drawing Lab", 
    "CH231": "Chemical Lab",
    "GE102": "Drawing Lab"  # Assigned to Drawing Lab
}

# Time slots
TIMES = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]

# Consecutive time slot blocks for multi-hour courses
CONS_3HR = {
    "9:00 AM": ["9:00 AM", "10:00 AM", "11:00 AM"],
    "10:00 AM": ["10:00 AM", "11:00 AM", "12:00 PM"],
    "2:00 PM": ["2:00 PM", "3:00 PM", "4:00 PM"],
    "3:00 PM": ["3:00 PM", "4:00 PM", "5:00 PM"]
}

# 4-hour blocks - fixed to just two start times
CONS_4HR = {
    "9:00 AM": ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM"],
    "2:00 PM": ["2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
}

# 2-hour blocks
CONS_2HR = {
    "9:00 AM": ["9:00 AM", "10:00 AM"],
    "10:00 AM": ["10:00 AM", "11:00 AM"],
    "11:00 AM": ["11:00 AM", "12:00 PM"],
    "2:00 PM": ["2:00 PM", "3:00 PM"],
    "3:00 PM": ["3:00 PM", "4:00 PM"],
    "4:00 PM": ["4:00 PM", "5:00 PM"]
}

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]



# For consistent course assignment
class CourseSchedule:
    def __init__(self, div, course, config):
        self.div = div
        self.course = course
        self.hr_pw = config["hr_pw"]
        self.dur_hr = config["dur_hr"]
        self.fixed_time = config.get("fixed_time", None)
        self.loc = config.get("loc", None)
        self.stud = config.get("stud", 0)
        self.time = None
        self.room = None
        self.days = []

# Reset creator if running multiple times
try:
    if 'FitnessMin' in creator.__dict__:
        del creator.FitnessMin
        del creator.Individual
except:
    pass

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()

def get_valid_starts(dur_hr):
    """Return valid starting time slots based on course duration."""
    if dur_hr == 4:
        return ["9:00 AM", "2:00 PM"]  # Only two start times for 4-hour courses
    elif dur_hr == 3:
        return ["9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM"]
    elif dur_hr == 2:
        return list(CONS_2HR.keys())
    else:  # 1 hour
        return TIMES

def get_cons_slots(start, dur_hr):
    """Get consecutive time slots based on start time and duration."""
    if dur_hr == 4:
        return CONS_4HR.get(start, [])
    elif dur_hr == 3:
        return CONS_3HR.get(start, [])
    elif dur_hr == 2:
        return CONS_2HR.get(start, [])
    else:  # 1 hour
        return [start]

def get_suitable_rooms(stud_count, is_lab_course=False):
    """Get rooms that can accommodate the student count."""
    suitable = []
    
    # Check if it's a lab course
    if is_lab_course:
        for room, capacity in LABS.items():
            if capacity >= stud_count:
                suitable.append(room)
    else:
        # Regular classroom
        for room, capacity in ROOMS.items():
            if capacity >= stud_count:
                suitable.append(room)
    
    return suitable if suitable else (list(LABS.keys()) if is_lab_course else list(ROOMS.keys()))

def create_individual():
    schedule = []
    course_schedules = []
    
    # Create course schedules for consistent assignments
    def create_course_schedules(course_dict, div):
        schedules = []
        for course, config in course_dict.items():
            if config["hr_pw"] > 0:  # Only schedule courses with hours > 0
                cs = CourseSchedule(div, course, config)
                
                # Handle course time assignment
                if cs.fixed_time:
                    cs.time = cs.fixed_time
                else:
                    valid_starts = get_valid_starts(cs.dur_hr)
                    cs.time = random.choice(valid_starts)
                
                # Handle room assignment based on capacity
                if cs.loc:
                    cs.room = cs.loc
                else:
                    is_lab = course in LAB_COURSES
                    if is_lab:
                        cs.room = LAB_COURSES[course]
                    else:
                        suitable_rooms = get_suitable_rooms(cs.stud, is_lab)
                        cs.room = random.choice(suitable_rooms)
                
                # Choose days based on how many times per week the course meets
                avail_days = DAYS.copy()
                random.shuffle(avail_days)
                cs.days = avail_days[:cs.hr_pw]
                
                schedules.append(cs)
        return schedules
    
    # Create schedules for all divisions
    course_schedules.extend(create_course_schedules(C_DIV_1_2, "Div 1-2"))
    course_schedules.extend(create_course_schedules(C_DIV_3_4, "Div 3-4"))
    course_schedules.extend(create_course_schedules(C_AI, "AI 2Y"))
    course_schedules.extend(create_course_schedules(C_CE, "CE 2Y"))
    course_schedules.extend(create_course_schedules(C_CH, "CH 2Y"))
    course_schedules.extend(create_course_schedules(C_CSE, "CSE 2Y"))
    course_schedules.extend(create_course_schedules(C_COMMON, "Common"))
    
    # Convert course schedules to schedule items
    for cs in course_schedules:
        for day in cs.days:
            time_slots = get_cons_slots(cs.time, cs.dur_hr)
            
            for slot in time_slots:
                schedule.append(((cs.div, cs.course, day, cs.stud), (slot, cs.room)))
    
    return schedule

toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    conflicts = 0
    room_time_map = {}  
    div_time_map = {}   
    
    
    multi_hr_entries = defaultdict(list)  
    
    for (div, course, day, stud), (time, room) in individual:
        
        if (day, time, room) in room_time_map:
            conflicts += 1
        else:
            room_time_map[(day, time, room)] = (div, course)
        
        
        if div != "Common" and (div, day, time) in div_time_map:
            conflicts += 1
        else:
            div_time_map[(div, day, time)] = course
        
        
        room_cap = ROOMS.get(room, LABS.get(room, 0))
        if stud > room_cap:
            conflicts += 3  
        
        
        
        dur_hr = 1  
        for course_dict in [C_DIV_1_2, C_DIV_3_4, C_AI, C_CE, C_CH, C_CSE, C_COMMON]:
            if course in course_dict and course_dict[course].get("dur_hr", 1) > 1:
                dur_hr = course_dict[course]["dur_hr"]
                break
        
        if dur_hr > 1:
            multi_hr_entries[(div, course, day)].append(time)
    
    
    for (div, course, day), times in multi_hr_entries.items():
        
        dur_hr = 1
        for course_dict in [C_DIV_1_2, C_DIV_3_4, C_AI, C_CE, C_CH, C_CSE, C_COMMON]:
            if course in course_dict:
                dur_hr = course_dict[course].get("dur_hr", 1)
                break
        
        
        if len(times) != dur_hr:
            conflicts += 5 
        
        # Check if slots are consecutive
        sorted_times = sorted(times, key=lambda x: TIMES.index(x) if x in TIMES else -1)
        # Check against the appropriate consecutive time block structure
        if dur_hr == 4:
            time_blocks = [CONS_4HR]
        elif dur_hr == 3:
            time_blocks = [CONS_3HR]
        elif dur_hr == 2:
            time_blocks = [CONS_2HR]
        else:
            time_blocks = []
            
        consecutive_found = False
        for time_block in time_blocks:
            for start_time, cons_slots in time_block.items():
                if set(sorted_times) == set(cons_slots[:dur_hr]):
                    consecutive_found = True
                    break
            if consecutive_found:
                break
        
        if not consecutive_found and dur_hr > 1:
            conflicts += 5  # Heavy penalty for non-consecutive slots
    
    # my own constartint for fixing the same corse should happen on same time after consequtively days same course should have same time and room on different days
    course_details = defaultdict(list)
    for (div, course, day, _), (time, room) in individual:
        # Skip multi-hour courses for consistency check on time
        dur_hr = 1
        for course_dict in [C_DIV_1_2, C_DIV_3_4, C_AI, C_CE, C_CH, C_CSE, C_COMMON]:
            if course in course_dict:
                dur_hr = course_dict[course].get("dur_hr", 1)
                break
        
        if dur_hr > 1:
            # For multi-hour courses, we only check room consistency
            course_details[(div, course, "room")].append(room)
        else:
            # For regular courses, check both time and room consistency
            course_details[(div, course, "time")].append(time)
            course_details[(div, course, "room")].append(room)
    
    # Penalize inconsistent times and rooms
    for (div, course, attr), values in course_details.items():
        if len(set(values)) > 1:
            conflicts += len(set(values)) - 1
    
    return (conflicts,)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)

def custom_mutate(individual, indpb=0.2):
    # Group by division and course
    course_groups = defaultdict(list)
    for i, ((div, course, day, stud), (time, room)) in enumerate(individual):
        course_groups[(div, course)].append(i)
    
    # Mutate entire course groups to maintain consistency
    for (div, course), indices in course_groups.items():
        if random.random() < indpb:
            # Skip fixed-time courses like NS102, NS104
            is_fixed_time = False
            for course_dict in [C_COMMON]:
                if course in course_dict and "fixed_time" in course_dict[course]:
                    is_fixed_time = True
                    break
            
            if is_fixed_time:
                continue
            
            # Get course duration
            dur_hr = 1
            stud_count = 0
            for course_dict in [C_DIV_1_2, C_DIV_3_4, C_AI, C_CE, C_CH, C_CSE, C_COMMON]:
                if course in course_dict:
                    dur_hr = course_dict[course].get("dur_hr", 1)
                    stud_count = course_dict[course].get("stud", 0)
                    break
            
            # Choose a new starting time based on duration
            valid_starts = get_valid_starts(dur_hr)
            new_start_time = random.choice(valid_starts)
            
            # Choose a new room based on capacity
            is_lab = course in LAB_COURSES
            if is_lab:
                new_room = LAB_COURSES[course]
            else:
                suitable_rooms = get_suitable_rooms(stud_count, is_lab)
                new_room = random.choice(suitable_rooms)
            
            # Group indices by day to handle multi-hour slots for the same day
            day_indices = defaultdict(list)
            for idx in indices:
                (d, c, day, s), (time, _) = individual[idx]
                day_indices[day].append((idx, time))
            
            # For each day, update all time slots
            for day, idx_time_pairs in day_indices.items():
                # Sort by time to ensure we're updating in order
                sorted_pairs = sorted(idx_time_pairs, key=lambda x: TIMES.index(x[1]) if x[1] in TIMES else -1)
                
                if dur_hr > 1:
                    # Get all consecutive slots for multi-hour courses
                    time_slots = get_cons_slots(new_start_time, dur_hr)
                    
                    # Make sure we have enough indices
                    if len(sorted_pairs) == dur_hr:
                        for slot_idx, time_slot in enumerate(time_slots):
                            idx = sorted_pairs[slot_idx][0]
                            individual[idx] = ((div, course, day, stud_count), (time_slot, new_room))
                else:
                    # Regular 1-hour course - just update time and room
                    for idx, _ in sorted_pairs:
                        individual[idx] = ((div, course, day, stud_count), (new_start_time, new_room))
    
    return (individual,)

toolbox.register("mutate", custom_mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

def run_ga():
    population = toolbox.population(n=100)
    generations = 200
    cx_prob = 0.7
    mut_prob = 0.3
    
    # Track the best individual
    best_fitness = float('inf')
    best_individual = None
    stagnation = 0
    
    for gen in range(generations):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values
        
        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid_ind:
            ind.fitness.values = toolbox.evaluate(ind)
        
        population[:] = offspring
        
        # Check if we found a better solution
        current_best = tools.selBest(population, 1)[0]
        if current_best.fitness.values[0] < best_fitness:
            best_fitness = current_best.fitness.values[0]
            best_individual = current_best
            stagnation = 0
            
            # Print progress every 10 generations
            if gen % 10 == 0:
                print(f"Gen {gen}: Best fitness = {best_fitness}")
        else:
            stagnation += 1
        
        # Early stopping if solution is optimal or stagnation
        if best_fitness == 0 or stagnation > 30:
            print(f"Stop at gen {gen}: {'optimal' if best_fitness == 0 else 'stagnation'}")
            break
    
    return best_individual if best_individual else tools.selBest(population, 1)[0]

def get_course_dur(course):
    """Get the duration of a course in hours."""
    for course_dict in [C_DIV_1_2, C_DIV_3_4, C_AI, C_CE, C_CH, C_CSE, C_COMMON]:
        if course in course_dict:
            return course_dict[course].get("dur_hr", 1)
    return 1

def generate_timetable():
    print("Running GA to generate timetable...")
    best_schedule = run_ga()
    fitness = best_schedule.fitness.values[0] if best_schedule.fitness.values else float('inf')
    print(f"Solution found with {fitness} conflicts")
    
    # Convert to DataFrame
    data = []
    for (div, course, day, stud), (time, room) in best_schedule:
        teacher = TEACHERS.get(course, "Unknown")
        
        # Get room capacity
        room_cap = ROOMS.get(room, LABS.get(room, 0))
        
        # Check if room is overbooked
        status = "OK" if stud <= room_cap else f"OVERBOOKED ({stud}/{room_cap})"
        
        data.append([div, course, teacher, day, time, room, stud, room_cap, status])
    
    df = pd.DataFrame(data, columns=["Division", "Course", "Teacher", "Day", "Time", "Room", 
                                      "Students", "Room Cap", "Status"])
    
    # Process multi-hour courses
    for _, row in df.iterrows():
        course = row["Course"]
        dur_hr = get_course_dur(course)
        
        if dur_hr > 1:
            # Find all slots for this course on this day
            same_course_day = df[(df["Course"] == course) & 
                               (df["Day"] == row["Day"]) & 
                               (df["Division"] == row["Division"])]
            
            if len(same_course_day) == dur_hr:
                # Sort by time
                sorted_times = sorted(same_course_day["Time"].tolist(), 
                                     key=lambda x: TIMES.index(x) if x in TIMES else -1)
                
                # Mark first slot
                df.loc[(df["Course"] == course) & 
                     (df["Day"] == row["Day"]) & 
                     (df["Division"] == row["Division"]) & 
                     (df["Time"] == sorted_times[0]), "Course"] = f"{course} ({dur_hr}hr start)"
                
                
                for i in range(1, len(sorted_times) - 1):
                    df.loc[(df["Course"] == course) & 
                         (df["Day"] == row["Day"]) & 
                         (df["Division"] == row["Division"]) & 
                         (df["Time"] == sorted_times[i]), "Course"] = f"{course} (cont)"
                
                # Mark last slot
                df.loc[(df["Course"] == course) & 
                     (df["Day"] == row["Day"]) & 
                     (df["Division"] == row["Division"]) & 
                     (df["Time"] == sorted_times[-1]), "Course"] = f"{course} (end)"
    
    
    df.to_excel("Timetable_Capacity.xlsx", index=False)
    print("Timetable saved as 'Timetable_Capacity.xlsx'")
    
    
    cap_issues = df[df["Status"].str.contains("OVERBOOKED")]
    if not cap_issues.empty:
        print(f"\nFound {len(cap_issues)} capacity issues:")
        for _, row in cap_issues.iterrows():
            print(f"{row['Division']} - {row['Course']} in {row['Room']} on {row['Day']} at {row['Time']}: {row['Students']} students, capacity {row['Room Cap']}")
    else:
        print("\nNo  issues found!")
    
    return df


if __name__ == "__main__":
    generate_timetable()
