from api import go_vote
# from database_operations import save_user_session_data, get_session_key, read_data_from_database
from redis_operations import refresh_user_votes, set_user_votes_to_zero


def main():
    go_vote(3523439, '5fce6c95872a37fdbfa525367f035942')


if __name__ == "__main__":
    main()


