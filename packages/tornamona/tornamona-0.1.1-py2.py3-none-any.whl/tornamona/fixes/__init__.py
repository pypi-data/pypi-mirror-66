from typing import Optional, List, Union, Dict, AnyStr

import pandas as pd


class Dataset:
    fixes: List = []
    data: Optional[Union[Dict, pd.DataFrame, pd.Series]] = None
    sources: Union[AnyStr, Dict] = None

    def register_fixes(self):
        pass

    def get(self, **kwargs) -> 'Dataset':
        ...
        return self

    def clean(self) -> 'Dataset':
        ...
        return self

    def to_df(self) -> pd.DataFrame:
        if isinstance(pd.DataFrame, self.data):
            return self.data
        else:  # assume it's something concatable
            return pd.concat(self.data)
