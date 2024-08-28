from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys
import random  # Import random module

class CriticalError(Exception):
    """Custom exception to signal a critical error requiring program termination."""
    # print("FUCK FUCK FUCK")
    pass

def go_vote(userId, uk):
    code = random.choice([0, -1, 418, 0, 0, 0, 0, -1])  # Randomly choose between 0, -1, 418
    time.sleep(0.5)
    print(f"userId = {userId} ##### code = {code}")
    return code

def get_session_key():
    userId = ''.join(random.choices('0123456789', k=7))  # Generate 7-digit userId
    uk = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))  # Generate 32-character uk
    time.sleep(0.2)

    return userId, uk


def lets_fucking_go(userId, uk):
    try:
        for i in range(10):  # Each user has 50 votes
            code = go_vote(userId, uk)
            if code == 0:
                print(f"User {userId} has voted {i + 1} times")
            elif code == -1:
                print(f"User {userId} has run out of votes")
                break
            else:
                print(f" {userId} 接口异常: uk={uk}")
                raise CriticalError(f"Critical error in user {userId} with uk={uk}")
        
        print(f"用户 {userId} 刷完")
    
    except CriticalError as e:
        print(e)
        raise  # Re-raise to propagate the exception to the main thread

def main():
    thread_num = 10

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        futures = []
        
        user_data = (('111', 'ac4da227e6f2d88276bc84f650374c20', 50), ('222', '1e894a371d9fc02ef1be9f040e1ee58e', 50), ('333', '08562031a50458cb3a604be31d60861a', 50), ('444', '08562031a50458cbjjjjj60861a', 50), ('555', '111111111111111111111', 50))
        if user_data:
            futures += [executor.submit(lets_fucking_go, userId, uk) for userId, uk, remain_vote_num in user_data]

        # Wait for all threads to complete or fail
        try:
            for future in as_completed(futures):
                future.result()  # Will raise exception if any thread fails
        except CriticalError:
            # print("Terminating all threads due to a critical error.")
            executor.shutdown(wait=False)  # Immediately shut down the executor
            sys.exit(1)  # Exit the entire program

    print("=========== Program finished ==============")

if __name__ == "__main__":
    main()
