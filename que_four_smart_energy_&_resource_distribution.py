# Hourly demand for Districts A, B, C
hourly_demand = {
    6: {'A': 20, 'B': 15, 'C': 25},
    7: {'A': 22, 'B': 16, 'C': 28},
    8: {'A': 24, 'B': 18, 'C': 30}
}

# Energy Sources
sources = {
    'Solar':   {'capacity': 50, 'available_hours': range(6, 19), 'cost': 1.0},
    'Hydro':   {'capacity': 40, 'available_hours': range(0, 25), 'cost': 1.5},
    'Diesel':  {'capacity': 60, 'available_hours': range(17, 24), 'cost': 3.0}
}

# Tolerance
tolerance = 0.1

def allocate_energy(hour, demand):
    allocation = {source: {district:0 for district in demand} for source in sources}
    remaining_demand = demand.copy()
    
    available_sources = {k:v for k,v in sources.items() if hour in v['available_hours']}
    available_sources = dict(sorted(available_sources.items(), key=lambda x: x[1]['cost']))
    
    for src_name, src in available_sources.items():
        src_capacity = src['capacity']
        for district, req in remaining_demand.items():
            if req <= 0:
                continue
            allocated = min(req, src_capacity)
            allocation[src_name][district] = allocated
            remaining_demand[district] -= allocated
            src_capacity -= allocated
    
    for district in demand:
        min_req = demand[district]*(1-tolerance)
        max_req = demand[district]*(1+tolerance)
        total_supplied = sum(allocation[src][district] for src in allocation)
        if total_supplied < min_req:
            print(f"Warning: District {district} demand not met within ±10% at Hour {hour}")
    
    return allocation

def calculate_total_cost(allocation):
    total_cost = 0
    for src_name, dist_alloc in allocation.items():
        cost_per_kwh = sources[src_name]['cost']
        total_cost += sum(dist_alloc.values()) * cost_per_kwh
    return total_cost

results = {}
for hour, demand in hourly_demand.items():
    alloc = allocate_energy(hour, demand)
    cost = calculate_total_cost(alloc)
    results[hour] = {'allocation': alloc, 'cost': cost}


for hour, data in results.items():
    print(f"\n Hour {hour} ")
    print("District Demand:", hourly_demand[hour])
    print("Allocation per Source:")
    for src, dist_alloc in data['allocation'].items():
        print(f"  {src}: {dist_alloc}")
    print("Total Cost:", data['cost'])