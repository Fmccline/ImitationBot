from trajectory_reader import RLBotTrajectoryReader
import datetime

from trajectory_writer import RLBotTrajectoryWriter


def main():
    log_path = 'logs/'
    output_path = 'csv/'
    trajectory_converter = RLBotTrajectoryConverter(log_path, output_path)

    start_date = datetime.date(year=2019, month=4, day=8)
    end_date = datetime.date(year=2019, month=4, day=14)
    skipped_dates = [] #[datetime.date(year=2019, month=4, day=17)]
    trajectory_converter.convert_files_to_csv(start_date, end_date, skipped_dates)


class RLBotTrajectoryConverter:

    def __init__(self, log_path, json_path):
        self.log_path = log_path
        self.json_path = json_path

    def get_bot_files(self, start_date, end_date, skipped_dates):
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
            if current_date not in skipped_dates:
                for bot_name in bot_names:
                    filename = f'{self.log_path}{bot_name}-{current_date}.log'
                    bot_file = (filename, bot_name)
                    bot_files.append(bot_file)
            current_date += datetime.timedelta(days=1)
        return bot_files

    def convert_files_to_csv(self, start_date, end_date, skipped_dates):
        output_file = f'{self.json_path}{start_date}_{end_date}-trajectories.csv'
        bot_files = self.get_bot_files(start_date, end_date, skipped_dates)

        trajectory_reader = RLBotTrajectoryReader()
        all_trajectories = []
        for filename, bot_name in bot_files:
            print(f"Reading trajectories from {filename}")
            trajectories = trajectory_reader.get_trajectories_from_file(filename, bot_name)
            for trajectory in trajectories:
                all_trajectories.append(trajectory)
        print(f"Writing {len(all_trajectories)} to {output_file}")
        RLBotTrajectoryWriter.write_trajectories_to_csv(all_trajectories, output_file)


if __name__ == '__main__':
    main()
