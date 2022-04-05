import time
from multiprocessing import Process
from interaction_users import InteractionUsers


if __name__ == '__main__':
    run_bots = int(input('How many bots do you want to run?: '))

    for _ in range(run_bots):
        condition_to_initialize = input('messages or continue messages or analysis: ')
        first_contact = int(input('first user: '))
        last_contact = int(input('last user: '))
        conversations = input('Type the name to save messages: ')
        analysis_total = input('Type the name to save total: ')
        analysis_resume = input('Type the save the resume: ')
        # a_b_testing = input('Will you do a|b testing? (yes or no): ')
        # a_message = input('Type the A message: ')
        # b_message = input('Type the B message: ')

        class_in_thread = InteractionUsers(
            condition_to_initialize = condition_to_initialize,
            first_contact  = first_contact,
            last_contact = last_contact,
            conversations = conversations,
            analysis_total = analysis_total,
            analysis_resume = analysis_resume,
            # a_b_testing = a_b_testing,
            # a_message = a_message,
            # b_message = b_message
        )
        process = Process(target=class_in_thread.sending_messages)
        process.start()
        time.sleep(10)