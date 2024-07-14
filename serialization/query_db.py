import sqlite3
from multiprocessing import Pool
import time

def run_query(query):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

    # Function to run queries in parallel
def run_parallel_queries(queries):
    with Pool(128) as p:
        results = p.map(run_query, queries)
    return results

# Function to run queries sequentially
def run_sequential_queries(queries):
    results = []
    for query in queries:
        results.append(run_query(query))
    return results

if __name__ == '__main__':
    
    # Prepare queries
    queries = [
        "SELECT AVG(value) FROM your_table WHERE id % 4 = 0",
        "SELECT AVG(value) FROM your_table WHERE id % 4 = 1",
    ] * 500
    
    # Time parallel queries
    start_time = time.time()
    parallel_results = run_parallel_queries(queries)
    parallel_time = time.time() - start_time
    
    # Time sequential queries
    start_time = time.time()
    sequential_results = run_sequential_queries(queries)
    sequential_time = time.time() - start_time
    
    # Print results
    print(f"Parallel query time: {parallel_time} seconds")
    print(f"Sequential query time: {sequential_time} seconds")
    print(f"Speedup: {sequential_time / parallel_time}x")
    
    # Verify that both methods return the same results
    assert parallel_results == sequential_results, "Results do not match!"
    

