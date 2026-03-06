def get_max_coverage(locations):
    n = len(locations)
   
    if n <= 2: return n 
    
    overall_max = 0
    for i in range(n):
        slopes = {} 
        for j in range(n):
          if i == j: continue 
            
          dx = locations[j][0] - locations[i][0]
          dy = locations[j][1] - locations[i][1]
            
          # Calculate slope and handle vertical lines 
          slope = (dy / dx) if dx != 0 else 'vertical'
          slopes[slope] = slopes.get(slope, 0) + 1
            
        if slopes:
          current_max = max(slopes.values()) + 1
          overall_max = max(overall_max, current_max)
            
    return overall_max

# Verification 
# Example 1: Ideal Repeater Placement
example1_points = [[1,1],[2,2],[3,3]]
# Example 2: Complex Repeater Placement
example2_points = [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]

print(f"Max coverage (Example 1): {get_max_coverage(example1_points)}") 
print(f"Max coverage (Example 2): {get_max_coverage(example2_points)}") 