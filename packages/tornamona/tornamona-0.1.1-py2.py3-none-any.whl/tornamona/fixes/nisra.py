import pandas as pd

from tornamona.fixes import Dataset


class WeeklyDeaths(Dataset):
    """
    Pulls the weekly death statistics from 2009-latest

    Includes Respiratory and COVID19 case counts for 2020

    Does not include supplemental breakdowns (Age/Sex/Cause/Place of Death) as these are not available for pre-2020 values
    """

    def get(self, **kwargs) -> 'Dataset':
        self.data = {}
        self.sources = {
            'historical': 'https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/Weekly_Deaths%20'
                          '-%20Historical.xls',
            'covid_19': 'https://www.nisra.gov.uk/sites/nisra.gov.uk/files/publications/Weekly_Deaths.xls'
        }
        for source, url in self.sources.items():
            self.data[source] = pd.read_excel(url, sheet_name=None)  # Get all sheet names as a dict of DataFrames

        return self

    def _0_strip_irrelevant_sheets(self) -> Dataset:
        """
        Remove things like the Background, Definition, and Chart sheets, as well as out of scope data such as the
        age and sex breakdowns.

        This relies on the existing inconsistency in whether 'Weekly Deaths' has a space or a underscore (Spaces are
        used in the weekly reports, underscore is used for the breakdowns

        :return:
        """
        for source, data in self.data.items():
            self.data[source] = {
                sheet: df for sheet, df in data.items()
                if sheet.startswith('Weekly Deaths_')
            }

        return self

    def _1_dump_first_3_rows_and_rename_columns(self) -> Dataset:
        """
        First 3 rows are junk
        Helpfully, historical and covid don't have the same columns, including the pointless presence of both
        week start and week end and *then* dropping week *start* in the 2020 results...

        :return:
        """
        new_columns = {
            'historical': ("Week", "Week Start", "Week End", "Total Deaths", "Average Deaths for previous 5 years",
                           "Min 5 year deaths", "Max 5 year deaths"),
            'covid_19': ("Week", "Week End", "Total Deaths", "Average Deaths for previous 5 years",
                         "Min 5 year deaths", "Max 5 year deaths", "Respiratory Deaths",
                         "Average Respiratory Deaths for previous 5 years", "COVID19 Deaths")
        }

        for source, data in self.data.items():
            for sheet, df in data.items():
                # Edit inplace because we're lazy and evil #TODO be better than this
                df = df[3:].copy()  # Needs to be a copy to avoid 'SettingWithCException'
                df.columns = new_columns[source]
                if source == 'covid_19':
                    df['Week Start'] = df['Week End'] - pd.Timedelta(days=6)
                data[sheet] = df

        return self

    def _2_concat_and_dropna(self) -> Dataset:
        """
        Now the sheets are in a format that should be able to just be concatenated, so if we've
        screwed up anywhere, there should be warnings/errors here.
        :return:
        """
        super_df = pd.concat([
            df
            for data in self.data.values()
            for df in data.values()
        ])

        super_df.dropna(how='all', inplace=True)  # Drop empty lines

        # Drop rows with text in the week column (advisory junk)
        self.data = super_df[super_df.Week.str.isdigit().astype(bool)]

        return self

    def _3_2014_typo(self) -> Dataset:
        """
        There is a typo in the Week Starts column in the 2014 dataset where one week magically appears to be 2004
        :return:
        """
        if not any(self.data['Week Start'] == pd.to_datetime('2004-02-01')):
            raise ValueError("Can't find broken value, this fix has possibly been resolved!")

        self.data.loc[
            self.data['Week Start'] == pd.to_datetime('2004-02-01'),
            'Week Start'
        ] = pd.to_datetime('2014-02-01')

        return self

    def _4_fix_dtypes(self) -> Dataset:
        """Fortunately this is super easy, barely an inconvenience, thanks to the pandas built-in 'infer_objects()'"""
        self.data = self.data.infer_objects().reset_index(drop=True)

    def clean(self) -> Dataset:
        self._0_strip_irrelevant_sheets()
        self._1_dump_first_3_rows_and_rename_columns()
        self._2_concat_and_dropna()
        self._3_2014_typo()
        self._4_fix_dtypes()

        return self
