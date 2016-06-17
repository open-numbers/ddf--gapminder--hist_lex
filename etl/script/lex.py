# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file

# configuration of file paths
source = '../source/gapdata004 v7.xlsx'
out_dir = '../../'


if __name__ == '__main__':
    data001 = pd.read_excel(source, sheetname='Data & meta data')

    # entities
    area = data001['Area'].unique()
    area_id = list(map(to_concept_id, area))
    ent = pd.DataFrame([], columns=['area', 'name'])

    ent['area'] = area_id
    ent['name'] = area

    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    ent.to_csv(path, index=False)

    # datapoints
    data001_dp_1 = data001[['Area', 'Year', 'Life expectancy at birth']].copy()
    data001_dp_2 = data001[['Area', 'Year', 'Life expectancy, with interpolations']].copy()
    data001_dp_3 = data001[['Area', 'Year', 'Data quality']].copy()

    data001_dp_1.columns = ['area', 'year', 'life_expectancy_at_birth']
    data001_dp_2.columns = ['area', 'year', 'life_expectancy_with_interpolations']
    data001_dp_3.columns = ['area', 'year', 'data_quality']

    data001_dp_1['area'] = data001_dp_1['area'].map(to_concept_id)
    data001_dp_2['area'] = data001_dp_2['area'].map(to_concept_id)
    data001_dp_3['area'] = data001_dp_3['area'].map(to_concept_id)
    data001_dp_3['data_quality'] = data001_dp_3['data_quality'].map(
        lambda x: int(x.split('.')[0]) if isinstance(x, str) else x
    )

    path1 = os.path.join(out_dir, 'ddf--datapoints--life_expectancy_at_birth--by--area--year.csv')
    path2 = os.path.join(out_dir, 'ddf--datapoints--life_expectancy_with_interpolations--by--area--year.csv')
    path3 = os.path.join(out_dir, 'ddf--datapoints--data_quality--by--area--year.csv')

    data001_dp_1.dropna().sort_values(by=['area', 'year']).to_csv(path1, index=False, float_format='%g')
    data001_dp_2.dropna().sort_values(by=['area', 'year']).to_csv(path2, index=False, float_format='%g')
    data001_dp_3.dropna().sort_values(by=['area', 'year']).to_csv(path3, index=False, float_format='%g')

    # concepts
    conc = ['life_expectancy_at_birth', 'life_expectancy_with_interpolations', 'data_quality', 'area', 'year', 'name']
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['concept'] = conc
    cdf['name'] = ['Life expectancy at birth', 'Life expectancy, with interpolations', 'Data quality', 'Area', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'measure', 'measure', 'entity_domain', 'time', 'string']

    cdf.to_csv(os.path.join(out_dir, 'ddf--concepts.csv'), index=False)

    # index
    create_index_file(out_dir)

    print('Done.')
