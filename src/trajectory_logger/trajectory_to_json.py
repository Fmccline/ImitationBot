from RLBotTrajectoryReader import RLBotTrajectoryReader
import datetime

from RLBotTrajectoryWriter import RLBotTrajectoryWriter


def get_bot_files(start_date, end_date):
    """
    Gets log files from the start date up to but not including the end date

    :param start_date: datetime.date
    :param end_date: datetime.date
    :return: list of tuples (filename, bot_name)
    """
    bot_files = []
    bot_names = ['ReliefBot', 'ReliefBot(2)', 'ReliefBot(3)', 'ReliefBot(4)']
    current_date = start_date
    while current_date != end_date:
        for bot_name in bot_names:
            filename = f'logs/{bot_name}-{current_date}.log'
            bot_file = (filename, bot_name)
            bot_files.append(bot_file)
        current_date += datetime.timedelta(days=1)
    return bot_files


def main():
    end_date = datetime.date(year=2019, month=4, day=17)
    start_date = end_date - datetime.timedelta(3)
    output_file = f'json/{start_date}_{end_date}-rlbot-trajectories.json'
    bot_files = get_bot_files(start_date, end_date)

    trajectory_reader = RLBotTrajectoryReader()
    all_trajectories = []
    for filename, bot_name in bot_files:
        trajectories = trajectory_reader.get_trajectories_from_file(filename, bot_name)
        all_trajectories.append(trajectories)

    RLBotTrajectoryWriter.write_trajectories_to_json(trajectories, output_file)


if __name__ == '__main__':
    main()
