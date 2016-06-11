import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import argparse
import GDD
import os

parser = argparse.ArgumentParser(description="Plot the relationship between max growing degree days and base temperature")
parser.add_argument("input_dir", help="Path to folder with GDD files to be used in the plot")
parser.add_argument("output_figure", help="Path to file in which figure will be saved")

args = parser.parse_args()




def max_cum_GDD(gdds):
    """Read GDD data from file, calculate cummulative GDDs and return the maximum value.

        Args:
            GDD_file (string): a path to the csv file containing the GDD data.

        Returns:
            float: the maximum cummulative GDD.

    """
    cum_gdd=gdds.cumsum()
    return max(cum_gdd)






def base_t_range(data,name,start=0,end=30):
    """Calculate the max cummulative GDD for varying values of base_t.

        The range of base temperatures goes from 'start' to 'end' increasing by 1.

        Args:
            data(pandas series or dataframe): Min and M temperature
                                data from wich GDD is calculated.
            name(string): name to be used in the gdd column of the
                         resulting DataFrame
            start(integer): First value for base_t
            end(integer): Last value for base_t

        Returns:
            pandas DataFrame: 2 columns dataframe. First column
                 ("base_t") is the value used for base temperature.
                 Second column (labeled with the name argument) contains the max cummulative gdd for the corresponding base temperature
    """

    max_gdds={"base_t":[],"gdd":[]}

    for base_t in range(start,end):
        gdd_data=GDD.apply_GDD(data,base_t=base_t)
        max_gdds["base_t"].append(base_t)
        max_gdds["gdd"].append(max_cum_GDD(gdd_data['gdd']))

        df=pd.DataFrame(max_gdds)
        df.rename(columns={"gdd":name},inplace=True)


    return df


data_files=os.listdir(args.input_dir)
name=data_files[0].split('.csv')[0]
data=GDD.read_file(data_files[0])
baset_GDD=base_t_range(data=data,name=name)

for data_file in data_files[1:]:
    name=data_file.split('.csv')[0]
    data=GDD.read_file(data_file)
    df=base_t_range(data=data,name=name)
    baset_GDD=pd.merge(baset_GDD,df)

baset_GDD=pd.melt(baset_GDD,id_vars='base_t',value_vars=[c for c in baset_GDD.columns[1:]])






#lm=pd.stats.ols.OLS(x=df["base_t"],y=df["gdd"])

fig=baset_GDD.plot(kind='scatter',x='base_t',y='value')
plt.savefig(args.output_figure)