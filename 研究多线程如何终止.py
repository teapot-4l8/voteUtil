from concurrent.futures import ThreadPoolExecutor
import time
import sys
import random  # Import random module

class CriticalError(Exception):
    """Custom exception to signal a critical error requiring program termination."""
    print("FUCK FUCK FUCK")
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
    for i in range(10):  # Each user has 50 votes
        code = go_vote(userId, uk)
        if code == 0:
            print(f"User {userId} has voted {i + 1} times")
        elif code == -1:
            print(f"User {userId} has run out of votes")
            break
        else:
            print(f" {userId} 接口异常:uk={uk}")
            sys.exit() 
            # break

    print(f"用户 {userId} 刷完")


def main():
    thread_num = 5
    remain_local_user = True  # Local users still have votes

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        while True:
            if remain_local_user:
                user_data = (('111', 'ac4da227e6f2d88276bc84f650374c20', 50), ('222', '1e894a371d9fc02ef1be9f040e1ee58e', 50), ('333', '08562031a50458cb3a604be31d60861a', 50), ('444', '08562031a50458cbjjjjj60861a', 50), ('555', '111111111111111111111', 50))
                if not user_data:  # No more local users with votes
                    remain_local_user = False
                    print("用户完啦")
                    # continue
                futures = [executor.submit(lets_fucking_go, userId, uk) for userId, uk, remain_vote_num in user_data]
            else:
                print("No users left, creating new users...")
                futures = [executor.submit(lets_fucking_go, *get_session_key()) for _ in range(thread_num)]
            
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception caught in future: {e}")
                
    print("=========== Program finished ==============")


if __name__ == "__main__":
    main()
