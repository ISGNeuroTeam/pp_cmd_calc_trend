import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax

from .calc_trend import calc_trend


class CalcTrendCommand(BaseCommand):
    # define syntax of your command here
    syntax = Syntax(
        [
            Positional("value_col", required=True, otl_type=OTLType.TEXT),
            Positional("window", required=False, otl_type=OTLType.TEXT),
            Keyword("time_field", required=False, otl_type=OTLType.TEXT)
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start calc_trend command')

        # that is how you get arguments
        value_col = self.get_arg("value_col").value
        window = self.get_arg("window").value or None
        time_field = self.get_arg("time_field").value or '_time'

        if time_field not in df.columns:
            raise Exception(
                f'No {time_field} in dataframe. Use time_field argument or make sure that dataframe has `_time` field'
            )

        self.logger.debug('Setting datetime index')
        self.logger.debug(f'Command calc_trend: value_col = {value_col}')
        self.logger.debug(f'Command calc_trend: window = {window}')

        df['_dt'] = pd.to_datetime(df[time_field])
        df.set_index('_dt', inplace=True, unit='s')

        df = calc_trend(df, value_col, window)

        self.log_progress('Calc trend command is complete')

        return df
