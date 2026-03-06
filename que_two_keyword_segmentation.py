def segment_query(query, dictionary):
    word_set = set(dictionary)
    memo = {}

    def solve(s):
        if s in memo: return memo[s]
        if not s: return [""]

        results = []
        for i in range(1, len(s) + 1):
            prefix = s[:i]
            if prefix in word_set:
                for suffix in solve(s[i:]):
                    results.append((prefix + " " + suffix).strip())
        
        memo[s] = results
        return results

    return solve(query)

# Test Runs 
dict1 = ["nepal", "trekking", "guide", "nepaltrekking"]
dict2 = ["visit", "kathmandu", "nepal", "visitkathmandu", "kathmandunepal"]
dict3 = ["everest", "hiking", "trek"]

print("Ex 1:", segment_query("nepaltrekkingguide", dict1))
print("Ex 2:", segment_query("visitkathmandunepal", dict2))
print("Ex 3:", segment_query("everesthikingtrail", dict3))